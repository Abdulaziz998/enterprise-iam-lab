from pathlib import Path

from app.database import Database
from app.models import Employee


def test_get_employee_by_id_returns_employee(tmp_path):
    db_file = tmp_path / "iam.db"
    db = Database(db_path=str(db_file))
    db.initialize()

    employee = Employee(
        employee_id="E100",
        first_name="Sam",
        last_name="Taylor",
        department="Engineering",
        job_title="Software Developer",
        manager="E010",
        username="sam.taylor",
    )
    db.insert_employee(employee)

    result = db.get_employee_by_id("E100")

    assert result is not None
    assert result["employee_id"] == "E100"
    assert result["first_name"] == "Sam"
    assert result["last_name"] == "Taylor"
    assert result["department"] == "Engineering"
    assert result["job_title"] == "Software Developer"
    assert result["manager"] == "E010"
    assert result["status"] == "active"
    assert result["username"] == "sam.taylor"


def test_get_employee_by_id_contains_all_fields(tmp_path):
    db_file = tmp_path / "iam.db"
    db = Database(db_path=str(db_file))
    db.initialize()

    employee = Employee(
        employee_id="E101",
        first_name="Taylor",
        last_name="Reed",
        department="Finance",
        job_title="Finance Analyst",
        manager="E020",
        status="terminated",
        username="taylor.reed",
    )
    db.insert_employee(employee)

    result = db.get_employee_by_id("E101")

    assert result is not None
    assert set(result.keys()) == {
        "employee_id",
        "first_name",
        "last_name",
        "department",
        "job_title",
        "manager",
        "status",
        "username",
        "groups",
        "applications",
    }
    assert result["groups"] == []
    assert result["applications"] == []


def test_get_employee_by_id_returns_none_for_missing_employee(tmp_path):
    db_file = tmp_path / "iam.db"
    db = Database(db_path=str(db_file))
    db.initialize()

    result = db.get_employee_by_id("MISSING")

    assert result is None


def test_get_employee_by_id_matches_exact_id(tmp_path):
    db_file = tmp_path / "iam.db"
    db = Database(db_path=str(db_file))
    db.initialize()

    employee = Employee(
        employee_id="E200",
        first_name="Alex",
        last_name="Green",
        department="HR",
        job_title="HR Specialist",
        manager="E030",
        username="alex.green",
    )
    db.insert_employee(employee)

    result_exact = db.get_employee_by_id("E200")
    result_partial = db.get_employee_by_id("E20")

    assert result_exact is not None
    assert result_exact["employee_id"] == "E200"
    assert result_partial is None


def test_get_employee_by_id_ignores_other_records(tmp_path):
    db_file = tmp_path / "iam.db"
    db = Database(db_path=str(db_file))
    db.initialize()

    employees = [
        Employee(
            employee_id="E300",
            first_name="Mia",
            last_name="Lopez",
            department="Support",
            job_title="Help Desk Analyst",
            manager="E040",
            username="mia.lopez",
        ),
        Employee(
            employee_id="E301",
            first_name="Noah",
            last_name="Kim",
            department="Operations",
            job_title="Operations Manager",
            manager="E050",
            username="noah.kim",
        ),
    ]

    for emp in employees:
        db.insert_employee(emp)

    result = db.get_employee_by_id("E301")

    assert result is not None
    assert result["employee_id"] == "E301"
    assert result["first_name"] == "Noah"
    assert result["last_name"] == "Kim"
