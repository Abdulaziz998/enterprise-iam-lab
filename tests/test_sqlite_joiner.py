import json
import sqlite3
from pathlib import Path

from app.iam_service import IAMService
from app.models import Employee


def test_joiner_writes_json_and_sqlite(tmp_path):
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
        employee_id="E200",
        first_name="Abdulaziz",
        last_name="Abdi",
        department="Information Technology",
        job_title="Help Desk Analyst",
        manager="Sarah Johnson",
    )

    result = service.create_employee(employee)

    assert result["success"] is True
    assert employees_file.exists()
    saved = json.loads(employees_file.read_text(encoding="utf-8"))
    assert saved[0]["employee_id"] == "E200"
    assert saved[0]["username"] == "abdulaziz.abdi"

    conn = sqlite3.connect(str(db_file))
    cursor = conn.cursor()
    cursor.execute("SELECT employee_id, username FROM employees WHERE employee_id = ?", ("E200",))
    row = cursor.fetchone()
    conn.close()

    assert row is not None
    assert row[0] == "E200"
    assert row[1] == "abdulaziz.abdi"


def test_duplicate_employee_id_rejection(tmp_path):
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
        employee_id="E201",
        first_name="Sarah",
        last_name="Lee",
        department="HR",
        job_title="HR Specialist",
        manager="E010",
    )

    first_result = service.create_employee(employee)
    second_result = service.create_employee(employee)

    assert first_result["success"] is True
    assert second_result["success"] is False
    assert "already exists" in second_result["message"]

    conn = sqlite3.connect(str(db_file))
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM employees WHERE employee_id = ?", ("E201",))
    count = cursor.fetchone()[0]
    conn.close()

    assert count == 1
