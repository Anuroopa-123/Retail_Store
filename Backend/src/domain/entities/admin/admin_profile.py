from sqlalchemy import Integer,String,Date,ForeignKey,Text
from sqlalchemy.orm import mapped_column,Mapped

from src.domain.entities.base import BaseModel

class AdminProfile(BaseModel):

    __tablename__="admin_profiles"

    user_id:Mapped[int]=mapped_column(
        Integer,
        ForeignKey("users.id"),
        unique=True
    )

    phone:Mapped[str]=mapped_column(
        String(20),
        nullable=True
    )

    gender:Mapped[str]=mapped_column(
        String(20),
        nullable=True
    )

    dob:Mapped[str]=mapped_column(
        Date,
        nullable=True
    )

    address:Mapped[str]=mapped_column(
        Text,
        nullable=True
    )

    city:Mapped[str]=mapped_column(
        String(100),
        nullable=True
    )

    state:Mapped[str]=mapped_column(
        String(100),
        nullable=True
    )

    country:Mapped[str]=mapped_column(
        String(100),
        nullable=True
    )

    pincode:Mapped[str]=mapped_column(
        String(20),
        nullable=True
    )

    photo:Mapped[str]=mapped_column(
        Text,
        nullable=True
    )