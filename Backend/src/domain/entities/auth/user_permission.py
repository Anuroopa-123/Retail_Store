# src/domain/entities/auth/user_permission.py
from __future__ import annotations

from sqlalchemy import Table, Column, String, ForeignKey, DateTime, Integer, func
from src.domain.entities.base import BaseModel
from src.domain.enums import GrantTypeEnum

user_permissions = Table(
    "user_permissions",
    BaseModel.metadata,
    Column(
        "user_id",
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "permission_id",
        Integer,
        ForeignKey("permissions.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "grant_type",
        String(10),
        default=GrantTypeEnum.ALLOW,
        nullable=False,
    ),
    Column(
        "granted_at",
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    ),
)