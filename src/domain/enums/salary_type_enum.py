from enum import Enum

class SalaryTypeEnum(str, Enum):

    FIXED   = "fixed"    # monthly fixed salary
    HOURLY  = "hourly"   # paid per hour worked