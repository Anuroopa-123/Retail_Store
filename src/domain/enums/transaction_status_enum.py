from enum import Enum
class TransactionStatusEnum(str, Enum):
    COMPLETED = "completed"
    REFUNDED  = "refunded"
    CANCELLED = "cancelled"
    PENDING   = "pending"
