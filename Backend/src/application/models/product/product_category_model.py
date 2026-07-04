from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ProductCategoryCreateRequest(BaseModel):

    tenant_id: int

    store_id: int

    name: str
    
    slug: str | None = None

    description: Optional[str] = None

    status: Optional[str] = "Active"

    created_by: Optional[int] = None


class ProductCategoryUpdateRequest(BaseModel):

    name: Optional[str] = None

    description: Optional[str] = None

    status: Optional[str] = None


class ProductCategoryResponse(BaseModel):

    id: int

    tenant_id: int

    store_id: int

    name: str

    description: Optional[str]

    status: str

    created_by: Optional[int]

    created_at: datetime

    updated_at: datetime

    class Config:
        from_attributes = True