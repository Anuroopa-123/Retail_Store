from __future__ import annotations
from datetime import datetime
from typing import Optional
from sqlalchemy import Integer, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True, sort_order=-1
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), sort_order=9997
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        onupdate=func.now(),
        sort_order=9998,
    )


class EmailVerificationMixin:
    is_email_verified: Mapped[bool] = mapped_column(default=False, sort_order=9995)
    email_verified_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, sort_order=9996
    )


class SoftDeleteMixin:
    is_deleted: Mapped[bool] = mapped_column(default=False, sort_order=9999)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, sort_order=10000
    )

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = func.now()

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None