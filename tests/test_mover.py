import json
from pathlib import Path

from app.iam_service import IAMService
from app.models import Employee


def setup_service_with_employee(tmp_path, initial_job_title="Help Desk Analyst"):
    employees_file = tmp_path / "employees.json"
    service = IAMService(employees_path=str(employees_file), roles_path=str(Path(__file__).resolve().parents[1] / "data" / "roles.json"))

    # Create an initial employee using the existing create_employee flow
    emp = Employee(
        employee_id="M001",
        first_name="Alex",
        last_name="Morgan",
        department="IT",
        job_title=initial_job_title,
        manager="M010",
    )
    create_result = service.create_employee(emp)
    assert create_result["success"] is True
    return service, emp


def test_successful_role_change(tmp_path):
    service, emp = setup_service_with_employee(tmp_path, initial_job_title="Help Desk Analyst")

    result = service.update_employee_role(emp.employee_id, "IAM Analyst")

    assert result["success"] is True
    updated = result["employee"]
    assert updated.job_title == "IAM Analyst"
    assert updated.employee_id == emp.employee_id
    assert updated.username == emp.username
    assert updated.groups == ["iam_team"]
    assert updated.applications == ["iam_console", "ticketing_system"]


def test_employee_not_found(tmp_path):
    service = IAMService(employees_path=str(tmp_path / "employees.json"), roles_path=str(Path(__file__).resolve().parents[1] / "data" / "roles.json"))

    result = service.update_employee_role("NONEXIST", "IAM Analyst")

    assert result["success"] is False
    assert "not found" in result["message"]


def test_invalid_role(tmp_path):
    service, emp = setup_service_with_employee(tmp_path)

    result = service.update_employee_role(emp.employee_id, "Legal Consultant")

    assert result["success"] is False
    assert "Invalid job title" in result["message"]


def test_username_and_id_unchanged_after_move(tmp_path):
    service, emp = setup_service_with_employee(tmp_path)

    before_username = emp.username
    before_id = emp.employee_id

    result = service.update_employee_role(emp.employee_id, "IAM Analyst")
    assert result["success"] is True
    updated = result["employee"]

    assert updated.username == before_username
    assert updated.employee_id == before_id


def test_groups_and_applications_updated(tmp_path):
    service, emp = setup_service_with_employee(tmp_path, initial_job_title="Software Developer")

    # Move Software Developer -> Security Analyst
    result = service.update_employee_role(emp.employee_id, "Security Analyst")
    assert result["success"] is True
    updated = result["employee"]

    assert updated.groups == ["security"]
    assert updated.applications == ["siem", "incident_response_tool"]
