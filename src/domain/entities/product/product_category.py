# src/domain/entities/product/product_category.py
from __future__ import annotations

from typing import Optional
from sqlalchemy import String, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.domain.entities.base import BaseModel


class ProductCategory(BaseModel):
    __tablename__ = "product_categories"

    tenant_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False)

    # self-referencing FK — a category can have a parent category
    # e.g. "Dairy" → parent "Food & Beverages"
    parent_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("product_categories.id", ondelete="SET NULL"),
        nullable=True,
    )
    image_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="active", nullable=False)

    parent: Mapped[Optional["ProductCategory"]] = relationship(
        "ProductCategory", remote_side="ProductCategory.id", back_populates="children"
    )
    children: Mapped[list["ProductCategory"]] = relationship(
        "ProductCategory", back_populates="parent"
    )

    def __repr__(self) -> str:
        return f"<ProductCategory name={self.name}>"