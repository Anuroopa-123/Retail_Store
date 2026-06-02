# src/domain/enums/token_status_enum.py

from enum import Enum


class TokenStatusEnum(str, Enum):
    PENDING = "pending"
    USED = "used"
    EXPIRED = "expired"
    REVOKED = "revoked"