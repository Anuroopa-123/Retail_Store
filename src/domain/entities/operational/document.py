# src/domain/entities//document.py
from __future__ import annotations

from typing import Optional
from sqlalchemy import String, ForeignKey, Text, BigInteger, Index, Integer
from sqlalchemy.orm import Mapped, mapped_column
from src.domain.entities.base import BaseModel
from src.domain.enums import DocumentStatusEnum


class Document(BaseModel):
    __tablename__ = "documents"

    tenant_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    uploaded_by: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    model_type: Mapped[str] = mapped_column(String(100), nullable=False)
    model_id: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(Text, nullable=False)
    mime_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    size_bytes: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    status: Mapped[str] = mapped_column(
        String(20), default=DocumentStatusEnum.ACTIVE, nullable=False
    )

    __table_args__ = (
        Index("ix_document_model_type_model_id", "model_type", "model_id"),
    )

    def __repr__(self) -> str:
        return f"<Document model={self.model_type} model_id={self.model_id}>"