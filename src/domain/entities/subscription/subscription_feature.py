# src/domain/entities/subscription/subscription_feature.py
from __future__ import annotations

from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.domain.entities.base import BaseModel


class SubscriptionFeature(BaseModel):
    __tablename__ = "subscription_features"

    subscription_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("subscriptions.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    feature_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("features.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    value: Mapped[str] = mapped_column(String(255), nullable=False)

    subscription: Mapped["Subscription"] = relationship("Subscription", back_populates="feature_overrides")
    feature: Mapped["Feature"] = relationship("Feature")

    def __repr__(self) -> str:
        return f"<SubscriptionFeature subscription={self.subscription_id} feature={self.feature_id}>"