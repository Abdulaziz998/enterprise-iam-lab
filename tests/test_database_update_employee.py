from app.database import Database
from app.models import Employee


def test_update_employee_successfully(tmp_path):
    db_file = tmp_path / "iam.db"
    db = Database(db_path=str(db_file))
    db.initialize()

    employee = Employee(
        employee_id="U001",
        first_name="Original",
        last_name="Name",
        department="IT",
        job_title="Help Desk Analyst",
        manager="U010",
        username="original.name",
    )
    db.insert_employee(employee)

    result = db.update_employee(
        employee_id="U001",
        first_name="Updated",
        last_name="Person",
        department="Engineering",
        job_title="Software Developer",
        manager="U020",
        status="active",
        username="updated.person",
    )

    assert result["success"] is True
    assert "updated successfully" in result["message"]


def test_update_employee_preserves_employee_id(tmp_path):
    db_file = tmp_path / "iam.db"
    db = Database(db_path=str(db_file))
    db.initialize()

    employee = Employee(
        employee_id="U002",
        first_name="Alice",
        last_name="Smith",
        department="HR",
        job_title="HR Specialist",
        manager="U030",
        username="alice.smith",
    )
    db.insert_employee(employee)

    db.update_employee(
        employee_id="U002",
        first_name="Alicia",
        last_name="Jones",
        department="Finance",
        job_title="Finance Analyst",
        manager="U040",
        status="active",
        username="alicia.jones",
    )

    updated = db.get_employee_by_id("U002")
    assert updated is not None
    assert updated["employee_id"] == "U002"


def test_update_employee_all_fields_changed(tmp_path):
    db_file = tmp_path / "iam.db"
    db = Database(db_path=str(db_file))
    db.initialize()

    employee = Employee(
        employee_id="U003",
        first_name="Bob",
        last_name="Brown",
        department="Support",
        job_title="Help Desk Analyst",
        manager="U050",
        status="active",
        username="bob.brown",
    )
    db.insert_employee(employee)

    db.update_employee(
        employee_id="U003",
        first_name="Robert",
        last_name="Green",
        department="Operations",
        job_title="Operations Manager",
        manager="U060",
        status="terminated",
        username="robert.green",
    )

    updated = db.get_employee_by_id("U003")
    assert updated is not None
    assert updated["first_name"] == "Robert"
    assert updated["last_name"] == "Green"
    assert updated["department"] == "Operations"
    assert updated["job_title"] == "Operations Manager"
    assert updated["manager"] == "U060"
    assert updated["status"] == "terminated"
    assert updated["username"] == "robert.green"


def test_update_employee_not_found(tmp_path):
    db_file = tmp_path / "iam.db"
    db = Database(db_path=str(db_file))
    db.initialize()

    result = db.update_employee(
        employee_id="MISSING",
        first_name="Test",
        last_name="User",
        department="IT",
        job_title="Analyst",
        manager="M010",
        status="active",
        username="test.user",
    )

    assert result["success"] is False
    assert "not found" in result["message"]


def test_update_employee_does_not_affect_other_employees(tmp_path):
    db_file = tmp_path / "iam.db"
    db = Database(db_path=str(db_file))
    db.initialize()

    emp1 = Employee(
        employee_id="U100",
        first_name="Employee1",
        last_name="One",
        department="IT",
        job_title="Help Desk Analyst",
        manager="U010",
        username="emp1.one",
    )
    emp2 = Employee(
        employee_id="U101",
        first_name="Employee2",
        last_name="Two",
        department="HR",
        job_title="HR Specialist",
        manager="U020",
        username="emp2.two",
    )
    db.insert_employee(emp1)
    db.insert_employee(emp2)

    db.update_employee(
        employee_id="U100",
        first_name="UpdatedEmp1",
        last_name="Updated",
        department="Finance",
        job_title="Finance Analyst",
        manager="U030",
        status="active",
        username="updated.emp1",
    )

    emp1_after = db.get_employee_by_id("U100")
    emp2_after = db.get_employee_by_id("U101")

    assert emp1_after["first_name"] == "UpdatedEmp1"
    assert emp2_after["first_name"] == "Employee2"
    assert emp2_after["last_name"] == "Two"
