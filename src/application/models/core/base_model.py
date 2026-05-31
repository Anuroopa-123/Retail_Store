# src/application/models/core/base_model.py
from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel
from pydantic.alias_generators import to_snake


class BaseResponseModel(BaseModel):
    model_config = {
        "alias_generator": to_snake,
        "from_attributes": True,
        "populate_by_name": True,
        "protected_namespaces": (),
        "json_encoders": {
            datetime: lambda v: v.isoformat(),
        },
    }


class BasePostModel(BaseModel):
    model_config = {
        "alias_generator": to_snake,
        "populate_by_name": True,
        "extra": "forbid",
        "protected_namespaces": (),
    }


class BasePatchModel(BasePostModel):
    pass