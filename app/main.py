from fastapi import FastAPI

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


@app.post("/employees")
def create_employee(employee: Employee):
    return service.create_employee(employee)
