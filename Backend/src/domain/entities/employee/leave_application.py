# src/domain/entities/employee/leave_application.py
from __future__ import annotations

from datetime import date
from typing import Optional
from sqlalchemy import String, ForeignKey, Integer, Date, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.domain.entities.base import BaseModel


class LeaveApplication(BaseModel):
    __tablename__ = "leave_applications"

    employee_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    leave_type: Mapped[str] = mapped_column(String(50), nullable=False)  # "sick", "casual", "annual"
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False)
    approved_by: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    employee: Mapped["User"] = relationship("User", foreign_keys=[employee_id])
    approver: Mapped[Optional["User"]] = relationship("User", foreign_keys=[approved_by])

    def __repr__(self) -> str:
        return f"<LeaveApplication employee={self.employee_id} status={self.status}>"