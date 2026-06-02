# src/domain/entities/product/product.py
from __future__ import annotations

from typing import Optional
from sqlalchemy import String, ForeignKey, Integer, Numeric, UniqueConstraint, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from src.domain.entities.base import BaseModel
from src.domain.enums import ProductStatusEnum


class Product(BaseModel):
    __tablename__ = "products"

    tenant_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    brand_id: Mapped[Optional[int]] = mapped_column(
    Integer, ForeignKey("brands.id", ondelete="SET NULL"),
    nullable=True, index=True,
     )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    sku: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    stock_qty: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    status: Mapped[str] = mapped_column(
        String(30), default=ProductStatusEnum.ACTIVE, nullable=False
    )
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    unit: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    reorder_level: Mapped[int] = mapped_column(Integer, default=10, nullable=False)

    metadata_: Mapped[dict] = mapped_column(
        "metadata", JSONB, default=dict, nullable=True
    )

    customer_interactions: Mapped[list["CustomerProduct"]] = relationship(
        "CustomerProduct", back_populates="product"
    )

    category_id: Mapped[Optional[int]] = mapped_column(
    Integer, ForeignKey("product_categories.id", ondelete="SET NULL"),
    nullable=True, index=True,
   )

    brand: Mapped[Optional["Brand"]] = relationship("Brand", back_populates="products")

    __table_args__ = (
        UniqueConstraint("tenant_id", "sku", name="uq_product_tenant_sku"),
    )

    def __repr__(self) -> str:
        return f"<Product sku={self.sku}>"