# src/domain/entities/inventory/stock_movement.py
from __future__ import annotations

from typing import Optional
from sqlalchemy import String, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.domain.entities.base import BaseModel


class StockMovement(BaseModel):
    __tablename__ = "stock_movements"

    product_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    store_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("stores.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    type: Mapped[str] = mapped_column(String(50), nullable=False)  # "in", "out", "adjustment"
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    previous_qty: Mapped[int] = mapped_column(Integer, nullable=False)
    current_qty: Mapped[int] = mapped_column(Integer, nullable=False)
    reference: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    moved_by: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    product: Mapped["Product"] = relationship("Product")
    store: Mapped["Store"] = relationship("Store")

    def __repr__(self) -> str:
        return f"<StockMovement product={self.product_id} type={self.type}>"