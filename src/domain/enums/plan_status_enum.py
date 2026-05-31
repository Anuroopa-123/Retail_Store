# src/domain/enums/plan_status_enum.py

from enum import Enum


class PlanStatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"