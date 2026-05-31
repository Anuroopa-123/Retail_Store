# src/domain/entities/employee/employee_attendance.py
from __future__ import annotations

from datetime import date, datetime
from typing import Optional
from sqlalchemy import String, ForeignKey, Date, DateTime, Numeric, UniqueConstraint, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.domain.entities.base import BaseModel
from src.domain.enums import AttendanceStatusEnum


class EmployeeAttendance(BaseModel):
    __tablename__ = "employee_attendances"

    employee_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("employee_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(20),
        default=AttendanceStatusEnum.PRESENT,
        nullable=False,
    )
    check_in: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    check_out: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    hours_worked: Mapped[Optional[str]] = mapped_column(
        Numeric(4, 2),
        nullable=True,
    )
    note: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    # relationships
    employee: Mapped["EmployeeProfile"] = relationship(
        "EmployeeProfile",
        back_populates="attendances",
    )

    __table_args__ = (
        UniqueConstraint(
            "employee_id", "date",
            name="uq_attendance_employee_date",
        ),
    )

    def __repr__(self) -> str:
        return f"<EmployeeAttendance employee={self.employee_id} date={self.date}>"