from enum import Enum
class PaymentMethodEnum(str, Enum):
    CASH   = "cash"
    CARD   = "card"
    UPI    = "upi"
    WALLET = "wallet"
    CREDIT = "credit"
