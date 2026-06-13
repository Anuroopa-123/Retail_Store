from pydantic import BaseModel

class DepartmentCreateRequest(
    BaseModel
):

    tenant_id: int

    store_id: int

    created_by: int

    name: str