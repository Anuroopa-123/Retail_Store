# src/domain/enums/feature_value_type_enum.py

from enum import Enum


class FeatureValueTypeEnum(str, Enum):
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    JSON = "json"