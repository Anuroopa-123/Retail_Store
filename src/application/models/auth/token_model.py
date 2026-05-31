# src/application/models/auth/token_model.py
from __future__ import annotations

from src.application.models.core.base_model import BaseResponseModel, BasePostModel


class TokenResponse(BaseResponseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class RefreshTokenRequest(BasePostModel):
    refresh_token: str