from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# ---------------------------------------
# Create Stock Movement
# ---------------------------------------

class StockMovementCreateRequest(BaseModel):

    tenant_id: int

    store_id: int

    product_id: int

    movement_type: str
    # STOCK_IN
    # STOCK_OUT
    # ADJUSTMENT
    # TRANSFER

    quantity: int

    previous_qty: int

    current_qty: int

    reference: Optional[str] = None

    note: Optional[str] = None

    moved_by: Optional[int] = None


# ---------------------------------------
# Update Stock Movement
# ---------------------------------------

class StockMovementUpdateRequest(BaseModel):

    movement_type: Optional[str] = None

    quantity: Optional[int] = None

    previous_qty: Optional[int] = None

    current_qty: Optional[int] = None

    reference: Optional[str] = None

    note: Optional[str] = None

    moved_by: Optional[int] = None


# ---------------------------------------
# Stock Movement Response
# ---------------------------------------

class StockMovementResponse(BaseModel):

    id: int

    tenant_id: int

    store_id: int

    product_id: int

    movement_type: str

    quantity: int

    previous_qty: int

    current_qty: int

    reference: Optional[str]

    note: Optional[str]

    moved_by: Optional[int]

    created_at: datetime

    updated_at: datetime

    class Config:

        from_attributes = True