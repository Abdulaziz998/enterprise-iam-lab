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


def test_create_read_and_move_employee_flow(tmp_path):
    setup_service_for_test(tmp_path)

    client = TestClient(main.app)
    create_response = client.post(
        "/employees",
        json={
            "employee_id": "API001",
            "first_name": "Ada",
            "last_name": "Lovelace",
            "department": "Engineering",
            "job_title": "Software Developer",
            "manager": "API010",
        },
    )

    assert create_response.status_code == 200
    created_payload = create_response.json()
    assert created_payload["success"] is True

    get_response = client.get("/employees/API001")
    assert get_response.status_code == 200
    get_payload = get_response.json()
    assert get_payload["employee"]["employee_id"] == "API001"

    move_response = client.post(
        "/employees/API001/move",
        json={"new_job_title": "IAM Analyst"},
    )

    assert move_response.status_code == 200
    move_payload = move_response.json()
    assert move_payload["success"] is True
    assert move_payload["employee"]["employee_id"] == "API001"
    assert move_payload["employee"]["job_title"] == "IAM Analyst"
    assert move_payload["employee"]["username"] == "ada.lovelace"


def test_move_employee_successfully(tmp_path):
    service = setup_service_for_test(tmp_path)

    employee = Employee(
        employee_id="M001",
        first_name="Mina",
        last_name="Rossi",
        department="IT",
        job_title="Help Desk Analyst",
        manager="M010",
        username="mina.rossi",
    )
    service.create_employee(employee)

    client = TestClient(main.app)
    response = client.post(
        "/employees/M001/move",
        json={"new_job_title": "IAM Analyst"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["employee"]["employee_id"] == "M001"
    assert data["employee"]["job_title"] == "IAM Analyst"
    assert data["employee"]["username"] == "mina.rossi"


def test_move_employee_updates_groups_and_applications(tmp_path):
    service = setup_service_for_test(tmp_path)

    employee = Employee(
        employee_id="M002",
        first_name="Nina",
        last_name="Lopez",
        department="IT",
        job_title="Help Desk Analyst",
        manager="M020",
        username="nina.lopez",
    )
    service.create_employee(employee)

    client = TestClient(main.app)
    response = client.post(
        "/employees/M002/move",
        json={"new_job_title": "Security Analyst"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["employee"]["groups"] == ["security"]
    assert data["employee"]["applications"] == ["siem", "incident_response_tool"]


def test_move_employee_missing_employee_returns_404(tmp_path):
    setup_service_for_test(tmp_path)

    client = TestClient(main.app)
    response = client.post(
        "/employees/NOTFOUND/move",
        json={"new_job_title": "IAM Analyst"},
    )

    assert response.status_code == 404
    data = response.json()
    assert data["success"] is False
    assert data["message"] == "Employee ID 'NOTFOUND' not found."


def test_move_employee_invalid_role_returns_400(tmp_path):
    service = setup_service_for_test(tmp_path)

    employee = Employee(
        employee_id="M003",
        first_name="Omar",
        last_name="Diaz",
        department="IT",
        job_title="Help Desk Analyst",
        manager="M030",
        username="omar.diaz",
    )
    service.create_employee(employee)

    client = TestClient(main.app)
    response = client.post(
        "/employees/M003/move",
        json={"new_job_title": "Not A Real Role"},
    )

    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
    assert "Invalid job title" in data["message"]
