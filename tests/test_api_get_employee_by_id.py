from fastapi.testclient import TestClient

from app import main
from app.database import Database
from app.models import Employee


def setup_temp_database(tmp_path):
    db_file = tmp_path / "iam.db"
    new_database = Database(db_path=str(db_file))
    return new_database


def test_get_employee_by_id_existing_employee_returns_200(tmp_path):
    new_database = setup_temp_database(tmp_path)
    main.database = new_database
    new_database.insert_employee(
        Employee(
            employee_id="E500",
            first_name="Dana",
            last_name="Hughes",
            department="Engineering",
            job_title="Software Developer",
            manager="E010",
            username="dana.hughes",
        )
    )

    client = TestClient(main.app)
    response = client.get("/employees/E500")

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["employee"]["employee_id"] == "E500"
    assert data["employee"]["first_name"] == "Dana"
    assert data["employee"]["last_name"] == "Hughes"
    assert data["employee"]["department"] == "Engineering"
    assert data["employee"]["job_title"] == "Software Developer"
    assert data["employee"]["manager"] == "E010"
    assert data["employee"]["status"] == "active"
    assert data["employee"]["username"] == "dana.hughes"


def test_get_employee_by_id_contains_all_fields(tmp_path):
    new_database = setup_temp_database(tmp_path)
    main.database = new_database
    new_database.insert_employee(
        Employee(
            employee_id="E501",
            first_name="Erin",
            last_name="Cole",
            department="Finance",
            job_title="Finance Analyst",
            manager="E020",
            status="terminated",
            username="erin.cole",
        )
    )

    client = TestClient(main.app)
    response = client.get("/employees/E501")

    assert response.status_code == 200
    data = response.json()
    assert set(data["employee"].keys()) == {
        "employee_id",
        "first_name",
        "last_name",
        "department",
        "job_title",
        "manager",
        "status",
        "username",
        "groups",
        "applications",
    }


def test_get_employee_by_id_missing_employee_returns_404(tmp_path):
    new_database = setup_temp_database(tmp_path)
    main.database = new_database

    client = TestClient(main.app)
    response = client.get("/employees/NOTFOUND")

    assert response.status_code == 404
    data = response.json()
    assert data["success"] is False
    assert data["message"] == "Employee not found."


def test_get_employee_by_id_exact_match_with_multiple_records(tmp_path):
    new_database = setup_temp_database(tmp_path)
    main.database = new_database
    employees = [
        Employee(
            employee_id="E502",
            first_name="Finn",
            last_name="Morgan",
            department="Support",
            job_title="Help Desk Analyst",
            manager="E030",
            username="finn.morgan",
        ),
        Employee(
            employee_id="E503",
            first_name="Gina",
            last_name="Reed",
            department="HR",
            job_title="HR Specialist",
            manager="E040",
            username="gina.reed",
        ),
    ]
    for employee in employees:
        new_database.insert_employee(employee)

    client = TestClient(main.app)
    response = client.get("/employees/E503")

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["employee"]["employee_id"] == "E503"
    assert data["employee"]["first_name"] == "Gina"
    assert data["employee"]["last_name"] == "Reed"


def test_created_employee_detail_includes_role_groups_and_applications(tmp_path):
    from pathlib import Path

    from app.iam_service import IAMService

    original_service = main.service
    original_database = main.database
    test_service = IAMService(
        employees_path=str(tmp_path / "employees.json"),
        roles_path=str(Path(__file__).resolve().parents[1] / "data" / "roles.json"),
        audit_log_path=str(tmp_path / "audit_log.json"),
        db_path=str(tmp_path / "iam.db"),
    )
    main.service = test_service
    main.database = test_service.database

    client = TestClient(main.app)
    try:
        create_response = client.post(
            "/employees",
            json={
                "employee_id": "API-GROUPS-1",
                "first_name": "Harper",
                "last_name": "Stone",
                "department": "IT Support",
                "job_title": "Help Desk Analyst",
                "manager": "Nina Patel",
                "status": "active",
            },
        )
        assert create_response.status_code == 200

        detail_response = client.get("/employees/API-GROUPS-1")
        assert detail_response.status_code == 200
        employee = detail_response.json()["employee"]
        assert employee["groups"] == ["helpdesk"]
        assert employee["applications"] == ["ticketing_system"]
    finally:
        main.service = original_service
        main.database = original_database
