from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# ---------------------------------------------
# Create Brand
# ---------------------------------------------
class BrandCreateRequest(BaseModel):

    tenant_id: int

    store_id: int

    category_id: int

    name: str

    description: Optional[str] = None

    logo_url: Optional[str] = None

    status: Optional[str] = "Active"

    created_by: Optional[int] = None


# ---------------------------------------------
# Update Brand
# ---------------------------------------------
class BrandUpdateRequest(BaseModel):

    category_id: Optional[int] = None

    name: Optional[str] = None

    description: Optional[str] = None

    logo_url: Optional[str] = None

    status: Optional[str] = None


# ---------------------------------------------
# Response Model
# ---------------------------------------------
class BrandResponse(BaseModel):

    id: int

    tenant_id: int

    store_id: int

    category_id: int

    name: str

    description: Optional[str]

    logo_url: Optional[str]

    status: str

    created_by: Optional[int]

    created_at: datetime

    updated_at: datetime

    class Config:
        from_attributes = True