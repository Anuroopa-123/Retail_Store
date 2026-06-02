from enum import Enum
class SettingTypeEnum(str, Enum):
    STRING  = "string"
    BOOLEAN = "boolean"
    INTEGER = "integer"
    JSON    = "json"