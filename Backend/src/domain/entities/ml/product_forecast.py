# src/domain/entities/ml/product_forecast.py
from __future__ import annotations

from datetime import date
from typing import Optional
from sqlalchemy import String, ForeignKey, Integer, Numeric, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.domain.entities.base import BaseModel


class ProductForecast(BaseModel):
    __tablename__ = "product_forecasts"

    tenant_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    store_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("stores.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    product_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    forecast_date: Mapped[date] = mapped_column(Date, nullable=False)
    predicted_sales: Mapped[int] = mapped_column(Integer, nullable=False)
    confidence_score: Mapped[Optional[float]] = mapped_column(Numeric(5, 2), nullable=True)
    model_version: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    product: Mapped["Product"] = relationship("Product")
    store: Mapped["Store"] = relationship("Store")

    def __repr__(self) -> str:
        return f"<ProductForecast product={self.product_id} date={self.forecast_date}>"