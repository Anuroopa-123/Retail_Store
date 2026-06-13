from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy import ForeignKey, Integer
from src.domain.entities.base import BaseModel

class Department(BaseModel):
    __tablename__ = "departments"

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="active"
    )
    
    
    tenant_id: Mapped[int] = mapped_column(
    Integer,
    ForeignKey("tenants.id"),
    nullable=False
    )

    store_id: Mapped[int] = mapped_column(
    Integer,
    ForeignKey("stores.id"),
    nullable=False
    )

    created_by: Mapped[int] = mapped_column(
    Integer,
    ForeignKey("users.id"),
    nullable=False
    )