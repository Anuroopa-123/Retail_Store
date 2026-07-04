from __future__ import annotations

from typing import Optional

from sqlalchemy import (
    String,
    Integer,
    Text,
    ForeignKey
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from src.domain.entities.base import BaseModel


class Brand(BaseModel):

    __tablename__ = "brands"

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

    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("product_categories.id", ondelete="CASCADE"),
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )

    logo_url: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="Active",
        nullable=False
    )

    created_by: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    category = relationship(
        "ProductCategory"
    )

    products = relationship(
        "Product",
        back_populates="brand"
    )

    def __repr__(self):
        return f"<Brand {self.name}>"