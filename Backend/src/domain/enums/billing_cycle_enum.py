# src/domain/enums/billing_cycle_enum.py

from enum import Enum


class BillingCycleEnum(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"
    LIFETIME = "lifetime"