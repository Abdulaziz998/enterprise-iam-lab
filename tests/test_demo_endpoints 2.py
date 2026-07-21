from pathlib import Path

from fastapi.testclient import TestClient

from app.iam_service import IAMService
from app.main import app


client = TestClient(app)


def configure_demo_service(tmp_path):
    import app.main as main_module
    original = main_module.service, main_module.database
    demo_service = IAMService(
        employees_path=str(tmp_path / "employees.json"),
        roles_path=str(Path(__file__).resolve().parents[1] / "data" / "roles.json"),
        audit_log_path=str(tmp_path / "audit_log.json"),
        db_path=str(tmp_path / "iam.db"),
    )
    main_module.service = demo_service
    main_module.database = demo_service.database
    return original


def restore_demo_service(original):
    import app.main as main_module
    main_module.service, main_module.database = original


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "Enterprise IAM API",
        "version": "1.0.0",
    }


def test_demo_seed_is_idempotent(tmp_path):
    original = configure_demo_service(tmp_path)
    try:
        first = client.post("/demo/seed")
        second = client.post("/demo/seed")

        assert first.status_code == 200
        assert second.status_code == 200
        assert first.json()["success"] is True
        assert second.json()["success"] is True

        employees = client.get("/employees").json()["employees"]
        assert len(employees) == 10
        assert any(employee["status"] == "terminated" for employee in employees)
        assert len(client.get("/audit-logs").json()["events"]) > 0
    finally:
        restore_demo_service(original)


def test_demo_reset_restores_predictable_state(tmp_path):
    original = configure_demo_service(tmp_path)
    try:
        client.post(
            "/employees",
            json={
                "employee_id": "CUSTOM1",
                "first_name": "Custom",
                "last_name": "User",
                "department": "Engineering",
                "job_title": "Software Developer",
                "manager": "Manager",
                "status": "active",
            },
        )

        response = client.post("/demo/reset")
        assert response.status_code == 200
        assert response.json()["success"] is True

        employees = client.get("/employees").json()["employees"]
        assert len(employees) == 10
        assert all(employee["employee_id"].startswith("D10") for employee in employees)
    finally:
        restore_demo_service(original)
