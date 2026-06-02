# src/domain/entities/auth/role_permission.py
from __future__ import annotations

from sqlalchemy import Table, Column, ForeignKey, DateTime, Integer, func
from src.domain.entities.base import BaseModel

role_permissions = Table(
    "role_permissions",
    BaseModel.metadata,
    Column(
        "role_id",
        Integer,
        ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "permission_id",
        Integer,
        ForeignKey("permissions.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "assigned_at",
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    ),
)