from fastapi.testclient import TestClient

from app import main
from app.database import Database
from app.models import Employee


def setup_temp_database(tmp_path):
    db_file = tmp_path / "iam.db"
    return Database(db_path=str(db_file))


def test_delete_employee_successfully(tmp_path):
    new_database = setup_temp_database(tmp_path)
    main.database = new_database

    employee = Employee(
        employee_id="DEL001",
        first_name="Ava",
        last_name="Long",
        department="Engineering",
        job_title="Software Developer",
        manager="DEL010",
        username="ava.long",
    )
    new_database.insert_employee(employee)

    client = TestClient(main.app)
    response = client.delete("/employees/DEL001")

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Employee deleted successfully."


def test_deleted_employee_can_no_longer_be_retrieved(tmp_path):
    new_database = setup_temp_database(tmp_path)
    main.database = new_database

    employee = Employee(
        employee_id="DEL002",
        first_name="Ben",
        last_name="Moore",
        department="HR",
        job_title="HR Specialist",
        manager="DEL020",
        username="ben.moore",
    )
    new_database.insert_employee(employee)

    client = TestClient(main.app)
    delete_response = client.delete("/employees/DEL002")
    assert delete_response.status_code == 200

    get_response = client.get("/employees/DEL002")
    assert get_response.status_code == 404
    get_data = get_response.json()
    assert get_data["success"] is False
    assert get_data["message"] == "Employee not found."


def test_delete_one_employee_does_not_delete_another(tmp_path):
    new_database = setup_temp_database(tmp_path)
    main.database = new_database

    employee1 = Employee(
        employee_id="DEL003",
        first_name="Cleo",
        last_name="Parks",
        department="Support",
        job_title="Help Desk Analyst",
        manager="DEL030",
        username="cleo.parks",
    )
    employee2 = Employee(
        employee_id="DEL004",
        first_name="Dylan",
        last_name="Scott",
        department="Finance",
        job_title="Finance Analyst",
        manager="DEL040",
        username="dylan.scott",
    )
    new_database.insert_employee(employee1)
    new_database.insert_employee(employee2)

    client = TestClient(main.app)
    delete_response = client.delete("/employees/DEL003")

    assert delete_response.status_code == 200
    remaining_response = client.get("/employees/DEL004")
    assert remaining_response.status_code == 200
    remaining_data = remaining_response.json()
    assert remaining_data["success"] is True
    assert remaining_data["employee"]["employee_id"] == "DEL004"


def test_delete_missing_employee_returns_404(tmp_path):
    new_database = setup_temp_database(tmp_path)
    main.database = new_database

    client = TestClient(main.app)
    response = client.delete("/employees/NOTFOUND")

    assert response.status_code == 404
    data = response.json()
    assert data["success"] is False
    assert data["message"] == "Employee not found."
