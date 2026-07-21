from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.iam_service import IAMService
from app.models import Employee

app = FastAPI(
    title="Enterprise IAM Lifecycle Lab",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

service = IAMService()
database = service.database


class MoveEmployeeRequest(BaseModel):
    new_job_title: str


DEMO_EMPLOYEES = [
    Employee("D1001", "Amina", "Hassan", "Engineering", "Software Developer", "Maya Chen", "active"),
    Employee("D1002", "Noah", "Reed", "Security", "Security Analyst", "Priya Shah", "active"),
    Employee("D1003", "Sofia", "Garcia", "Finance", "Finance Analyst", "Omar Khan", "active"),
    Employee("D1004", "Ethan", "Brooks", "IT Support", "Help Desk Analyst", "Nina Patel", "active"),
    Employee("D1005", "Maya", "Chen", "Identity", "IAM Analyst", "Abdulaziz Abdi", "active"),
    Employee("D1006", "Lena", "Morris", "People", "HR Specialist", "Grace Lee", "active"),
    Employee("D1007", "Caleb", "Stone", "Engineering", "Software Developer", "Maya Chen", "terminated"),
    Employee("D1008", "Priya", "Shah", "Security", "Security Analyst", "Abdulaziz Abdi", "active"),
    Employee("D1009", "Omar", "Khan", "Finance", "Finance Analyst", "Abdulaziz Abdi", "terminated"),
    Employee("D1010", "Nina", "Patel", "IT Support", "Help Desk Analyst", "Abdulaziz Abdi", "active"),
]


def _clear_demo_state():
    for employee in database.get_all_employees():
        database.delete_employee(employee.get("employee_id"))
    service._save_employees([])
    service.audit_logger._save_audit_log([])


def _seed_demo_state():
    _clear_demo_state()
    created = 0
    for employee in DEMO_EMPLOYEES:
        result = service.create_employee(employee)
        if result.get("success"):
            created += 1
        if employee.status == "terminated":
            service.terminate_employee(employee.employee_id)
    service.update_employee_role("D1004", "IAM Analyst")
    return created


@app.get("/")
def read_root():
    return {
        "message": "Enterprise IAM Lifecycle Lab API",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "Enterprise IAM API",
        "version": "1.0.0",
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


@app.get("/audit-logs")
def get_audit_logs(action: Optional[str] = None, status: Optional[str] = None, employee_id: Optional[str] = None):
    events = service.audit_logger.get_events()

    if action:
        action_lower = action.lower()
        events = [event for event in events if event.get("action", "").lower() == action_lower]

    if status:
        status_lower = status.lower()
        events = [event for event in events if event.get("status", "").lower() == status_lower]

    if employee_id:
        events = [event for event in events if event.get("employee_id") == employee_id]

    return {
        "success": True,
        "count": len(events),
        "events": events,
    }


@app.get("/roles")
def get_roles():
    roles_data = service._load_roles()
    roles = [
        {
            "job_title": title,
            "groups": details.get("groups", []),
            "applications": details.get("applications", []),
        }
        for title, details in sorted(roles_data.items(), key=lambda item: item[0])
    ]

    return {
        "success": True,
        "count": len(roles),
        "roles": roles,
    }


@app.get("/roles/{job_title}")
def get_role_by_title(job_title: str):
    roles_data = service._load_roles()
    role_definition = roles_data.get(job_title)

    if role_definition is None:
        return JSONResponse(
            status_code=404,
            content={"success": False, "message": "Role not found."},
        )

    return {
        "success": True,
        "role": {
            "job_title": job_title,
            "groups": role_definition.get("groups", []),
            "applications": role_definition.get("applications", []),
        },
    }


@app.post("/employees")
def create_employee(employee: Employee):
    return service.create_employee(employee)


@app.post("/demo/seed")
def seed_demo_data():
    created = _seed_demo_state()
    events = service.audit_logger.get_events()
    return {
        "success": True,
        "message": "Demo data loaded successfully.",
        "employees_created": created,
        "audit_events": len(events),
    }


@app.post("/demo/reset")
def reset_demo_data():
    created = _seed_demo_state()
    events = service.audit_logger.get_events()
    return {
        "success": True,
        "message": "Demo data reset successfully.",
        "employees_created": created,
        "audit_events": len(events),
    }
