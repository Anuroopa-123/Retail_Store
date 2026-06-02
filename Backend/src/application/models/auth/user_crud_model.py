# src/application/models/auth/user_crud_model.py
from __future__ import annotations

import re
from typing import Optional
from pydantic import EmailStr, field_validator
from src.application.models.core.base_model import BasePostModel, BasePatchModel
from src.domain.enums.user_status_enum import UserStatusEnum


class UserCreateModel(BasePostModel):
    tenant_id: int
    store_id: int
    email: EmailStr
    name: str
    password: str
    phone: Optional[str] = None

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("At least 8 characters")
        if not re.search(r"[A-Z]", v):
            raise ValueError("At least one uppercase letter")
        if not re.search(r"[0-9]", v):
            raise ValueError("At least one number")
        return v


class UserUpdateModel(BasePatchModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class UserPasswordUpdateModel(BasePostModel):
    current_password: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("At least 8 characters")
        if not re.search(r"[A-Z]", v):
            raise ValueError("At least one uppercase letter")
        if not re.search(r"[0-9]", v):
            raise ValueError("At least one number")
        return v


class UserStatusUpdateModel(BasePostModel):
    status: UserStatusEnum