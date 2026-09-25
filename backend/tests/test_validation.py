from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_empty_message_is_rejected():
    response = client.post(
        "/api/v1/chat",
        json={
            "message": "",
            "user_id": "EMP001",
            "user_role": "EMPLOYEE",
        },
    )

    assert response.status_code == 422


def test_invalid_role_is_rejected():
    response = client.post(
        "/api/v1/chat",
        json={
            "message": "hello",
            "user_id": "EMP001",
            "user_role": "UNKNOWN_ROLE",
        },
    )

    assert response.status_code == 422
