# src/domain/entities/product/brand.py
from __future__ import annotations

from typing import Optional
from sqlalchemy import String, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.domain.entities.base import BaseModel


class Brand(BaseModel):
    __tablename__ = "brands"

    tenant_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    logo_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="active", nullable=False)

    # one brand → many products
    products: Mapped[list["Product"]] = relationship(
        "Product", back_populates="brand"
    )

    def __repr__(self) -> str:
        return f"<Brand name={self.name}>"