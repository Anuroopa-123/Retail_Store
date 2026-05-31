# src/domain/entities/subscription/feature.py
from __future__ import annotations

from typing import Optional
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from src.domain.entities.base import BaseModel
from src.domain.enums import FeatureValueTypeEnum


class Feature(BaseModel):
    __tablename__ = "features"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    value_type: Mapped[str] = mapped_column(
        String(20), default=FeatureValueTypeEnum.STRING, nullable=False
    )
    default_value: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    def __repr__(self) -> str:
        return f"<Feature slug={self.slug}>"