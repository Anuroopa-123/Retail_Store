# src/domain/enums/customer_product_relation_enum.py

from enum import Enum


class CustomerProductRelationEnum(str, Enum):
    VIEWED = "viewed"
    CARTED = "carted"
    PURCHASED = "purchased"
    WISHLISTED = "wishlisted"
    REVIEWED = "reviewed"