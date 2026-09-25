import logging
from typing import Any

from backend.app.graph.state import AgentState

logger = logging.getLogger(__name__)


REQUIRED_BACKGROUND_FIELDS = {
    "full_name": "Full Name",
    "date_of_birth": "Date of Birth",
    "government_id": "Government ID",
    "address": "Address",
    "employment_history": "Employment History",
    "education_verification": "Education Verification",
}


def check_background_information(
    employee_data: dict[str, Any],
) -> dict[str, Any]:
    """
    Check whether required HR/background-check fields exist.

    This function does not make any external AWS calls.
    """

    missing_fields: list[str] = []

    for field, display_name in REQUIRED_BACKGROUND_FIELDS.items():
        value = employee_data.get(field)

        if value is None:
            missing_fields.append(display_name)
        elif isinstance(value, str) and not value.strip():
            missing_fields.append(display_name)

    if missing_fields:
        status = "INCOMPLETE"
    else:
        status = "COMPLETE"

    return {
        "status": status,
        "missing_fields": missing_fields,
        "checked_fields": list(REQUIRED_BACKGROUND_FIELDS.values()),
    }


def _extract_employee_data(user_input: str) -> dict[str, Any]:
    """
    Simple local representation for Step 4.

    Later this will be replaced with DynamoDB/S3 retrieval.
    """

    return {
        "full_name": user_input,
    }


def background_agent(state: AgentState) -> dict[str, Any]:
    """
    A2 Security Background Check Agent.
    """

    employee_data = state.get("tool_results", {}).get(
        "employee_data"
    )

    if not employee_data:
        employee_data = _extract_employee_data(
            state.get("user_input", "")
        )

    result = check_background_information(employee_data)

    if result["status"] == "COMPLETE":
        response = (
            "Background verification information is complete. "
            "No required fields are missing."
        )
        workflow_status = "COMPLETED"

    else:
        missing = ", ".join(result["missing_fields"])

        response = (
            "Background verification information is incomplete. "
            f"Missing required information: {missing}."
        )

        workflow_status = "ACTION_REQUIRED"

    logger.info(
        "A2 background check completed: status=%s missing=%s",
        result["status"],
        len(result["missing_fields"]),
    )

    return {
        "response": response,
        "status": workflow_status,
        "requires_human_approval": False,
        "tool_results": {
            "agent": "A2_BACKGROUND",
            "background_check": result,
        },
    }