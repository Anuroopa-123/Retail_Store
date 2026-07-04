from __future__ import annotations

from typing import Optional

from sqlalchemy import (
    String,
    ForeignKey,
    Integer,
    Text
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from src.domain.entities.base import BaseModel


class ProductCategory(BaseModel):

    __tablename__ = "product_categories"

    tenant_id: Mapped[int] = mapped_column(

        Integer,

        ForeignKey(
            "tenants.id",
            ondelete="CASCADE"
        ),

        nullable=False,

        index=True

    )

    store_id: Mapped[int] = mapped_column(

        Integer,

        ForeignKey(
            "stores.id",
            ondelete="CASCADE"
        ),

        nullable=False,

        index=True

    )

    name: Mapped[str] = mapped_column(
    String(255),
    nullable=False
)
    slug: Mapped[str] = mapped_column(
    String(255),
    nullable=False
)

    description: Mapped[Optional[str]] = mapped_column(

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

    def __repr__(self):

        return f"<ProductCategory {self.name}>"