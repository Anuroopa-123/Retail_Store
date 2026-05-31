# src/domain/entities/operational/setting.py
from __future__ import annotations

from typing import Optional
from sqlalchemy import String, ForeignKey, Text, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.domain.entities.base import BaseModel
from src.domain.enums import SettingTypeEnum


class Setting(BaseModel):
    __tablename__ = "settings"

    tenant_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    key: Mapped[str] = mapped_column(String(100), nullable=False)
    value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    type: Mapped[str] = mapped_column(
        String(20), default=SettingTypeEnum.STRING, nullable=False
    )
    group: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="settings")

    __table_args__ = (
        UniqueConstraint("tenant_id", "key", name="uq_setting_tenant_key"),
    )

    def __repr__(self) -> str:
        return f"<Setting key={self.key} tenant={self.tenant_id}>"