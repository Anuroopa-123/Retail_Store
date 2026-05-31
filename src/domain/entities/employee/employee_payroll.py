from __future__ import annotations

from datetime import date
from typing import Optional
from sqlalchemy import String, ForeignKey, Date, Numeric, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.domain.entities.base import BaseModel
from src.domain.enums import PayrollStatusEnum


class EmployeePayroll(BaseModel):
    __tablename__ = "employee_payrolls"

    employee_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("employee_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    month: Mapped[int] = mapped_column(Integer, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    days_present: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    days_absent: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    hours_worked: Mapped[float] = mapped_column(Numeric(6, 2), default=0, nullable=False)
    basic_salary: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    deductions: Mapped[float] = mapped_column(Numeric(10, 2), default=0, nullable=False)
    bonuses: Mapped[float] = mapped_column(Numeric(10, 2), default=0, nullable=False)
    net_salary: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), default=PayrollStatusEnum.DRAFT, nullable=False
    )
    paid_on: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    employee: Mapped["EmployeeProfile"] = relationship(
        "EmployeeProfile", back_populates="payrolls"
    )

    __table_args__ = (
        UniqueConstraint(
            "employee_id", "month", "year",
            name="uq_payroll_employee_month_year",
        ),
    )

    def __repr__(self) -> str:
        return f"<EmployeePayroll employee={self.employee_id} {self.month}/{self.year}>"