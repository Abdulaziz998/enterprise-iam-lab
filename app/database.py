import sqlite3
from pathlib import Path
from typing import Optional

from app.models import Employee


class Database:
    """Simple SQLite database helper for the IAM lifecycle lab."""

    def __init__(self, db_path: Optional[str] = None):
        repo_root = Path(__file__).resolve().parents[1]
        self.db_path = Path(db_path) if db_path else repo_root / "data" / "iam.db"
        self.connection: Optional[sqlite3.Connection] = None

    def connect(self) -> sqlite3.Connection:
        """Open a connection to the SQLite database."""
        self.connection = sqlite3.connect(str(self.db_path))
        return self.connection

    def close(self) -> None:
        """Close the currently open database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None

    def initialize(self) -> None:
        """Create the SQLite database and the employees table."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS employees (
                employee_id TEXT PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                department TEXT,
                job_title TEXT,
                manager TEXT,
                status TEXT,
                username TEXT
            )
            """
        )
        conn.commit()
        self.close()

    def insert_employee(self, employee: Employee) -> dict:
        """Insert one Employee into the employees table."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS employees (
                employee_id TEXT PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                department TEXT,
                job_title TEXT,
                manager TEXT,
                status TEXT,
                username TEXT
            )
            """
        )

        try:
            cursor.execute(
                """
                INSERT INTO employees (
                    employee_id,
                    first_name,
                    last_name,
                    department,
                    job_title,
                    manager,
                    status,
                    username
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    employee.employee_id,
                    employee.first_name,
                    employee.last_name,
                    employee.department,
                    employee.job_title,
                    employee.manager,
                    employee.status,
                    employee.username,
                ),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            self.close()
            return {
                "success": False,
                "message": f"Employee ID '{employee.employee_id}' already exists.",
            }
        finally:
            self.close()

        return {
            "success": True,
            "message": f"Employee '{employee.employee_id}' inserted successfully.",
        }

    def update_employee_role(self, employee_id: str, new_job_title: str, new_status: str, new_username: str) -> dict:
        """Update employee role fields in the SQLite employees table."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS employees (
                employee_id TEXT PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                department TEXT,
                job_title TEXT,
                manager TEXT,
                status TEXT,
                username TEXT
            )
            """
        )

        cursor.execute(
            "SELECT employee_id FROM employees WHERE employee_id = ?",
            (employee_id,),
        )
        if cursor.fetchone() is None:
            self.close()
            return {"success": False, "message": f"Employee ID '{employee_id}' not found."}

        cursor.execute(
            """
            UPDATE employees
            SET job_title = ?, status = ?, username = ?
            WHERE employee_id = ?
            """,
            (new_job_title, new_status, new_username, employee_id),
        )
        conn.commit()
        self.close()

        return {"success": True, "message": f"Employee '{employee_id}' updated successfully."}
