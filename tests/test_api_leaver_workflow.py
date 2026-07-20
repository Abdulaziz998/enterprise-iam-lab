from pathlib import Path

from fastapi.testclient import TestClient

from app import main
from app.iam_service import IAMService
from app.models import Employee


def setup_service_for_test(tmp_path):
    db_file = tmp_path / "iam.db"
    employees_file = tmp_path / "employees.json"
    audit_file = tmp_path / "audit_log.json"
    service = IAMService(
        employees_path=str(employees_file),
        roles_path=str(Path(__file__).resolve().parents[1] / "data" / "roles.json"),
        audit_log_path=str(audit_file),
        db_path=str(db_file),
    )
    main.database = service.database
    main.service = service
    return service


def test_terminate_employee_successfully(tmp_path):
    service = setup_service_for_test(tmp_path)

    employee = Employee(
        employee_id="T001",
        first_name="Lara",
        last_name="Croft",
        department="Operations",
        job_title="Help Desk Analyst",
        manager="T010",
        username="lara.croft",
    )
    service.create_employee(employee)

    client = TestClient(main.app)
    response = client.post("/employees/T001/terminate")

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["employee"]["employee_id"] == "T001"
    assert data["employee"]["status"] == "terminated"
    assert data["employee"]["groups"] == []
    assert data["employee"]["applications"] == []
    assert data["employee"]["username"] == "lara.croft"
    assert data["employee"]["first_name"] == "Lara"
    assert data["employee"]["last_name"] == "Croft"
    assert data["employee"]["department"] == "Operations"
    assert data["employee"]["manager"] == "T010"
    assert data["employee"]["job_title"] == "Help Desk Analyst"


def test_termination_persists_in_sqlite(tmp_path):
    service = setup_service_for_test(tmp_path)

    employee = Employee(
        employee_id="T002",
        first_name="Mason",
        last_name="Reed",
        department="Engineering",
        job_title="Software Developer",
        manager="T020",
        username="mason.reed",
    )
    service.create_employee(employee)

    client = TestClient(main.app)
    response = client.post("/employees/T002/terminate")
    assert response.status_code == 200

    persisted = main.database.get_employee_by_id("T002")
    assert persisted is not None
    assert persisted["status"] == "terminated"


def test_terminate_missing_employee_returns_404(tmp_path):
    setup_service_for_test(tmp_path)

    client = TestClient(main.app)
    response = client.post("/employees/NOTFOUND/terminate")

    assert response.status_code == 404
    data = response.json()
    assert data["success"] is False
    assert data["message"] == "Employee ID 'NOTFOUND' not found."


def test_terminate_employee_end_to_end(tmp_path):
    setup_service_for_test(tmp_path)

    client = TestClient(main.app)
    create_response = client.post(
        "/employees",
        json={
            "employee_id": "T003",
            "first_name": "Jane",
            "last_name": "Doe",
            "department": "Finance",
            "job_title": "Finance Analyst",
            "manager": "T030",
        },
    )
    assert create_response.status_code == 200

    get_response = client.get("/employees/T003")
    assert get_response.status_code == 200
    assert get_response.json()["employee"]["status"] == "active"

    terminate_response = client.post("/employees/T003/terminate")
    assert terminate_response.status_code == 200
    terminate_payload = terminate_response.json()
    assert terminate_payload["success"] is True

    get_after_response = client.get("/employees/T003")
    assert get_after_response.status_code == 200
    assert get_after_response.json()["employee"]["status"] == "terminated"


def test_termination_preserves_employee_id_and_username(tmp_path):
    service = setup_service_for_test(tmp_path)

    employee = Employee(
        employee_id="T004",
        first_name="Zoe",
        last_name="Harris",
        department="HR",
        job_title="HR Specialist",
        manager="T040",
        username="zoe.harris",
    )
    service.create_employee(employee)

    client = TestClient(main.app)
    response = client.post("/employees/T004/terminate")

    assert response.status_code == 200
    data = response.json()
    assert data["employee"]["employee_id"] == "T004"
    assert data["employee"]["username"] == "zoe.harris"
