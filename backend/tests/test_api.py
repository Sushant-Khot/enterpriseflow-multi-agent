from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_chat_creates_workflow():
    response = client.post(
        "/api/v1/chat",
        json={
            "message": "Please review my blog",
            "user_id": "EMP001",
            "user_role": "EMPLOYEE",
        },
    )

    assert response.status_code == 200

    body = response.json()
    assert body["intent"] == "BLOG_REVIEW"
    assert body["selected_agent"] == "A1_BLOG"
    assert body["request_id"].startswith("EF-")
    assert body["workflow_id"].startswith("WF-")


def test_workflow_status():
    response = client.post(
        "/api/v1/chat",
        json={
            "message": "Calculate my incentive",
            "user_id": "EMP001",
            "user_role": "EMPLOYEE",
        },
    )

    workflow_id = response.json()["workflow_id"]

    status_response = client.get(f"/api/v1/workflows/{workflow_id}")

    assert status_response.status_code == 200
    assert status_response.json()["workflow_id"] == workflow_id
    assert status_response.json()["selected_agent"] == "A3_SALARY"
