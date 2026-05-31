# src/domain/entities/tenant.py
from __future__ import annotations

from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.domain.entities.base import BaseModel
from src.domain.enums import TenantStatusEnum


class Tenant(BaseModel):
    __tablename__ = "tenants"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    domain: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(
        String(20), default=TenantStatusEnum.ACTIVE, nullable=False
    )

    users: Mapped[list["User"]] = relationship("User", back_populates="tenant")
    roles: Mapped[list["Role"]] = relationship("Role", back_populates="tenant")
    settings: Mapped[list["Setting"]] = relationship("Setting", back_populates="tenant")
    stores: Mapped[list["Store"]] = relationship("Store", back_populates="tenant")


    def __repr__(self) -> str:
        return f"<Tenant slug={self.slug}>"