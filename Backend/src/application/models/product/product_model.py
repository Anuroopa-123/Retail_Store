from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# ---------------------------------------
# Create Product
# ---------------------------------------

class ProductCreateRequest(BaseModel):

    tenant_id: int

    store_id: int

    category_id: Optional[int] = None

    brand_id: Optional[int] = None

    product_name: str

    purchase_price: float

    selling_price: float

    tax: float = 0

    stock: int = 0

    minimum_stock: int = 10

    unit: Optional[str] = None

    description: Optional[str] = None

    image_url: Optional[str] = None

    status: str = "Active"

    created_by: Optional[int] = None


# ---------------------------------------
# Update Product
# ---------------------------------------

class ProductUpdateRequest(BaseModel):

    category_id: Optional[int] = None

    brand_id: Optional[int] = None

    product_name: Optional[str] = None

    purchase_price: Optional[float] = None

    selling_price: Optional[float] = None

    tax: Optional[float] = None

    unit: Optional[str] = None

    description: Optional[str] = None

    image_url: Optional[str] = None

    status: Optional[str] = None


# ---------------------------------------
# Product Response
# ---------------------------------------

class ProductResponse(BaseModel):

    id: int

    tenant_id: int

    store_id: int

    category_id: Optional[int]

    brand_id: Optional[int]

    product_name: str

    sku: str

    barcode: str

    purchase_price: float

    selling_price: float

    tax: float

    stock: int

    minimum_stock: int

    unit: Optional[str]

    image_url: Optional[str]

    description: Optional[str]

    status: str

    created_by: Optional[int]

    created_at: datetime

    updated_at: datetime

    class Config:

        from_attributes = True