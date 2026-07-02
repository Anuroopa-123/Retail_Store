# src/domain/entities/employee/employee_profile.py
from __future__ import annotations

from datetime import date
from typing import Optional
from sqlalchemy import String, ForeignKey, Date, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from src.domain.entities.base import BaseModel


class EmployeeProfile(BaseModel):
    __tablename__ = "employee_profiles"

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"),
        unique=True, nullable=False,
    )
    tenant_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    store_id: Mapped[int] = mapped_column(
    Integer,
    ForeignKey("stores.id"),
    nullable=False
)
    employee_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    gender: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    dob: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    address: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=True)
    emergency_contact: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=True)
    joining_date: Mapped[date] = mapped_column(Date, nullable=False)
    leaving_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    department: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="employee_profile")
    
    attendances: Mapped[list["EmployeeAttendance"]] = relationship(
        "EmployeeAttendance", back_populates="employee"
    )
    payrolls: Mapped[list["EmployeePayroll"]] = relationship(
        "EmployeePayroll", back_populates="employee"
    )
    

    def __repr__(self) -> str:
        return f"<EmployeeProfile code={self.employee_code}>"