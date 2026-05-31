# src/domain/entities/subscription/plan_feature.py
from __future__ import annotations

from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.domain.entities.base import BaseModel


class PlanFeature(BaseModel):
    __tablename__ = "plan_features"

    plan_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("subscription_plans.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    feature_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("features.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    value: Mapped[str] = mapped_column(String(255), nullable=False)

    plan: Mapped["SubscriptionPlan"] = relationship("SubscriptionPlan", back_populates="plan_features")
    feature: Mapped["Feature"] = relationship("Feature")

    def __repr__(self) -> str:
        return f"<PlanFeature plan={self.plan_id} feature={self.feature_id}>"