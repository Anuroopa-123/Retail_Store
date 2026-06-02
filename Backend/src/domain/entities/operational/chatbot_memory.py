# src/domain/entities/operational/chatbot_memory.py
from __future__ import annotations

from datetime import datetime
from typing import Optional
from sqlalchemy import String, ForeignKey, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from src.domain.entities.base import BaseModel


class ChatbotMemory(BaseModel):
    __tablename__ = "chatbot_memories"

    tenant_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    customer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("customers.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    session_id: Mapped[str] = mapped_column(String(255), nullable=False)
    messages: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    context: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=True)
    last_active_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    customer: Mapped["Customer"] = relationship("Customer")

    def __repr__(self) -> str:
        return f"<ChatbotMemory customer={self.customer_id} session={self.session_id}>"