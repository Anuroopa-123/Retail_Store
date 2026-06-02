# src/domain/enums/role_slug_enum.py

from enum import Enum


class RoleSlugEnum(str, Enum):
    SUPERADMIN = "superadmin"
    ADMIN = "admin"
    STORE_MANAGER = "store_manager"
    INVENTORY_MANAGER = "inventory_manager"
    CASHIER = "cashier"
    DELIVERY_STAFF = "delivery_staff"