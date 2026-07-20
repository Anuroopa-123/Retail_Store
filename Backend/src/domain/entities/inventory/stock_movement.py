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
    mapped_column,
    relationship
)

from src.domain.entities.base import BaseModel


class StockMovement(BaseModel):

    __tablename__ = "stock_movements"

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
    
    destination_store_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey(
            "stores.id",
            ondelete="CASCADE"
        ),
        nullable=True,
        index=True
    )

    product_id: Mapped[int] = mapped_column(

        Integer,

        ForeignKey(
            "products.id",
            ondelete="CASCADE"
        ),

        nullable=False,

        index=True

    )

    movement_type: Mapped[str] = mapped_column(

        String(50),

        nullable=False

    )
    # STOCK_IN
    # STOCK_OUT
    # ADJUSTMENT
    # TRANSFER

    quantity: Mapped[int] = mapped_column(

        Integer,

        nullable=False

    )

    previous_qty: Mapped[int] = mapped_column(

        Integer,

        nullable=False

    )

    current_qty: Mapped[int] = mapped_column(

        Integer,

        nullable=False

    )

    reference: Mapped[Optional[str]] = mapped_column(

        String(255),

        nullable=True

    )

    note: Mapped[Optional[str]] = mapped_column(

        Text,

        nullable=True

    )

    moved_by: Mapped[Optional[int]] = mapped_column(

        Integer,

        ForeignKey(
            "users.id",
            ondelete="SET NULL"
        ),

        nullable=True

    )

    product = relationship("Product")

    store = relationship(
        "Store",
        foreign_keys=[store_id]
    )

    destination_store = relationship(
        "Store",
        foreign_keys=[destination_store_id]
    )
    def __repr__(self):

        return f"<StockMovement {self.product_id}>"