from fastapi import FastAPI

from app.iam_service import IAMService
from app.models import Employee

app = FastAPI(
    title="Enterprise IAM Lifecycle Lab",
    version="1.0.0",
)

service = IAMService()


@app.get("/")
def read_root():
    return {
        "message": "Enterprise IAM Lifecycle Lab API",
        "status": "running",
    }


@app.post("/employees")
def create_employee(employee: Employee):
    return service.create_employee(employee)
