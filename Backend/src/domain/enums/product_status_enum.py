# src/domain/enums/product_status_enum.py

from enum import Enum


class ProductStatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    OUT_OF_STOCK = "out_of_stock"
    DISCONTINUED = "discontinued"
    DRAFT = "draft"