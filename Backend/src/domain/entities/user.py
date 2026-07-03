# src/domain/entities/user.py
from __future__ import annotations

from typing import Optional
from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.domain.entities.base import BaseModel
from src.domain.enums import UserStatusEnum
from src.domain.entities.auth.session import Session
from src.domain.entities.auth.personal_access_token import PersonalAccessToken
from src.domain.entities.auth.password_reset_token import PasswordResetToken
from src.domain.entities.auth.email_verification_token import EmailVerificationToken
from src.domain.entities.operational.notification import Notification
from sqlalchemy.orm import relationship


class User(BaseModel):
    __tablename__ = "users"

    tenant_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    store_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("stores.id", ondelete="SET NULL"),
        nullable=True, index=True,
    )
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), default=UserStatusEnum.PENDING, nullable=False
    )
    email_verified_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # relationships
    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="users")
    store: Mapped[Optional["Store"]] = relationship("Store", back_populates="users")
    roles: Mapped[list["Role"]] = relationship(
        "Role", secondary="user_roles", back_populates="users"
    )
    employee_profile: Mapped[Optional["EmployeeProfile"]] = relationship(
        "EmployeeProfile", back_populates="user", uselist=False
    )
    sessions: Mapped[list["Session"]] = relationship(
    "Session", back_populates="user", cascade="all, delete-orphan"
)
    personal_access_tokens: Mapped[list["PersonalAccessToken"]] = relationship(
    "PersonalAccessToken", back_populates="user", cascade="all, delete-orphan"
)
    password_reset_tokens: Mapped[list["PasswordResetToken"]] = relationship(
    "PasswordResetToken", back_populates="user", cascade="all, delete-orphan"
)
    email_verification_tokens: Mapped[list["EmailVerificationToken"]] = relationship(
    "EmailVerificationToken", back_populates="user", cascade="all, delete-orphan"
)
    notifications: Mapped[list["Notification"]] = relationship(
    "Notification", back_populates="user", cascade="all, delete-orphan"
)
    @property
    def is_verified(self) -> bool:
        return self.email_verified_at is not None

    def __repr__(self) -> str:
        return f"<User email={self.email}>"