from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.database import Database
from app.iam_service import IAMService
from app.models import Employee

app = FastAPI(
    title="Enterprise IAM Lifecycle Lab",
    version="1.0.0",
)

service = IAMService()
database = Database()


@app.get("/")
def read_root():
    return {
        "message": "Enterprise IAM Lifecycle Lab API",
        "status": "running",
    }


@app.get("/employees")
def get_employees():
    employees = database.get_all_employees()
    return {
        "success": True,
        "count": len(employees),
        "employees": employees,
    }


@app.get("/employees/{employee_id}")
def get_employee_by_id(employee_id: str):
    employee = database.get_employee_by_id(employee_id)
    if employee is None:
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "message": "Employee not found.",
            },
        )

    return {
        "success": True,
        "employee": employee,
    }


@app.post("/employees")
def create_employee(employee: Employee):
    return service.create_employee(employee)
