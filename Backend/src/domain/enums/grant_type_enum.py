# src/domain/enums/grant_type_enum.py

from enum import Enum


class GrantTypeEnum(str, Enum):
    ALLOW = "allow"
    DENY = "deny"