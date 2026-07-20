from fastapi.testclient import TestClient

from app import main
from app.database import Database
from app.models import Employee


def setup_temp_database(tmp_path):
    db_file = tmp_path / "iam.db"
    new_database = Database(db_path=str(db_file))
    return new_database


def test_update_employee_successful(tmp_path):
    new_database = setup_temp_database(tmp_path)
    main.database = new_database

    original_employee = Employee(
        employee_id="UP001",
        first_name="John",
        last_name="Doe",
        department="IT",
        job_title="Help Desk Analyst",
        manager="UP010",
        username="john.doe",
    )
    new_database.insert_employee(original_employee)

    update_body = Employee(
        employee_id="UP001",
        first_name="Jonathan",
        last_name="Smith",
        department="Engineering",
        job_title="Software Developer",
        manager="UP020",
        status="active",
        username="jonathan.smith",
    )

    client = TestClient(main.app)
    response = client.put("/employees/UP001", json=update_body.to_dict())

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Employee updated successfully."


def test_update_employee_all_fields_updated(tmp_path):
    new_database = setup_temp_database(tmp_path)
    main.database = new_database

    original = Employee(
        employee_id="UP002",
        first_name="Alice",
        last_name="Johnson",
        department="HR",
        job_title="HR Specialist",
        manager="UP030",
        username="alice.johnson",
    )
    new_database.insert_employee(original)

    update_body = Employee(
        employee_id="UP002",
        first_name="Alicia",
        last_name="Williams",
        department="Finance",
        job_title="Finance Analyst",
        manager="UP040",
        status="active",
        username="alicia.williams",
    )

    client = TestClient(main.app)
    response = client.put("/employees/UP002", json=update_body.to_dict())

    assert response.status_code == 200
    data = response.json()
    assert data["employee"]["first_name"] == "Alicia"
    assert data["employee"]["last_name"] == "Williams"
    assert data["employee"]["department"] == "Finance"
    assert data["employee"]["job_title"] == "Finance Analyst"
    assert data["employee"]["manager"] == "UP040"
    assert data["employee"]["username"] == "alicia.williams"


def test_update_employee_preserves_employee_id(tmp_path):
    new_database = setup_temp_database(tmp_path)
    main.database = new_database

    original = Employee(
        employee_id="UP003",
        first_name="Bob",
        last_name="Brown",
        department="Support",
        job_title="Help Desk Analyst",
        manager="UP050",
        username="bob.brown",
    )
    new_database.insert_employee(original)

    update_body = Employee(
        employee_id="UP003",
        first_name="Robert",
        last_name="Blue",
        department="Operations",
        job_title="Operations Manager",
        manager="UP060",
        status="active",
        username="robert.blue",
    )

    client = TestClient(main.app)
    response = client.put("/employees/UP003", json=update_body.to_dict())

    assert response.status_code == 200
    data = response.json()
    assert data["employee"]["employee_id"] == "UP003"


def test_update_employee_url_id_overrides_body_id(tmp_path):
    new_database = setup_temp_database(tmp_path)
    main.database = new_database

    original = Employee(
        employee_id="UP004",
        first_name="Carol",
        last_name="Davis",
        department="IT",
        job_title="Help Desk Analyst",
        manager="UP070",
        username="carol.davis",
    )
    new_database.insert_employee(original)

    # Request body has different employee_id, but URL is authoritative
    update_body = Employee(
        employee_id="DIFFERENT_ID",
        first_name="Caroline",
        last_name="Green",
        department="Engineering",
        job_title="Software Developer",
        manager="UP080",
        status="active",
        username="caroline.green",
    )

    client = TestClient(main.app)
    response = client.put("/employees/UP004", json=update_body.to_dict())

    assert response.status_code == 200
    data = response.json()
    assert data["employee"]["employee_id"] == "UP004"
    assert data["employee"]["first_name"] == "Caroline"


def test_update_employee_not_found(tmp_path):
    new_database = setup_temp_database(tmp_path)
    main.database = new_database

    update_body = Employee(
        employee_id="NOTFOUND",
        first_name="Test",
        last_name="User",
        department="IT",
        job_title="Test",
        manager="M010",
        username="test.user",
    )

    client = TestClient(main.app)
    response = client.put("/employees/NOTFOUND", json=update_body.to_dict())

    assert response.status_code == 404
    data = response.json()
    assert data["success"] is False
    assert data["message"] == "Employee not found."


def test_update_employee_persists_to_sqlite(tmp_path):
    new_database = setup_temp_database(tmp_path)
    main.database = new_database

    original = Employee(
        employee_id="UP005",
        first_name="David",
        last_name="Evans",
        department="HR",
        job_title="HR Specialist",
        manager="UP090",
        username="david.evans",
    )
    new_database.insert_employee(original)

    update_body = Employee(
        employee_id="UP005",
        first_name="Dave",
        last_name="Foster",
        department="Finance",
        job_title="Finance Director",
        manager="UP100",
        status="active",
        username="dave.foster",
    )

    client = TestClient(main.app)
    response = client.put("/employees/UP005", json=update_body.to_dict())

    assert response.status_code == 200

    # Verify persisted in SQLite by querying directly
    persisted = new_database.get_employee_by_id("UP005")
    assert persisted is not None
    assert persisted["first_name"] == "Dave"
    assert persisted["last_name"] == "Foster"
    assert persisted["department"] == "Finance"


def test_update_employee_does_not_affect_other_employees(tmp_path):
    new_database = setup_temp_database(tmp_path)
    main.database = new_database

    emp1 = Employee(
        employee_id="UP200",
        first_name="Employee1",
        last_name="One",
        department="IT",
        job_title="Help Desk Analyst",
        manager="M010",
        username="emp1.one",
    )
    emp2 = Employee(
        employee_id="UP201",
        first_name="Employee2",
        last_name="Two",
        department="HR",
        job_title="HR Specialist",
        manager="M020",
        username="emp2.two",
    )
    new_database.insert_employee(emp1)
    new_database.insert_employee(emp2)

    update_body = Employee(
        employee_id="UP200",
        first_name="UpdatedEmp1",
        last_name="Updated",
        department="Finance",
        job_title="Finance Analyst",
        manager="M030",
        status="active",
        username="updated.emp1",
    )

    client = TestClient(main.app)
    response = client.put("/employees/UP200", json=update_body.to_dict())

    assert response.status_code == 200

    emp1_after = new_database.get_employee_by_id("UP200")
    emp2_after = new_database.get_employee_by_id("UP201")

    assert emp1_after["first_name"] == "UpdatedEmp1"
    assert emp2_after["first_name"] == "Employee2"
    assert emp2_after["last_name"] == "Two"
