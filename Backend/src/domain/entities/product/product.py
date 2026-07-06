from __future__ import annotations

from typing import Optional

from sqlalchemy import (
    String,
    ForeignKey,
    Integer,
    Numeric,
    Text,
    UniqueConstraint
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from src.domain.entities.base import BaseModel


class Product(BaseModel):

    __tablename__ = "products"

    tenant_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    store_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("stores.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    category_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("product_categories.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    brand_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("brands.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    product_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    sku: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    barcode: Mapped[Optional[str]] = mapped_column(
        String(100),
        unique=True,
        nullable=True
    )

    purchase_price: Mapped[float] = mapped_column(
        Numeric(10,2),
        nullable=False
    )

    selling_price: Mapped[float] = mapped_column(
        Numeric(10,2),
        nullable=False
    )

    tax: Mapped[float] = mapped_column(
        Numeric(5,2),
        default=0
    )

    stock: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    minimum_stock: Mapped[int] = mapped_column(
        Integer,
        default=10
    )

    image_url: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )

    unit: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="Active"
    )

    created_by: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    category = relationship("ProductCategory")

    brand = relationship(
        "Brand",
        back_populates="products"
    )

    __table_args__ = (

        UniqueConstraint(
            "tenant_id",
            "sku",
            name="uq_product_tenant_sku"
        ),

    )

    def __repr__(self):

        return f"<Product {self.product_name}>"