import json
import sqlite3
from pathlib import Path

from app.iam_service import IAMService
from app.models import Employee


def test_sqlite_mover_updates_json_and_sqlite(tmp_path):
    employees_file = tmp_path / "employees.json"
    audit_file = tmp_path / "audit_log.json"
    db_file = tmp_path / "iam.db"

    service = IAMService(
        employees_path=str(employees_file),
        roles_path=str(Path(__file__).resolve().parents[1] / "data" / "roles.json"),
        audit_log_path=str(audit_file),
        db_path=str(db_file),
    )

    employee = Employee(
        employee_id="M200",
        first_name="Alex",
        last_name="Morgan",
        department="IT",
        job_title="Help Desk Analyst",
        manager="M010",
    )

    result_create = service.create_employee(employee)
    assert result_create["success"] is True

    result_update = service.update_employee_role("M200", "IAM Analyst")
    assert result_update["success"] is True

    saved_json = json.loads(employees_file.read_text(encoding="utf-8"))
    assert saved_json[0]["employee_id"] == "M200"
    assert saved_json[0]["job_title"] == "IAM Analyst"
    assert saved_json[0]["username"] == "alex.morgan"

    conn = sqlite3.connect(str(db_file))
    cursor = conn.cursor()
    cursor.execute("SELECT employee_id, job_title, username FROM employees WHERE employee_id = ?", ("M200",))
    row = cursor.fetchone()
    conn.close()

    assert row is not None
    assert row[0] == "M200"
    assert row[1] == "IAM Analyst"
    assert row[2] == "alex.morgan"


def test_sqlite_mover_employee_id_and_username_preserved(tmp_path):
    employees_file = tmp_path / "employees.json"
    audit_file = tmp_path / "audit_log.json"
    db_file = tmp_path / "iam.db"

    service = IAMService(
        employees_path=str(employees_file),
        roles_path=str(Path(__file__).resolve().parents[1] / "data" / "roles.json"),
        audit_log_path=str(audit_file),
        db_path=str(db_file),
    )

    employee = Employee(
        employee_id="M201",
        first_name="Beth",
        last_name="Reed",
        department="Finance",
        job_title="Finance Analyst",
        manager="M011",
    )

    result_create = service.create_employee(employee)
    assert result_create["success"] is True
    old_username = result_create["employee"].username

    result_update = service.update_employee_role("M201", "Security Analyst")
    assert result_update["success"] is True
    updated = result_update["employee"]

    assert updated.employee_id == "M201"
    assert updated.username == old_username

    conn = sqlite3.connect(str(db_file))
    cursor = conn.cursor()
    cursor.execute("SELECT employee_id, username FROM employees WHERE employee_id = ?", ("M201",))
    row = cursor.fetchone()
    conn.close()

    assert row[0] == "M201"
    assert row[1] == old_username


def test_sqlite_mover_employee_not_found(tmp_path):
    employees_file = tmp_path / "employees.json"
    audit_file = tmp_path / "audit_log.json"
    db_file = tmp_path / "iam.db"

    service = IAMService(
        employees_path=str(employees_file),
        roles_path=str(Path(__file__).resolve().parents[1] / "data" / "roles.json"),
        audit_log_path=str(audit_file),
        db_path=str(db_file),
    )

    result = service.update_employee_role("NONEXIST", "IAM Analyst")

    assert result["success"] is False
    assert "not found" in result["message"]
