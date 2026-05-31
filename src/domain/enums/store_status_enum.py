from enum import Enum
# src/domain/enums/__init__.py — add this

class StoreStatusEnum(str, Enum):
    ACTIVE   = "active"
    INACTIVE = "inactive"
    CLOSED   = "closed"