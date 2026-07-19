import sqlite3
from pathlib import Path

from app.database import Database
from app.models import Employee


def test_get_all_employees_empty_database(tmp_path):
    db_file = tmp_path / "iam.db"
    db = Database(db_path=str(db_file))
    db.initialize()

    result = db.get_all_employees()

    assert result == []


def test_get_all_employees_single_employee(tmp_path):
    db_file = tmp_path / "iam.db"
    db = Database(db_path=str(db_file))
    db.initialize()

    employee = Employee(
        employee_id="E001",
        first_name="Alice",
        last_name="Smith",
        department="Engineering",
        job_title="Software Developer",
        manager="E010",
        username="alice.smith",
    )

    db.insert_employee(employee)
    result = db.get_all_employees()

    assert len(result) == 1
    assert result[0]["employee_id"] == "E001"
    assert result[0]["first_name"] == "Alice"
    assert result[0]["last_name"] == "Smith"
    assert result[0]["department"] == "Engineering"
    assert result[0]["job_title"] == "Software Developer"
    assert result[0]["manager"] == "E010"
    assert result[0]["status"] == "active"
    assert result[0]["username"] == "alice.smith"


def test_get_all_employees_multiple_employees(tmp_path):
    db_file = tmp_path / "iam.db"
    db = Database(db_path=str(db_file))
    db.initialize()

    emp1 = Employee(
        employee_id="E001",
        first_name="Alice",
        last_name="Smith",
        department="Engineering",
        job_title="Software Developer",
        manager="E010",
        username="alice.smith",
    )

    emp2 = Employee(
        employee_id="E002",
        first_name="Bob",
        last_name="Johnson",
        department="Finance",
        job_title="Finance Analyst",
        manager="E020",
        username="bob.johnson",
    )

    emp3 = Employee(
        employee_id="E003",
        first_name="Charlie",
        last_name="Brown",
        department="HR",
        job_title="HR Specialist",
        manager="E030",
        username="charlie.brown",
    )

    db.insert_employee(emp1)
    db.insert_employee(emp2)
    db.insert_employee(emp3)

    result = db.get_all_employees()

    assert len(result) == 3
    assert result[0]["employee_id"] == "E001"
    assert result[1]["employee_id"] == "E002"
    assert result[2]["employee_id"] == "E003"


def test_get_all_employees_contains_all_fields(tmp_path):
    db_file = tmp_path / "iam.db"
    db = Database(db_path=str(db_file))
    db.initialize()

    employee = Employee(
        employee_id="E100",
        first_name="Diana",
        last_name="Prince",
        department="Operations",
        job_title="Operations Manager",
        manager="E050",
        status="active",
        username="diana.prince",
    )

    db.insert_employee(employee)
    result = db.get_all_employees()

    assert len(result) == 1
    emp_dict = result[0]

    required_fields = {
        "employee_id",
        "first_name",
        "last_name",
        "department",
        "job_title",
        "manager",
        "status",
        "username",
    }
    assert set(emp_dict.keys()) == required_fields


def test_get_all_employees_ordered_by_employee_id(tmp_path):
    db_file = tmp_path / "iam.db"
    db = Database(db_path=str(db_file))
    db.initialize()

    emp_ids = ["E003", "E001", "E002"]
    for emp_id in emp_ids:
        employee = Employee(
            employee_id=emp_id,
            first_name="Test",
            last_name="User",
            department="IT",
            job_title="Analyst",
            manager="E010",
            username=f"user{emp_id}",
        )
        db.insert_employee(employee)

    result = db.get_all_employees()

    assert len(result) == 3
    assert result[0]["employee_id"] == "E001"
    assert result[1]["employee_id"] == "E002"
    assert result[2]["employee_id"] == "E003"


def test_get_all_employees_preserves_status_field(tmp_path):
    db_file = tmp_path / "iam.db"
    db = Database(db_path=str(db_file))
    db.initialize()

    employee = Employee(
        employee_id="E200",
        first_name="Eve",
        last_name="Davis",
        department="IT",
        job_title="Systems Admin",
        manager="E060",
        status="terminated",
        username="eve.davis",
    )

    db.insert_employee(employee)
    result = db.get_all_employees()

    assert len(result) == 1
    assert result[0]["status"] == "terminated"
