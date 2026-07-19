import json
import sqlite3
from pathlib import Path

from app.iam_service import IAMService
from app.models import Employee


def test_sqlite_leaver_updates_json_and_sqlite(tmp_path):
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
        employee_id="L300",
        first_name="Noah",
        last_name="Chen",
        department="Operations",
        job_title="Help Desk Analyst",
        manager="L010",
    )

    result_create = service.create_employee(employee)
    assert result_create["success"] is True

    result_terminate = service.terminate_employee(employee.employee_id)
    assert result_terminate["success"] is True

    saved_json = json.loads(employees_file.read_text(encoding="utf-8"))
    assert saved_json[0]["employee_id"] == "L300"
    assert saved_json[0]["status"] == "terminated"
    assert saved_json[0]["groups"] == []
    assert saved_json[0]["applications"] == []

    conn = sqlite3.connect(str(db_file))
    cursor = conn.cursor()
    cursor.execute(
        "SELECT employee_id, status, username FROM employees WHERE employee_id = ?",
        ("L300",),
    )
    row = cursor.fetchone()
    conn.close()

    assert row is not None
    assert row[0] == "L300"
    assert row[1] == "terminated"
    assert row[2] == employee.username


def test_sqlite_leaver_preserves_identity(tmp_path):
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
        employee_id="L301",
        first_name="Priya",
        last_name="Nayar",
        department="Engineering",
        job_title="Software Developer",
        manager="L011",
    )

    result_create = service.create_employee(employee)
    assert result_create["success"] is True
    before_username = result_create["employee"].username

    result_terminate = service.terminate_employee("L301")
    assert result_terminate["success"] is True

    updated = result_terminate["employee"]
    assert updated.employee_id == "L301"
    assert updated.username == before_username
    assert updated.first_name == "Priya"
    assert updated.last_name == "Nayar"
    assert updated.department == "Engineering"
    assert updated.job_title == "Software Developer"
    assert updated.status == "terminated"
    assert updated.groups == []
    assert updated.applications == []

    conn = sqlite3.connect(str(db_file))
    cursor = conn.cursor()
    cursor.execute(
        "SELECT employee_id, status, username FROM employees WHERE employee_id = ?",
        ("L301",),
    )
    row = cursor.fetchone()
    conn.close()

    assert row is not None
    assert row[0] == "L301"
    assert row[1] == "terminated"
    assert row[2] == before_username
