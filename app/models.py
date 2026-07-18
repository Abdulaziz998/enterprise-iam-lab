from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Employee:
    """Employee identity model for the IAM lifecycle lab."""

    employee_id: str
    first_name: str
    last_name: str
    department: str
    job_title: str
    manager: Optional[str]
    status: str = "active"
    username: Optional[str] = None
    groups: List[str] = field(default_factory=list)
    applications: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation of the Employee."""
        return {
            "employee_id": self.employee_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "department": self.department,
            "job_title": self.job_title,
            "manager": self.manager,
            "status": self.status,
            "username": self.username,
            "groups": list(self.groups),
            "applications": list(self.applications),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Employee":
        """Create an Employee object from a dictionary."""
        return cls(
            employee_id=data.get("employee_id", ""),
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
            department=data.get("department", ""),
            job_title=data.get("job_title", ""),
            manager=data.get("manager"),
            status=data.get("status", "active"),
            username=data.get("username"),
            groups=list(data.get("groups", [])),
            applications=list(data.get("applications", [])),
        )
