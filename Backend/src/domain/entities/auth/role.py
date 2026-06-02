# src/domain/entities/auth/role.py
from __future__ import annotations

from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.domain.entities.base import BaseModel


class Role(BaseModel):
    __tablename__ = "roles"

    tenant_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    slug: Mapped[str] = mapped_column(String(50), nullable=False)

    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="roles")
    users: Mapped[list["User"]] = relationship(
        "User", secondary="user_roles", back_populates="roles"
    )
    permissions: Mapped[list["Permission"]] = relationship(
        "Permission", secondary="role_permissions"
    )

    def __repr__(self) -> str:
        return f"<Role slug={self.slug}>"