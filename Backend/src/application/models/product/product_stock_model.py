from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# ---------------------------------------
# Create Product Stock
# ---------------------------------------

class ProductStockCreateRequest(BaseModel):

    product_id: int

    store_id: int

    stock: int = 0

    minimum_stock: int = 10


# ---------------------------------------
# Update Product Stock
# ---------------------------------------

class ProductStockUpdateRequest(BaseModel):

    stock: Optional[int] = None

    minimum_stock: Optional[int] = None


# ---------------------------------------
# Response
# ---------------------------------------

class ProductStockResponse(BaseModel):

    id: int

    product_id: int

    store_id: int

    stock: int

    minimum_stock: int

    created_at: datetime

    updated_at: datetime

    class Config:

        from_attributes = True