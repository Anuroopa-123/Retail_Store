# src/domain/entities/auth/email_verification_token.py
from __future__ import annotations

from datetime import datetime
from typing import Optional
from sqlalchemy import String, ForeignKey, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.domain.entities.base import BaseModel


class EmailVerificationToken(BaseModel):
    __tablename__ = "email_verification_tokens"

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    token_hash: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="email_verification_tokens")

    def __repr__(self) -> str:
        return f"<EmailVerificationToken user={self.user_id}>"