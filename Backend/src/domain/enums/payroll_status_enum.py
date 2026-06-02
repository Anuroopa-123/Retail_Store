from enum import Enum

class PayrollStatusEnum(str, Enum):
    DRAFT     = "draft"      # being calculated
    APPROVED  = "approved"   # manager approved
    PAID      = "paid"       # salary disbursed
