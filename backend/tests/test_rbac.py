import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.core.rbac import (
    ROLES,
    ROLE_PERMISSIONS,
    INTENT_PERMISSIONS,
    allowed_intent,
    has_permission,
)
from backend.app.graph.workflow import security_gate
from backend.app.services.ticket_store import ticket_store

client = TestClient(app)


def test_roles_definition():
    assert ROLES == {"EMPLOYEE", "HR_ADMIN", "SUPPORT_ADMIN"}
    assert "EMPLOYEE" in ROLE_PERMISSIONS
    assert "HR_ADMIN" in ROLE_PERMISSIONS
    assert "SUPPORT_ADMIN" in ROLE_PERMISSIONS


def test_employee_background_check_denied_403():
    """Employee background check must return HTTP 403."""
    response = client.post(
        "/api/v1/chat",
        json={
            "message": "Run background check for Alice",
            "user_id": "EMP001",
            "user_role": "EMPLOYEE",
        },
    )
    assert response.status_code == 403
    assert "not authorized" in response.json().get("detail", "").lower() or "access denied" in response.json().get("detail", "").lower()


def test_employee_accessing_other_salary_denied_403():
    """Employee accessing another employee's salary must return HTTP 403."""
    response = client.post(
        "/api/v1/chat",
        json={
            "message": "Calculate salary",
            "user_id": "EMP001",
            "user_role": "EMPLOYEE",
            "context": {
                "employee_data": {
                    "employee_id": "EMP002",
                    "base_salary": 50000,
                    "allowance": 5000,
                    "deduction": 2000,
                    "performance_score": 85,
                }
            },
        },
    )
    assert response.status_code == 403


def test_employee_salary_missing_employee_id_denied():
    """Employee salary calculation without matching employee_id must be denied."""
    assert allowed_intent("EMPLOYEE", "SALARY_INCENTIVE", employee_id=None, user_id="EMP001") is False

    response = client.post(
        "/api/v1/chat",
        json={
            "message": "Calculate my salary",
            "user_id": "EMP001",
            "user_role": "EMPLOYEE",
            "context": {},
        },
    )
    assert response.status_code == 403


def test_employee_salary_own_allowed_200():
    """Employee accessing own salary must be allowed with HTTP 200."""
    assert allowed_intent("EMPLOYEE", "SALARY_INCENTIVE", employee_id="EMP001", user_id="EMP001") is True

    response = client.post(
        "/api/v1/chat",
        json={
            "message": "Calculate my salary",
            "user_id": "EMP001",
            "user_role": "EMPLOYEE",
            "context": {
                "employee_data": {
                    "employee_id": "EMP001",
                    "base_salary": 50000,
                    "allowance": 5000,
                    "deduction": 2000,
                    "performance_score": 85,
                }
            },
        },
    )
    assert response.status_code == 200
    assert response.json()["status"] in ("SUCCESS", "COMPLETED")


def test_employee_support_request_allowed_200():
    """Employee support request (GENERAL_SUPPORT / SUPPORT_TICKET) must be allowed."""
    assert allowed_intent("EMPLOYEE", "GENERAL_SUPPORT") is True
    assert allowed_intent("EMPLOYEE", "SUPPORT_TICKET") is True

    response = client.post(
        "/api/v1/chat",
        json={
            "message": "My laptop monitor is flickering, please help",
            "user_id": "EMP001",
            "user_role": "EMPLOYEE",
        },
    )
    assert response.status_code == 200
    assert response.json()["selected_agent"] == "A4_SUPPORT"


def test_hr_admin_background_check_allowed_200():
    """HR_ADMIN background check must be allowed with HTTP 200."""
    assert allowed_intent("HR_ADMIN", "BACKGROUND_CHECK") is True

    response = client.post(
        "/api/v1/chat",
        json={
            "message": "Perform background verification check",
            "user_id": "HR001",
            "user_role": "HR_ADMIN",
            "context": {
                "employee_data": {
                    "full_name": "Bob Smith",
                    "date_of_birth": "1990-01-01",
                    "government_id": "ID12345",
                    "address": "123 Main St",
                    "employment_history": "Company XYZ",
                    "education_verification": "Degree verified",
                }
            },
        },
    )
    assert response.status_code == 200
    assert response.json()["selected_agent"] == "A2_BACKGROUND"


def test_support_admin_ticket_operations_allowed_200():
    """SUPPORT_ADMIN must be allowed to list, view, update, and resolve tickets."""
    ticket = ticket_store.create_ticket(user_id="EMP001", summary="Issue with printer")
    ticket_id = ticket["ticket_id"]

    # List tickets
    list_res = client.get("/api/v1/tickets?user_role=SUPPORT_ADMIN")
    assert list_res.status_code == 200

    # Get ticket
    get_res = client.get(f"/api/v1/tickets/{ticket_id}?user_id=SUP001&user_role=SUPPORT_ADMIN")
    assert get_res.status_code == 200

    # Update ticket
    patch_res = client.patch(
        f"/api/v1/tickets/{ticket_id}?user_role=SUPPORT_ADMIN",
        json={"status": "IN_PROGRESS"},
    )
    assert patch_res.status_code == 200

    # Resolve ticket
    resolve_res = client.post(f"/api/v1/tickets/{ticket_id}/resolve?user_role=SUPPORT_ADMIN")
    assert resolve_res.status_code == 200

    # Non-support roles must be forbidden
    assert client.get("/api/v1/tickets?user_role=EMPLOYEE").status_code == 403
    assert client.patch(f"/api/v1/tickets/{ticket_id}?user_role=HR_ADMIN", json={"status": "OPEN"}).status_code == 403


def test_security_gate_denies_invalid_role():
    """security_gate must reject roles not in ROLES."""
    invalid_state = {"user_role": "SUPERUSER", "user_input": "hello"}
    result = security_gate(invalid_state)
    assert result["security_status"] == "DENIED"
    assert result["authorization_status"] == "DENIED"
    assert result["status"] == "FORBIDDEN"

    valid_state = {"user_role": "EMPLOYEE", "user_input": "hello"}
    valid_result = security_gate(valid_state)
    assert valid_result["security_status"] == "PASSED"


def test_invalid_role_rejected_by_api():
    """Invalid roles must be rejected by the API."""
    response = client.post(
        "/api/v1/chat",
        json={
            "message": "hello",
            "user_id": "EMP001",
            "user_role": "INVALID_ROLE",
        },
    )
    assert response.status_code == 422
