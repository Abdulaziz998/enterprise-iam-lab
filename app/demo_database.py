from app.database import Database
from app.models import Employee


def main():
    db = Database()
    db.initialize()

    employee = Employee(
        employee_id="200001",
        first_name="Abdulaziz",
        last_name="Abdi",
        department="Information Technology",
        job_title="Help Desk Analyst",
        manager="Sarah Johnson",
        status="active",
        username="abdulaziz.abdi",
    )

    result = db.insert_employee(employee)
    print("Insert result:")
    print(result)

    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT employee_id, first_name, last_name, department, job_title, manager, status, username FROM employees")
    rows = cursor.fetchall()
    db.close()

    print("\nEmployees in SQLite:")
    for row in rows:
        print({
            "employee_id": row[0],
            "first_name": row[1],
            "last_name": row[2],
            "department": row[3],
            "job_title": row[4],
            "manager": row[5],
            "status": row[6],
            "username": row[7],
        })


if __name__ == "__main__":
    main()
