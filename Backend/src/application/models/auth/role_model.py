# src/application/models/auth/role_model.py

from __future__ import annotations
from typing import List

from src.application.models.core.base_model import (
    BaseResponseModel,
    BasePostModel
)

class RoleResponse(BaseResponseModel):
    id: int
    name: str
    slug: str

class AssignRoleRequest(BasePostModel):
    role_slug: str

class AssignRolesModel(BasePostModel):
    role_ids: List[int]

class AssignRoleBySlugModel(BasePostModel):
    role_slug: str