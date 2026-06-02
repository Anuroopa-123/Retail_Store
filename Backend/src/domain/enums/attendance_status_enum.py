from enum import Enum

class AttendanceStatusEnum(str, Enum):
    PRESENT  = "present"
    ABSENT   = "absent"
    HALF_DAY = "half_day"
    LEAVE    = "leave"
    HOLIDAY  = "holiday"