# src/domain/entities/subscription/subscription.py
from __future__ import annotations

from datetime import date, datetime
from typing import Optional
from sqlalchemy import String, ForeignKey, Date, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.domain.entities.base import BaseModel
from src.domain.enums import SubscriptionStatusEnum


class Subscription(BaseModel):
    __tablename__ = "subscriptions"

    customer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("customers.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    plan_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("subscription_plans.id"),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(20), default=SubscriptionStatusEnum.ACTIVE, nullable=False
    )
    trial_ends_at: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    current_period_start: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    current_period_end: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    cancelled_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    customer: Mapped["Customer"] = relationship("Customer", back_populates="subscriptions")
    plan: Mapped["SubscriptionPlan"] = relationship("SubscriptionPlan", back_populates="subscriptions")
    feature_overrides: Mapped[list["SubscriptionFeature"]] = relationship(
        "SubscriptionFeature", back_populates="subscription"
    )

    def __repr__(self) -> str:
        return f"<Subscription customer={self.customer_id} plan={self.plan_id}>"