from pathlib import Path

from fastapi.testclient import TestClient

from app.database import Database
from app.iam_service import IAMService
from app.main import app
from app.models import Employee


def test_get_employees_returns_200(tmp_path):
    employees_file = tmp_path / "employees.json"
    audit_file = tmp_path / "audit_log.json"
    db_file = tmp_path / "iam.db"

    # Create new app and client for this test
    from fastapi import FastAPI

    test_app = FastAPI()
    service = IAMService(
        employees_path=str(employees_file),
        roles_path=str(Path(__file__).resolve().parents[1] / "data" / "roles.json"),
        audit_log_path=str(audit_file),
        db_path=str(db_file),
    )
    database = Database(db_path=str(db_file))

    @test_app.get("/employees")
    def get_employees():
        employees = database.get_all_employees()
        return {
            "success": True,
            "count": len(employees),
            "employees": employees,
        }

    client = TestClient(test_app)
    response = client.get("/employees")

    assert response.status_code == 200


def test_get_employees_empty_database(tmp_path):
    employees_file = tmp_path / "employees.json"
    audit_file = tmp_path / "audit_log.json"
    db_file = tmp_path / "iam.db"

    from fastapi import FastAPI

    test_app = FastAPI()
    service = IAMService(
        employees_path=str(employees_file),
        roles_path=str(Path(__file__).resolve().parents[1] / "data" / "roles.json"),
        audit_log_path=str(audit_file),
        db_path=str(db_file),
    )
    database = Database(db_path=str(db_file))

    @test_app.get("/employees")
    def get_employees():
        employees = database.get_all_employees()
        return {
            "success": True,
            "count": len(employees),
            "employees": employees,
        }

    client = TestClient(test_app)
    response = client.get("/employees")

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["count"] == 0
    assert data["employees"] == []


def test_get_employees_single_employee(tmp_path):
    employees_file = tmp_path / "employees.json"
    audit_file = tmp_path / "audit_log.json"
    db_file = tmp_path / "iam.db"

    from fastapi import FastAPI

    test_app = FastAPI()
    service = IAMService(
        employees_path=str(employees_file),
        roles_path=str(Path(__file__).resolve().parents[1] / "data" / "roles.json"),
        audit_log_path=str(audit_file),
        db_path=str(db_file),
    )
    database = Database(db_path=str(db_file))

    @test_app.get("/employees")
    def get_employees():
        employees = database.get_all_employees()
        return {
            "success": True,
            "count": len(employees),
            "employees": employees,
        }

    employee = Employee(
        employee_id="API001",
        first_name="Frank",
        last_name="Wilson",
        department="IT",
        job_title="Help Desk Analyst",
        manager="API010",
    )
    service.create_employee(employee)

    client = TestClient(test_app)
    response = client.get("/employees")

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["count"] == 1
    assert len(data["employees"]) == 1
    assert data["employees"][0]["employee_id"] == "API001"
    assert data["employees"][0]["first_name"] == "Frank"
    assert data["employees"][0]["last_name"] == "Wilson"


def test_get_employees_multiple_employees(tmp_path):
    employees_file = tmp_path / "employees.json"
    audit_file = tmp_path / "audit_log.json"
    db_file = tmp_path / "iam.db"

    from fastapi import FastAPI

    test_app = FastAPI()
    service = IAMService(
        employees_path=str(employees_file),
        roles_path=str(Path(__file__).resolve().parents[1] / "data" / "roles.json"),
        audit_log_path=str(audit_file),
        db_path=str(db_file),
    )
    database = Database(db_path=str(db_file))

    @test_app.get("/employees")
    def get_employees():
        employees = database.get_all_employees()
        return {
            "success": True,
            "count": len(employees),
            "employees": employees,
        }

    emp1 = Employee(
        employee_id="API002",
        first_name="Grace",
        last_name="Lee",
        department="Finance",
        job_title="Finance Analyst",
        manager="API020",
    )
    emp2 = Employee(
        employee_id="API003",
        first_name="Henry",
        last_name="Martinez",
        department="HR",
        job_title="HR Specialist",
        manager="API030",
    )
    emp3 = Employee(
        employee_id="API001",
        first_name="Iris",
        last_name="Johnson",
        department="Engineering",
        job_title="Software Developer",
        manager="API040",
    )

    service.create_employee(emp1)
    service.create_employee(emp2)
    service.create_employee(emp3)

    client = TestClient(test_app)
    response = client.get("/employees")

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["count"] == 3
    assert len(data["employees"]) == 3


def test_get_employees_count_matches_records(tmp_path):
    employees_file = tmp_path / "employees.json"
    audit_file = tmp_path / "audit_log.json"
    db_file = tmp_path / "iam.db"

    from fastapi import FastAPI

    test_app = FastAPI()
    service = IAMService(
        employees_path=str(employees_file),
        roles_path=str(Path(__file__).resolve().parents[1] / "data" / "roles.json"),
        audit_log_path=str(audit_file),
        db_path=str(db_file),
    )
    database = Database(db_path=str(db_file))

    @test_app.get("/employees")
    def get_employees():
        employees = database.get_all_employees()
        return {
            "success": True,
            "count": len(employees),
            "employees": employees,
        }

    for i in range(5):
        employee = Employee(
            employee_id=f"API{i:03d}",
            first_name=f"Employee{i}",
            last_name="Test",
            department="Test",
            job_title="Help Desk Analyst",
            manager="API999",
        )
        service.create_employee(employee)

    client = TestClient(test_app)
    response = client.get("/employees")

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["count"] == 5
    assert len(data["employees"]) == 5
    assert data["count"] == len(data["employees"])
