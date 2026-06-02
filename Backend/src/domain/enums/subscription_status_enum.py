# src/domain/enums/subscription_status_enum.py

from enum import Enum


class SubscriptionStatusEnum(str, Enum):
    ACTIVE = "active"
    TRIALING = "trialing"
    PAST_DUE = "past_due"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    PAUSED = "paused"