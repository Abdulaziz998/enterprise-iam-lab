import sqlite3
from pathlib import Path

from app.database import Database
from app.models import Employee


def test_successful_insert(tmp_path):
    db_file = tmp_path / "iam.db"
    db = Database(db_path=str(db_file))
    db.initialize()

    employee = Employee(
        employee_id="I001",
        first_name="Grace",
        last_name="Hopper",
        department="Engineering",
        job_title="Software Developer",
        manager="I010",
        username="grace.hopper",
    )

    result = db.insert_employee(employee)

    assert result["success"] is True
    assert "inserted successfully" in result["message"]


def test_duplicate_employee_id_rejection(tmp_path):
    db_file = tmp_path / "iam.db"
    db = Database(db_path=str(db_file))
    db.initialize()

    employee = Employee(
        employee_id="I002",
        first_name="Alan",
        last_name="Turing",
        department="Engineering",
        job_title="Software Developer",
        manager="I010",
        username="alan.turing",
    )

    first_result = db.insert_employee(employee)
    second_result = db.insert_employee(employee)

    assert first_result["success"] is True
    assert second_result["success"] is False
    assert "already exists" in second_result["message"]


def test_employee_exists_in_sqlite_after_insert(tmp_path):
    db_file = tmp_path / "iam.db"
    db = Database(db_path=str(db_file))
    db.initialize()

    employee = Employee(
        employee_id="I003",
        first_name="Ada",
        last_name="Lovelace",
        department="Engineering",
        job_title="Software Developer",
        manager="I010",
        username="ada.lovelace",
    )

    db.insert_employee(employee)

    conn = sqlite3.connect(str(db_file))
    cursor = conn.cursor()
    cursor.execute(
        "SELECT employee_id, first_name, last_name, username FROM employees WHERE employee_id = ?",
        (employee.employee_id,),
    )
    row = cursor.fetchone()
    conn.close()

    assert row is not None
    assert row[0] == employee.employee_id
    assert row[1] == employee.first_name
    assert row[2] == employee.last_name
    assert row[3] == employee.username
