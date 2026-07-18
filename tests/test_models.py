import pytest

from app.models import Employee


def test_employee_creation_defaults():
    employee = Employee(
        employee_id="E001",
        first_name="Abdul",
        last_name="Khan",
        department="Engineering",
        job_title="Software Developer",
        manager="E010",
        username="abdul.khan"
    )

    assert employee.employee_id == "E001"
    assert employee.first_name == "Abdul"
    assert employee.last_name == "Khan"
    assert employee.department == "Engineering"
    assert employee.job_title == "Software Developer"
    assert employee.manager == "E010"
    assert employee.username == "abdul.khan"
    assert employee.status == "active"
    assert employee.groups == []
    assert employee.applications == []


def test_employee_to_dict_and_from_dict():
    employee = Employee(
        employee_id="E002",
        first_name="Nina",
        last_name="Patel",
        department="HR",
        job_title="HR Specialist",
        manager="E011",
        username="nina.patel",
        groups=["hr"],
        applications=["hris"]
    )

    payload = employee.to_dict()

    assert payload == {
        "employee_id": "E002",
        "first_name": "Nina",
        "last_name": "Patel",
        "department": "HR",
        "job_title": "HR Specialist",
        "manager": "E011",
        "status": "active",
        "username": "nina.patel",
        "groups": ["hr"],
        "applications": ["hris"],
    }

    recreated = Employee.from_dict(payload)

    assert isinstance(recreated, Employee)
    assert recreated == employee
