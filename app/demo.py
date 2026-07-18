from app.models import Employee
from app.iam_service import IAMService


def main():
    employee = Employee(
        employee_id="100001",
        first_name="Abdulaziz",
        last_name="Abdi",
        department="Information Technology",
        job_title="Help Desk Analyst",
        manager="Sarah Johnson",
    )

    service = IAMService()
    result = service.create_employee(employee)

    print("Result:")
    print(result)
    print()
    print("Final Employee Object:")
    print(employee)


if __name__ == "__main__":
    main()
