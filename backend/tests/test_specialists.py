from decimal import Decimal

from backend.app.agents.background_agent import (
    check_background_information,
)
from backend.app.agents.blog_agent import (
    _fallback_blog_review,
)
from backend.app.agents.salary_agent import (
    calculate_salary,
    redact_pii,
)
from backend.app.services.ticket_store import (
    InMemoryTicketStore,
)


def test_blog_fallback_review():

    result = _fallback_blog_review(
        "This is a short article about AWS Lambda."
    )

    assert "OVERALL_SCORE" in result
    assert "RECOMMENDATIONS" in result
    assert "ACCEPTED" in result


def test_background_check_complete():

    employee = {
        "full_name": "Employee One",
        "date_of_birth": "1999-01-01",
        "government_id": "REDACTED",
        "address": "Bengaluru",
        "employment_history": "Company A",
        "education_verification": "Verified",
    }

    result = check_background_information(
        employee
    )

    assert result["status"] == "COMPLETE"
    assert result["missing_fields"] == []


def test_background_check_missing_fields():

    employee = {
        "full_name": "Employee One",
        "date_of_birth": "",
        "government_id": "REDACTED",
        "address": "",
        "employment_history": "Company A",
        "education_verification": "Verified",
    }

    result = check_background_information(
        employee
    )

    assert result["status"] == "INCOMPLETE"

    assert "Date of Birth" in result[
        "missing_fields"
    ]

    assert "Address" in result[
        "missing_fields"
    ]


def test_salary_calculation():

    result = calculate_salary(
        base_salary=Decimal("50000"),
        allowance=Decimal("5000"),
        deduction=Decimal("3000"),
        performance_score=Decimal("92"),
    )

    assert result["incentive"] == Decimal(
        "10000.00"
    )

    assert result["gross_salary"] == Decimal(
        "65000.00"
    )

    assert result["net_salary"] == Decimal(
        "62000.00"
    )


def test_salary_low_performance():

    result = calculate_salary(
        base_salary=Decimal("50000"),
        allowance=Decimal("5000"),
        deduction=Decimal("3000"),
        performance_score=Decimal("60"),
    )

    assert result["incentive"] == Decimal(
        "0.00"
    )

    assert result["net_salary"] == Decimal(
        "52000.00"
    )


def test_pii_redaction():

    text = (
        "Employee ID 123456789012 "
        "Account 1234567890123456"
    )

    result = redact_pii(text)

    assert "123456789012" not in result
    assert "1234567890123456" not in result


def test_ticket_creation():

    store = InMemoryTicketStore()

    ticket = store.create_ticket(
        user_id="EMP001",
        summary="Unable to access payroll portal.",
    )

    assert ticket["ticket_id"].startswith(
        "TKT-"
    )

    assert ticket["status"] == "OPEN"

    stored = store.get_ticket(
        ticket["ticket_id"]
    )

    assert stored is not None