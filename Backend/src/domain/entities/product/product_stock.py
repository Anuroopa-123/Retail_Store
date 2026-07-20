from __future__ import annotations

from sqlalchemy import (
    Integer,
    ForeignKey,
    UniqueConstraint
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from src.domain.entities.base import BaseModel


class ProductStock(BaseModel):

    __tablename__ = "product_stock"

    product_id: Mapped[int] = mapped_column(

        Integer,

        ForeignKey(
            "products.id",
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

    stock: Mapped[int] = mapped_column(

        Integer,

        default=0,

        nullable=False

    )

    minimum_stock: Mapped[int] = mapped_column(

        Integer,

        default=10,

        nullable=False

    )

    product = relationship(

        "Product"

    )

    store = relationship(

        "Store"

    )

    __table_args__ = (

        UniqueConstraint(

            "product_id",

            "store_id",

            name="uq_product_store"

        ),

    )

    def __repr__(self):

        return f"<ProductStock Product={self.product_id} Store={self.store_id}>"