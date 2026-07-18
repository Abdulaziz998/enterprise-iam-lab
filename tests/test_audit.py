import json
from pathlib import Path

from app.audit import AuditLogger
from app.iam_service import IAMService
from app.models import Employee


def test_audit_log_successful_create(tmp_path):
    audit_file = tmp_path / "audit_log.json"
    employees_file = tmp_path / "employees.json"
    service = IAMService(
        employees_path=str(employees_file),
        roles_path=str(Path(__file__).resolve().parents[1] / "data" / "roles.json"),
        audit_log_path=str(audit_file),
    )

    emp = Employee(
        employee_id="A001",
        first_name="Alice",
        last_name="Brown",
        department="IT",
        job_title="Help Desk Analyst",
        manager="A010",
    )

    service.create_employee(emp)

    logs = json.loads(audit_file.read_text(encoding="utf-8"))
    assert len(logs) > 0

    create_log = logs[-1]
    assert create_log["action"] == "CREATE"
    assert create_log["employee_id"] == "A001"
    assert create_log["status"] == "SUCCESS"
    assert "username" in create_log["details"]
    assert "timestamp" in create_log
    assert create_log["timestamp"].endswith("Z")


def test_audit_log_successful_role_update(tmp_path):
    audit_file = tmp_path / "audit_log.json"
    employees_file = tmp_path / "employees.json"
    service = IAMService(
        employees_path=str(employees_file),
        roles_path=str(Path(__file__).resolve().parents[1] / "data" / "roles.json"),
        audit_log_path=str(audit_file),
    )

    emp = Employee(
        employee_id="A002",
        first_name="Bob",
        last_name="Green",
        department="IT",
        job_title="Help Desk Analyst",
        manager="A010",
    )
    service.create_employee(emp)

    service.update_employee_role("A002", "IAM Analyst")

    logs = json.loads(audit_file.read_text(encoding="utf-8"))
    update_log = None
    for log in logs:
        if log["action"] == "UPDATE_ROLE":
            update_log = log
            break

    assert update_log is not None
    assert update_log["employee_id"] == "A002"
    assert update_log["status"] == "SUCCESS"
    assert update_log["details"]["old_job_title"] == "Help Desk Analyst"
    assert update_log["details"]["new_job_title"] == "IAM Analyst"
    assert "timestamp" in update_log


def test_audit_log_successful_termination(tmp_path):
    audit_file = tmp_path / "audit_log.json"
    employees_file = tmp_path / "employees.json"
    service = IAMService(
        employees_path=str(employees_file),
        roles_path=str(Path(__file__).resolve().parents[1] / "data" / "roles.json"),
        audit_log_path=str(audit_file),
    )

    emp = Employee(
        employee_id="A003",
        first_name="Charlie",
        last_name="White",
        department="HR",
        job_title="HR Specialist",
        manager="A011",
    )
    service.create_employee(emp)

    service.terminate_employee("A003")

    logs = json.loads(audit_file.read_text(encoding="utf-8"))
    terminate_log = None
    for log in logs:
        if log["action"] == "TERMINATE":
            terminate_log = log
            break

    assert terminate_log is not None
    assert terminate_log["employee_id"] == "A003"
    assert terminate_log["status"] == "SUCCESS"
    assert "job_title" in terminate_log["details"]
    assert "timestamp" in terminate_log


def test_audit_log_failed_operation(tmp_path):
    audit_file = tmp_path / "audit_log.json"
    employees_file = tmp_path / "employees.json"
    service = IAMService(
        employees_path=str(employees_file),
        roles_path=str(Path(__file__).resolve().parents[1] / "data" / "roles.json"),
        audit_log_path=str(audit_file),
    )

    # Try to create an employee with invalid job title
    emp = Employee(
        employee_id="A004",
        first_name="Diana",
        last_name="Black",
        department="Legal",
        job_title="Non-existent Role",
        manager="A012",
    )

    service.create_employee(emp)

    logs = json.loads(audit_file.read_text(encoding="utf-8"))
    failed_log = None
    for log in logs:
        if log["action"] == "CREATE" and log["status"] == "FAILED":
            failed_log = log
            break

    assert failed_log is not None
    assert failed_log["employee_id"] == "A004"
    assert "reason" in failed_log["details"]
    assert "Invalid job title" in failed_log["details"]["reason"]


def test_audit_log_timestamp_format(tmp_path):
    audit_file = tmp_path / "audit_log.json"
    logger = AuditLogger(str(audit_file))

    logger.log_event(
        action="TEST",
        employee_id="TEST001",
        status="SUCCESS",
        details={"test": "data"},
    )

    logs = json.loads(audit_file.read_text(encoding="utf-8"))
    log = logs[0]

    assert "timestamp" in log
    assert log["timestamp"].endswith("Z")
    # Verify ISO format: YYYY-MM-DDTHH:MM:SS.ffffffZ
    assert "T" in log["timestamp"]
    assert log["timestamp"].count("-") >= 2  # At least date separators


def test_audit_log_valid_json(tmp_path):
    audit_file = tmp_path / "audit_log.json"
    service = IAMService(
        employees_path=str(tmp_path / "employees.json"),
        roles_path=str(Path(__file__).resolve().parents[1] / "data" / "roles.json"),
        audit_log_path=str(audit_file),
    )

    emp = Employee(
        employee_id="A005",
        first_name="Eve",
        last_name="Red",
        department="Finance",
        job_title="Finance Analyst",
        manager="A013",
    )
    service.create_employee(emp)

    # Try to parse the audit log as JSON
    with audit_file.open("r", encoding="utf-8") as handle:
        logs = json.load(handle)

    assert isinstance(logs, list)
    assert len(logs) > 0
    for log in logs:
        assert "timestamp" in log
        assert "action" in log
        assert "employee_id" in log
        assert "status" in log
        assert "details" in log
