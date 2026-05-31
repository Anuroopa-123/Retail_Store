# src/application/models/auth/permission_model.py
from __future__ import annotations

from src.application.models.core.base_model import BaseResponseModel


class PermissionResponse(BaseResponseModel):
    id: int
    name: str
    slug: str
    module: str