import json
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app, service


def test_audit_logs_empty_returns_zero(tmp_path):
    service.audit_logger.audit_log_path = tmp_path / "audit_log.json"

    client = TestClient(app)
    response = client.get("/audit-logs")

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["count"] == 0
    assert data["events"] == []


def test_audit_logs_return_events_and_support_filters(tmp_path):
    audit_file = tmp_path / "audit_log.json"
    service.audit_logger.audit_log_path = audit_file

    events = [
        {
            "timestamp": "2026-07-19T12:00:00Z",
            "action": "create",
            "employee_id": "100001",
            "status": "failed",
            "details": {"reason": "policy violation"},
        },
        {
            "timestamp": "2026-07-19T12:05:00Z",
            "action": "UPDATE_ROLE",
            "employee_id": "100002",
            "status": "SUCCESS",
            "details": {"old_role": "HR Specialist", "new_role": "IAM Analyst"},
        },
    ]

    audit_file.write_text(json.dumps(events), encoding="utf-8")

    client = TestClient(app)
    response = client.get("/audit-logs")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["count"] == 2
    assert data["events"] == events

    response = client.get("/audit-logs?action=CREATE")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 1
    assert data["events"][0]["action"] == "create"

    response = client.get("/audit-logs?status=FAILED")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 1
    assert data["events"][0]["status"] == "failed"

    response = client.get("/audit-logs?employee_id=100001")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 1
    assert data["events"][0]["employee_id"] == "100001"


def test_audit_logs_invalid_file_returns_empty_list(tmp_path):
    audit_file = tmp_path / "audit_log.json"
    audit_file.write_text("not a valid json", encoding="utf-8")
    service.audit_logger.audit_log_path = audit_file

    client = TestClient(app)
    response = client.get("/audit-logs")

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["count"] == 0
    assert data["events"] == []
