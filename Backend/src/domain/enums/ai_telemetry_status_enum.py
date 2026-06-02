from enum import Enum

class AITelemetryStatusEnum(str, Enum):
    SUCCESS = "success"
    FAILED  = "failed"
    TIMEOUT = "timeout"
