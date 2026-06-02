# src/domain/entities/auth/user_role.py
from __future__ import annotations

from sqlalchemy import Table, Column, ForeignKey, DateTime, Integer, func
from src.domain.entities.base import BaseModel

user_roles = Table(
    "user_roles",
    BaseModel.metadata,
    Column(
        "user_id",
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "role_id",
        Integer,
        ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "assigned_at",
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    ),
)