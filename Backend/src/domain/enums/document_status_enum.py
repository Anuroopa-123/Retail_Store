from enum import Enum


class DocumentStatusEnum(str, Enum):
    ACTIVE  = "active"
    DELETED = "deleted"
