from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.iam_service import IAMService
from app.models import Employee

app = FastAPI(
    title="Enterprise IAM Lifecycle Lab",
    version="1.0.0",
)

service = IAMService()
database = service.database


class MoveEmployeeRequest(BaseModel):
    new_job_title: str


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


@app.put("/employees/{employee_id}")
def update_employee(employee_id: str, employee: Employee):
    update_result = database.update_employee(
        employee_id=employee_id,
        first_name=employee.first_name,
        last_name=employee.last_name,
        department=employee.department,
        job_title=employee.job_title,
        manager=employee.manager,
        status=employee.status,
        username=employee.username,
    )

    if not update_result.get("success", False):
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "message": "Employee not found.",
            },
        )

    updated_employee = database.get_employee_by_id(employee_id)

    return {
        "success": True,
        "message": "Employee updated successfully.",
        "employee": updated_employee,
    }


@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: str):
    delete_result = database.delete_employee(employee_id)
    if not delete_result.get("success", False):
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "message": "Employee not found.",
            },
        )

    return {
        "success": True,
        "message": "Employee deleted successfully.",
    }


@app.post("/employees/{employee_id}/move")
def move_employee(employee_id: str, payload: MoveEmployeeRequest):
    result = service.update_employee_role(employee_id, payload.new_job_title)

    if not result.get("success", False):
        message = result.get("message", "Employee not found.")
        if "not found" in message.lower():
            return JSONResponse(status_code=404, content={"success": False, "message": message})
        return JSONResponse(status_code=400, content={"success": False, "message": message})

    return {
        "success": True,
        "message": result.get("message"),
        "employee": result.get("employee"),
    }


@app.post("/employees/{employee_id}/terminate")
def terminate_employee(employee_id: str):
    result = service.terminate_employee(employee_id)
    if not result.get("success", False):
        return JSONResponse(
            status_code=404,
            content={"success": False, "message": result.get("message")},
        )

    return {
        "success": True,
        "message": result.get("message"),
        "employee": result.get("employee"),
    }


@app.post("/employees")
def create_employee(employee: Employee):
    return service.create_employee(employee)
