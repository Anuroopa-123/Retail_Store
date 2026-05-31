# src/domain/enums/tenant_status_enum.py

from enum import Enum


class TenantStatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"