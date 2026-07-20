from fastapi.testclient import TestClient

from app.main import app, service


def test_get_roles_returns_all_roles_sorted():
    client = TestClient(app)
    response = client.get("/roles")

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["count"] == len(data["roles"])
    assert data["roles"] == sorted(data["roles"], key=lambda role: role["job_title"])

    assert all("job_title" in role for role in data["roles"])
    assert all("groups" in role for role in data["roles"])
    assert all("applications" in role for role in data["roles"])
    assert all("permissions" not in role for role in data["roles"])


def test_get_role_by_title_returns_role():
    client = TestClient(app)
    response = client.get("/roles/Help Desk Analyst")

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["role"]["job_title"] == "Help Desk Analyst"
    assert data["role"]["groups"] == ["helpdesk"]
    assert data["role"]["applications"] == ["ticketing_system"]


def test_get_role_by_title_missing_returns_404():
    client = TestClient(app)
    response = client.get("/roles/Unknown Role")

    assert response.status_code == 404
    data = response.json()
    assert data["success"] is False
    assert data["message"] == "Role not found."
