# src/domain/entities/alerts/alert_rule.py
from __future__ import annotations

from typing import Optional
from sqlalchemy import String, ForeignKey, Integer, Numeric, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from src.domain.entities.base import BaseModel


class AlertRule(BaseModel):
    __tablename__ = "alert_rules"

    tenant_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    type: Mapped[str] = mapped_column(String(100), nullable=False)   # "low_stock", "attendance"
    threshold_value: Mapped[Optional[float]] = mapped_column(Numeric, nullable=True)
    notify_role: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # role slug
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    def __repr__(self) -> str:
        return f"<AlertRule type={self.type}>"