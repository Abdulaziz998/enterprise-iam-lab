from pathlib import Path

from app.iam_service import IAMService
from app.models import Employee


def setup_service_with_employee(tmp_path, job_title="Help Desk Analyst"):
    employees_file = tmp_path / "employees.json"
    service = IAMService(employees_path=str(employees_file), roles_path=str(Path(__file__).resolve().parents[1] / "data" / "roles.json"))

    emp = Employee(
        employee_id="L001",
        first_name="Taylor",
        last_name="Smith",
        department="Support",
        job_title=job_title,
        manager="L010",
    )
    create_result = service.create_employee(emp)
    assert create_result["success"] is True
    return service, create_result["employee"]


def test_successful_termination(tmp_path):
    service, employee = setup_service_with_employee(tmp_path)

    result = service.terminate_employee(employee.employee_id)

    assert result["success"] is True
    updated = result["employee"]
    assert updated.status == "terminated"
    assert updated.groups == []
    assert updated.applications == []
    assert updated.username == employee.username
    assert updated.employee_id == employee.employee_id


def test_employee_not_found(tmp_path):
    service = IAMService(employees_path=str(tmp_path / "employees.json"), roles_path=str(Path(__file__).resolve().parents[1] / "data" / "roles.json"))

    result = service.terminate_employee("NONEXISTENT")

    assert result["success"] is False
    assert "not found" in result["message"]


def test_fields_preserved_after_termination(tmp_path):
    service, employee = setup_service_with_employee(tmp_path, job_title="Software Developer")

    before_username = employee.username
    before_id = employee.employee_id
    before_first = employee.first_name
    before_last = employee.last_name
    before_manager = employee.manager
    before_department = employee.department
    before_job_title = employee.job_title

    result = service.terminate_employee(employee.employee_id)
    assert result["success"] is True
    updated = result["employee"]

    assert updated.username == before_username
    assert updated.employee_id == before_id
    assert updated.first_name == before_first
    assert updated.last_name == before_last
    assert updated.manager == before_manager
    assert updated.department == before_department
    assert updated.job_title == before_job_title
    assert updated.status == "terminated"
    assert updated.groups == []
    assert updated.applications == []
