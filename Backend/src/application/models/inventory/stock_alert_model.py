from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# ---------------------------------------
# Create Stock Alert
# ---------------------------------------

class StockAlertCreateRequest(BaseModel):

    tenant_id: int

    store_id: int

    product_id: int

    current_qty: int

    threshold_qty: int

    alert_type: str

    status: str = "Active"


# ---------------------------------------
# Update Stock Alert
# ---------------------------------------

class StockAlertUpdateRequest(BaseModel):

    current_qty: Optional[int] = None

    threshold_qty: Optional[int] = None

    alert_type: Optional[str] = None

    status: Optional[str] = None


# ---------------------------------------
# Response
# ---------------------------------------

class StockAlertResponse(BaseModel):

    id: int

    tenant_id: int

    store_id: int

    product_id: int

    current_qty: int

    threshold_qty: int

    alert_type: str

    status: str

    created_at: datetime

    updated_at: datetime

    class Config:

        from_attributes = True