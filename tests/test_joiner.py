import json
from pathlib import Path

from app.iam_service import IAMService
from app.models import Employee


def test_successful_employee_creation(tmp_path):
    employees_file = tmp_path / "employees.json"
    service = IAMService(employees_path=str(employees_file), roles_path=str(Path(__file__).resolve().parents[1] / "data" / "roles.json"))

    employee = Employee(
        employee_id="E100",
        first_name="Abdul",
        last_name="Aziz",
        department="Engineering",
        job_title="Software Developer",
        manager="E010",
    )

    result = service.create_employee(employee)

    assert result["success"] is True
    assert result["employee"].username == "abdul.aziz"
    assert result["employee"].groups == ["engineering"]
    assert result["employee"].applications == ["code_repo", "ci_system", "dev_aws_account"]

    saved = json.loads(employees_file.read_text(encoding="utf-8"))
    assert saved[0]["employee_id"] == "E100"


def test_duplicate_employee_id_rejection(tmp_path):
    employees_file = tmp_path / "employees.json"
    service = IAMService(employees_path=str(employees_file), roles_path=str(Path(__file__).resolve().parents[1] / "data" / "roles.json"))

    first = Employee(
        employee_id="E101",
        first_name="Nina",
        last_name="Patel",
        department="HR",
        job_title="HR Specialist",
        manager="E011",
    )
    second = Employee(
        employee_id="E101",
        first_name="Nina",
        last_name="Patel",
        department="HR",
        job_title="HR Specialist",
        manager="E011",
    )

    assert service.create_employee(first)["success"] is True
    result = service.create_employee(second)

    assert result["success"] is False
    assert "already exists" in result["message"]


def test_missing_required_field_rejection(tmp_path):
    service = IAMService(
        employees_path=str(tmp_path / "employees.json"),
        roles_path=str(Path(__file__).resolve().parents[1] / "data" / "roles.json"),
    )
    employee = Employee(
        employee_id="",
        first_name="Abdul",
        last_name="",
        department="Engineering",
        job_title="Software Developer",
        manager="E010",
    )

    result = service.create_employee(employee)

    assert result["success"] is False
    assert "Missing required fields" in result["message"]
    assert "employee_id" in result["message"]
    assert "last_name" in result["message"]


def test_username_generation(tmp_path):
    service = IAMService(
        employees_path=str(tmp_path / "employees.json"),
        roles_path=str(Path(__file__).resolve().parents[1] / "data" / "roles.json"),
    )
    employee = Employee(
        employee_id="E102",
        first_name="Abdul",
        last_name="Aziz",
        department="Engineering",
        job_title="Software Developer",
        manager="E010",
    )

    result = service.create_employee(employee)

    assert result["success"] is True
    assert result["employee"].username == "abdul.aziz"


def test_duplicate_username_handling(tmp_path):
    service = IAMService(
        employees_path=str(tmp_path / "employees.json"),
        roles_path=str(Path(__file__).resolve().parents[1] / "data" / "roles.json"),
    )

    first = Employee(
        employee_id="E103",
        first_name="Abdul",
        last_name="Aziz",
        department="Engineering",
        job_title="Software Developer",
        manager="E010",
    )
    second = Employee(
        employee_id="E104",
        first_name="Abdul",
        last_name="Aziz",
        department="Engineering",
        job_title="Software Developer",
        manager="E010",
    )

    result1 = service.create_employee(first)
    result2 = service.create_employee(second)

    assert result1["success"] is True
    assert result2["success"] is True
    assert result1["employee"].username == "abdul.aziz"
    assert result2["employee"].username == "abdul.aziz2"


def test_role_assignment(tmp_path):
    service = IAMService(
        employees_path=str(tmp_path / "employees.json"),
        roles_path=str(Path(__file__).resolve().parents[1] / "data" / "roles.json"),
    )
    employee = Employee(
        employee_id="E105",
        first_name="Sofia",
        last_name="Lee",
        department="Finance",
        job_title="Finance Analyst",
        manager="E012",
    )

    result = service.create_employee(employee)

    assert result["success"] is True
    assert result["employee"].groups == ["finance"]
    assert result["employee"].applications == ["finance_ledger", "expense_portal"]


def test_invalid_job_title_rejection(tmp_path):
    service = IAMService(
        employees_path=str(tmp_path / "employees.json"),
        roles_path=str(Path(__file__).resolve().parents[1] / "data" / "roles.json"),
    )
    employee = Employee(
        employee_id="E106",
        first_name="Jon",
        last_name="Doe",
        department="Legal",
        job_title="Legal Consultant",
        manager="E013",
    )

    result = service.create_employee(employee)

    assert result["success"] is False
    assert "Invalid job title" in result["message"]
