# src/domain/entities/store.py
from __future__ import annotations

from typing import Optional
from datetime import time
from sqlalchemy import String, ForeignKey, Integer, Time, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from src.domain.entities.base import BaseModel
from src.domain.enums import StoreStatusEnum


class Store(BaseModel):
    __tablename__ = "stores"

    tenant_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    opening_time: Mapped[Optional[time]] = mapped_column(Time, nullable=True)
    closing_time: Mapped[Optional[time]] = mapped_column(Time, nullable=True)
    status: Mapped[str] = mapped_column(
        String(50), default=StoreStatusEnum.ACTIVE, nullable=False
    )

    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="stores")
    users: Mapped[list["User"]] = relationship("User", back_populates="store")

    def __repr__(self) -> str:
        return f"<Store name={self.name}>"