# src/domain/entities/inventory/stock_alert.py
from __future__ import annotations

from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.domain.entities.base import BaseModel


class StockAlert(BaseModel):
    __tablename__ = "stock_alerts"

    tenant_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    product_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    current_qty: Mapped[int] = mapped_column(Integer, nullable=False)
    threshold_qty: Mapped[int] = mapped_column(Integer, nullable=False)
    alert_type: Mapped[str] = mapped_column(String(50), nullable=False)  # "low_stock", "out_of_stock"
    status: Mapped[str] = mapped_column(String(50), default="active", nullable=False)

    product: Mapped["Product"] = relationship("Product")

    def __repr__(self) -> str:
        return f"<StockAlert product={self.product_id} type={self.alert_type}>"