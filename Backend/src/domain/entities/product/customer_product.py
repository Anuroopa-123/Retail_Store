# src/domain/entities/product/customer_product.py
from __future__ import annotations

from sqlalchemy import String, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.domain.entities.base import BaseModel


class CustomerProduct(BaseModel):
    __tablename__ = "customer_products"

    customer_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("customers.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    product_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    relation_type: Mapped[str] = mapped_column(String(20), nullable=False)

    customer: Mapped["Customer"] = relationship(
        "Customer", back_populates="product_interactions"
    )
    product: Mapped["Product"] = relationship(
        "Product",
        # back_populates="customer_interactions"
    )

    __table_args__ = (
        UniqueConstraint(
            "customer_id", "product_id", "relation_type",
            name="uq_customer_product_relation",
        ),
    )

    def __repr__(self) -> str:
        return f"<CustomerProduct customer={self.customer_id} product={self.product_id}>"