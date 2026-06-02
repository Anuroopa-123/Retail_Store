# src/application/models/auth/auth_user_model.py
from __future__ import annotations

import re
from typing import Optional
from pydantic import EmailStr, field_validator
from src.application.models.core.base_model import BaseResponseModel, BasePostModel
from src.domain.enums.user_status_enum import UserStatusEnum


class RegisterRequest(BasePostModel):
    name: str
    email: EmailStr
    password: str
    tenant_slug: str
    store_id: int

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


class LoginRequest(BasePostModel):
    email: EmailStr
    password: str


class UserResponse(BaseResponseModel):
    id: int
    email: str
    name: str
    status: UserStatusEnum
    tenant_id: int
    store_id: Optional[int]
    roles: list[str]


class ChangePasswordRequest(BasePostModel):
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
    

class ForgotPasswordRequest(BasePostModel):
    email: str

class ResetPasswordRequest(BasePostModel):
    token: str
    new_password: str