# src/domain/entities/subscription/subscription_plan.py
from __future__ import annotations

from sqlalchemy import String, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.domain.entities.base import BaseModel
from src.domain.enums import BillingCycleEnum, PlanStatusEnum


class SubscriptionPlan(BaseModel):
    __tablename__ = "subscription_plans"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    billing_cycle: Mapped[str] = mapped_column(
        String(20), default=BillingCycleEnum.MONTHLY, nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(20), default=PlanStatusEnum.ACTIVE, nullable=False
    )

    plan_features: Mapped[list["PlanFeature"]] = relationship(
        "PlanFeature", back_populates="plan"
    )
    subscriptions: Mapped[list["Subscription"]] = relationship(
        "Subscription", back_populates="plan"
    )

    def __repr__(self) -> str:
        return f"<SubscriptionPlan slug={self.slug}>"