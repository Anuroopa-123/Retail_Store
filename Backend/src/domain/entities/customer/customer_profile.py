# src/domain/entities/customer/customer_profile.py
from __future__ import annotations

from datetime import date
from typing import Optional
from sqlalchemy import String, ForeignKey, Date, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from src.domain.entities.base import BaseModel


class CustomerProfile(BaseModel):
    __tablename__ = "customer_profiles"

    customer_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("customers.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    first_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    gender: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    dob: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    address: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=True)
    preferences: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=True)

    customer: Mapped["Customer"] = relationship(
        "Customer", back_populates="profile"
    )

    def __repr__(self) -> str:
        return f"<CustomerProfile customer_id={self.customer_id}>"