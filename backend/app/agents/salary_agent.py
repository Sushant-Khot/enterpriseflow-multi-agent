import logging
import re
from decimal import Decimal, ROUND_HALF_UP
from typing import Any

from backend.app.graph.state import AgentState
from backend.app.services.bedrock import invoke_bedrock

logger = logging.getLogger(__name__)


SALARY_SYSTEM_PROMPT = """
You are the Salary and Incentive Explanation Agent.

Your task is to explain a salary calculation that has already
been performed by deterministic business logic.

IMPORTANT:

- Do NOT recalculate the salary.
- Do NOT modify any provided numeric result.
- Do NOT request bank account numbers.
- Do NOT expose sensitive personal information.
- Explain the calculation clearly.
- Clearly distinguish salary, deductions and incentives.

Return a concise professional explanation.
"""


def _money(value: Decimal) -> Decimal:
    """
    Round monetary values to two decimal places.
    """

    return value.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


def calculate_salary(
    base_salary: Decimal,
    allowance: Decimal,
    deduction: Decimal,
    performance_score: Decimal,
) -> dict[str, Decimal]:
    """
    Deterministic salary calculation.

    Incentive rules:

    90-100  -> 20% of base salary
    80-89   -> 15%
    70-79   -> 10%
    below 70 -> 0%

    This is a demonstration business rule and can later
    be replaced by organization-approved rules.
    """

    if base_salary < 0:
        raise ValueError("Base salary cannot be negative.")

    if allowance < 0:
        raise ValueError("Allowance cannot be negative.")

    if deduction < 0:
        raise ValueError("Deduction cannot be negative.")

    if not 0 <= performance_score <= 100:
        raise ValueError(
            "Performance score must be between 0 and 100."
        )

    if performance_score >= 90:
        incentive_rate = Decimal("0.20")
    elif performance_score >= 80:
        incentive_rate = Decimal("0.15")
    elif performance_score >= 70:
        incentive_rate = Decimal("0.10")
    else:
        incentive_rate = Decimal("0.00")

    incentive = _money(
        base_salary * incentive_rate
    )

    gross_salary = _money(
        base_salary + allowance + incentive
    )

    net_salary = _money(
        gross_salary - deduction
    )

    return {
        "base_salary": _money(base_salary),
        "allowance": _money(allowance),
        "incentive": incentive,
        "deduction": _money(deduction),
        "gross_salary": gross_salary,
        "net_salary": net_salary,
        "incentive_rate": incentive_rate,
    }


PII_PATTERNS = [
    (
        re.compile(r"\b\d{12}\b"),
        "[REDACTED-ID]",
    ),
    (
        re.compile(r"\b\d{10,18}\b"),
        "[REDACTED-ACCOUNT]",
    ),
]


def redact_pii(text: str) -> str:
    """
    Basic local PII redaction.

    This is intentionally simple for Step 4.
    A stronger PII mechanism/Bedrock Guardrails integration
    will be added in the security stage.
    """

    result = text

    for pattern, replacement in PII_PATTERNS:
        result = pattern.sub(replacement, result)

    return result


def _format_calculation(calculation: dict[str, Decimal]) -> str:
    return (
        f"Base Salary: {calculation['base_salary']}\n"
        f"Allowance: {calculation['allowance']}\n"
        f"Incentive: {calculation['incentive']}\n"
        f"Deduction: {calculation['deduction']}\n"
        f"Gross Salary: {calculation['gross_salary']}\n"
        f"Net Salary: {calculation['net_salary']}\n"
    )


def explain_salary(
    calculation: dict[str, Decimal],
) -> str:
    """
    Ask Bedrock to explain the already-computed result.
    """

    calculation_text = _format_calculation(calculation)

    safe_text = redact_pii(calculation_text)

    try:
        result = invoke_bedrock(
            system_prompt=SALARY_SYSTEM_PROMPT,
            user_prompt=f"""
Explain this deterministic salary calculation:

<calculation>
{safe_text}
</calculation>
""",
        )

        return result["text"]

    except Exception as exc:
        logger.warning(
            "Salary explanation failed. Using local explanation. Error=%s",
            exc,
        )

        return (
            "Salary calculation completed.\n\n"
            f"{calculation_text}"
        )


def salary_agent(state: AgentState) -> dict[str, Any]:
    """
    A3 Salary and Incentive Agent.
    """

    employee_data = state.get("tool_results", {}).get(
        "employee_data",
        {},
    )

    try:
        base_salary = Decimal(
            str(employee_data.get("base_salary", "0"))
        )

        allowance = Decimal(
            str(employee_data.get("allowance", "0"))
        )

        deduction = Decimal(
            str(employee_data.get("deduction", "0"))
        )

        performance_score = Decimal(
            str(employee_data.get("performance_score", "0"))
        )

        calculation = calculate_salary(
            base_salary=base_salary,
            allowance=allowance,
            deduction=deduction,
            performance_score=performance_score,
        )

        explanation = explain_salary(calculation)

        logger.info(
            "A3 salary calculation completed for workflow=%s",
            state.get("workflow_id"),
        )

        return {
            "response": explanation,
            "status": "COMPLETED",
            "requires_human_approval": False,
            "pii_detected": True,
            "tool_results": {
                "agent": "A3_SALARY",
                "calculation": {
                    key: str(value)
                    for key, value in calculation.items()
                },
            },
        }

    except (ValueError, ArithmeticError) as exc:
        logger.warning(
            "A3 salary calculation failed: %s",
            exc,
        )

        return {
            "response": "Unable to calculate salary because the supplied salary information is invalid.",
            "status": "FAILED",
            "error": str(exc),
            "requires_human_approval": False,
            "tool_results": {
                "agent": "A3_SALARY",
            },
        }