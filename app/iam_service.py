import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.models import Employee


class IAMService:
    """Simple IAM service for employee Joiner workflow."""

    def __init__(
        self,
        employees_path: Optional[str] = None,
        roles_path: Optional[str] = None,
    ):
        repo_root = Path(__file__).resolve().parents[1]
        self.employees_path = Path(employees_path) if employees_path else repo_root / "data" / "employees.json"
        self.roles_path = Path(roles_path) if roles_path else repo_root / "data" / "roles.json"

    def create_employee(self, employee: Employee) -> Dict[str, Any]:
        """Create a new employee record for the Joiner workflow."""
        missing_fields = self._validate_required_fields(employee)
        if missing_fields:
            return {
                "success": False,
                "message": f"Missing required fields: {', '.join(missing_fields)}",
            }

        employees = self._load_employees()
        if self._employee_id_exists(employee.employee_id, employees):
            return {
                "success": False,
                "message": f"Employee ID '{employee.employee_id}' already exists.",
            }

        roles = self._load_roles()
        role_data = roles.get(employee.job_title)
        if role_data is None:
            return {
                "success": False,
                "message": f"Invalid job title '{employee.job_title}'.",
            }

        employee.groups = list(role_data.get("groups", []))
        employee.applications = list(role_data.get("applications", []))
        employee.username = self._generate_username(employee, employees)

        employees.append(employee.to_dict())
        self._save_employees(employees)

        return {
            "success": True,
            "message": f"Employee '{employee.employee_id}' created successfully.",
            "employee": employee,
        }

    def _validate_required_fields(self, employee: Employee) -> List[str]:
        """Return a list of missing required fields for the employee."""
        missing = []
        if not employee.employee_id or not str(employee.employee_id).strip():
            missing.append("employee_id")
        if not employee.first_name or not employee.first_name.strip():
            missing.append("first_name")
        if not employee.last_name or not employee.last_name.strip():
            missing.append("last_name")
        if not employee.department or not employee.department.strip():
            missing.append("department")
        if not employee.job_title or not employee.job_title.strip():
            missing.append("job_title")
        return missing

    def _employee_id_exists(self, employee_id: str, employees: List[Dict[str, Any]]) -> bool:
        """Check whether an employee ID already exists in the employee store."""
        return any(emp.get("employee_id") == employee_id for emp in employees)

    def _load_employees(self) -> List[Dict[str, Any]]:
        """Load the employee list from the JSON file."""
        if not self.employees_path.exists():
            return []

        with self.employees_path.open("r", encoding="utf-8") as handle:
            try:
                data = json.load(handle)
            except json.JSONDecodeError:
                return []

        return data if isinstance(data, list) else []

    def _save_employees(self, employees: List[Dict[str, Any]]) -> None:
        """Save the employee list back to the JSON file."""
        self.employees_path.parent.mkdir(parents=True, exist_ok=True)
        with self.employees_path.open("w", encoding="utf-8") as handle:
            json.dump(employees, handle, indent=2)

    def _load_roles(self) -> Dict[str, Any]:
        """Load role definitions from the roles JSON file."""
        if not self.roles_path.exists():
            return {}

        with self.roles_path.open("r", encoding="utf-8") as handle:
            try:
                return json.load(handle)
            except json.JSONDecodeError:
                return {}

    def _generate_username(self, employee: Employee, employees: List[Dict[str, Any]]) -> str:
        """Create a username from first and last name, avoiding duplicates."""
        base = self._normalize_username(f"{employee.first_name}.{employee.last_name}")
        existing_usernames = {emp.get("username") for emp in employees if emp.get("username")}
        username = base
        suffix = 2
        while username in existing_usernames:
            username = f"{base}{suffix}"
            suffix += 1
        return username

    def _normalize_username(self, raw_username: str) -> str:
        """Normalize names to a lowercase username with dots."""
        normalized = raw_username.strip().lower()
        normalized = re.sub(r"[^a-z0-9.]+", "", normalized)
        normalized = re.sub(r"\.{2,}", ".", normalized)
        return normalized

    def update_employee_role(self, employee_id: str, new_job_title: str) -> Dict[str, Any]:
        """Update an existing employee's role (Mover workflow).

        This updates `job_title`, `groups`, and `applications` while preserving
        `employee_id`, `username`, `manager`, and `department`.
        """
        employees = self._load_employees()

        # Find employee record
        target = None
        for emp in employees:
            if emp.get("employee_id") == employee_id:
                target = emp
                break

        if target is None:
            return {"success": False, "message": f"Employee ID '{employee_id}' not found."}

        roles = self._load_roles()
        role_data = roles.get(new_job_title)
        if role_data is None:
            return {"success": False, "message": f"Invalid job title '{new_job_title}'."}

        # Update the mutable fields according to the new role
        target["job_title"] = new_job_title
        target["groups"] = list(role_data.get("groups", []))
        target["applications"] = list(role_data.get("applications", []))

        # Persist changes
        self._save_employees(employees)

        # Return an Employee object for convenience
        updated_employee = Employee.from_dict(target)

        return {
            "success": True,
            "message": f"Employee '{employee_id}' role updated to '{new_job_title}'.",
            "employee": updated_employee,
        }
