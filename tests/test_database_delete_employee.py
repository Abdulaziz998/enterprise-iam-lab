from app.database import Database
from app.models import Employee


def test_delete_employee_successfully(tmp_path):
    db_file = tmp_path / "iam.db"
    db = Database(db_path=str(db_file))
    db.initialize()

    employee = Employee(
        employee_id="D001",
        first_name="Laura",
        last_name="King",
        department="Engineering",
        job_title="Software Developer",
        manager="D010",
        username="laura.king",
    )
    db.insert_employee(employee)

    result = db.delete_employee("D001")

    assert result["success"] is True
    assert result["message"] == "Employee deleted successfully."


def test_deleted_employee_cannot_be_retrieved(tmp_path):
    db_file = tmp_path / "iam.db"
    db = Database(db_path=str(db_file))
    db.initialize()

    employee = Employee(
        employee_id="D002",
        first_name="Mia",
        last_name="Reid",
        department="HR",
        job_title="HR Specialist",
        manager="D020",
        username="mia.reid",
    )
    db.insert_employee(employee)
    db.delete_employee("D002")

    result = db.get_employee_by_id("D002")
    assert result is None


def test_delete_missing_employee_returns_failure(tmp_path):
    db_file = tmp_path / "iam.db"
    db = Database(db_path=str(db_file))
    db.initialize()

    result = db.delete_employee("MISSING")

    assert result["success"] is False
    assert result["message"] == "Employee not found."


def test_delete_one_employee_does_not_delete_another(tmp_path):
    db_file = tmp_path / "iam.db"
    db = Database(db_path=str(db_file))
    db.initialize()

    emp1 = Employee(
        employee_id="D003",
        first_name="Noah",
        last_name="Lee",
        department="Support",
        job_title="Help Desk Analyst",
        manager="D030",
        username="noah.lee",
    )
    emp2 = Employee(
        employee_id="D004",
        first_name="Olivia",
        last_name="Park",
        department="Finance",
        job_title="Finance Analyst",
        manager="D040",
        username="olivia.park",
    )
    db.insert_employee(emp1)
    db.insert_employee(emp2)

    db.delete_employee("D003")

    remaining = db.get_employee_by_id("D004")
    assert remaining is not None
    assert remaining["employee_id"] == "D004"
    assert remaining["first_name"] == "Olivia"


def test_employees_table_still_works_after_deletion(tmp_path):
    db_file = tmp_path / "iam.db"
    db = Database(db_path=str(db_file))
    db.initialize()

    employee = Employee(
        employee_id="D005",
        first_name="Peter",
        last_name="Kim",
        department="Operations",
        job_title="Operations Manager",
        manager="D050",
        username="peter.kim",
    )
    db.insert_employee(employee)
    db.delete_employee("D005")

    # Insert another employee after deletion to ensure table is still usable
    employee2 = Employee(
        employee_id="D006",
        first_name="Quinn",
        last_name="Wang",
        department="IT",
        job_title="Software Developer",
        manager="D060",
        username="quinn.wang",
    )
    insert_result = db.insert_employee(employee2)

    assert insert_result["success"] is True
    assert db.get_employee_by_id("D006") is not None
