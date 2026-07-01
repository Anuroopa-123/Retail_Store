from datetime import date
from pydantic import BaseModel


class AdminProfileUpdateRequest(BaseModel):

    phone: str | None = None

    gender: str | None = None

    dob: date | None = None

    address: str | None = None

    city: str | None = None

    state: str | None = None

    country: str | None = None

    pincode: str | None = None

    photo: str | None = None