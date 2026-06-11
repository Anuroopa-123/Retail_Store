from pydantic import BaseModel
from datetime import date

class EmployeeCreateRequest(BaseModel):
    tenant_id: int
    name: str
    email: str
    password: str
    employee_code: str
    gender: str | None = None
    phone: str | None = None
    department: str | None = None
    joining_date: date