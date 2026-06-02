# src/domain/entities/operational/ai_telemetry.py
from __future__ import annotations

from typing import Optional
from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from src.domain.entities.base import BaseModel
from src.domain.enums import AITelemetryStatusEnum


class AITelemetry(BaseModel):
    __tablename__ = "ai_telemetry"

    tenant_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    user_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    prompt_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    input_tokens: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    output_tokens: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    latency_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(
        String(20), default=AITelemetryStatusEnum.SUCCESS, nullable=False
    )

    def __repr__(self) -> str:
        return f"<AITelemetry model={self.model} status={self.status}>"