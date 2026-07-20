import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class AuditLogger:
    """Simple audit logger for IAM lifecycle events."""

    def __init__(self, audit_log_path: Optional[str] = None):
        """Initialize the audit logger with a path to the audit log file."""
        repo_root = Path(__file__).resolve().parents[1]
        self.audit_log_path = Path(audit_log_path) if audit_log_path else repo_root / "data" / "audit_log.json"

    def log_event(
        self,
        action: str,
        employee_id: str,
        status: str,
        details: Dict[str, Any],
    ) -> None:
        """Log an audit event to the audit log file.

        Args:
            action: The type of operation (e.g., "CREATE", "UPDATE_ROLE", "TERMINATE").
            employee_id: The employee ID involved in the action.
            status: The result status ("SUCCESS" or "FAILED").
            details: A dict with additional context (error message, old/new values, etc.).
        """
        timestamp = datetime.utcnow().isoformat() + "Z"

        event = {
            "timestamp": timestamp,
            "action": action,
            "employee_id": employee_id,
            "status": status,
            "details": details,
        }

        logs = self._load_audit_log()
        logs.append(event)
        self._save_audit_log(logs)

    def _load_audit_log(self) -> List[Dict[str, Any]]:
        """Load existing audit events from the log file."""
        if not self.audit_log_path.exists():
            return []

        with self.audit_log_path.open("r", encoding="utf-8") as handle:
            try:
                data = json.load(handle)
            except json.JSONDecodeError:
                return []

        return data if isinstance(data, list) else []

    def get_events(self) -> List[Dict[str, Any]]:
        """Load audit events from the configured audit log."""
        return self._load_audit_log()

    def _save_audit_log(self, logs: List[Dict[str, Any]]) -> None:
        """Save audit logs back to the JSON file."""
        self.audit_log_path.parent.mkdir(parents=True, exist_ok=True)
        with self.audit_log_path.open("w", encoding="utf-8") as handle:
            json.dump(logs, handle, indent=2)
