from pydantic import EmailStr
from src.application.models.core.base_model import BasePostModel


class CreateAdminRequest(BasePostModel):
    tenant_id: int
    store_id: int
    name: str
    email: EmailStr
    password: str