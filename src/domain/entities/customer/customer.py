# src/domain/entities/customer/customer.py
from __future__ import annotations

from typing import Optional
from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.domain.entities.base import BaseModel
from src.domain.enums import CustomerStatusEnum


class Customer(BaseModel):
    __tablename__ = "customers"

    tenant_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )
    phone: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
    )
    status: Mapped[str] = mapped_column(
        String(20),
        default=CustomerStatusEnum.ACTIVE,
        nullable=False,
    )

    # relationships
    profile: Mapped["CustomerProfile"] = relationship(
        "CustomerProfile",
        back_populates="customer",
        uselist=False,
        cascade="all, delete-orphan",
    )
    product_interactions: Mapped[list["CustomerProduct"]] = relationship(
        "CustomerProduct", back_populates="customer"
    )
    subscriptions: Mapped[list["Subscription"]] = relationship(
        "Subscription", back_populates="customer"
    )

    def __repr__(self) -> str:
        return f"<Customer email={self.email}>"