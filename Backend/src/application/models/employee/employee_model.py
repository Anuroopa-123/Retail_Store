from pydantic import BaseModel
from datetime import date

class EmployeeCreateRequest(
    BaseModel
):

    tenant_id: int

    store_id: int

    name: str

    email: str

    password: str

    gender: str | None = None

    phone: str | None = None

    department_id: int

    joining_date: date