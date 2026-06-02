# src/presentation/api/auth/router.py
from __future__ import annotations

import secrets
from datetime import timedelta, datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError

from src.infrastructure.database.postgresql import get_session
from src.infrastructure.auth.security import (
    verify_password, create_access_token,
    create_refresh_token, decode_token,
)
from src.infrastructure.email_service import EmailService
from src.application.models.auth.auth_user_model import (
    RegisterRequest, LoginRequest,
    UserResponse, ChangePasswordRequest,
    ForgotPasswordRequest, ResetPasswordRequest,
)
from src.application.models.auth.token_model import (
    TokenResponse, RefreshTokenRequest,
)
from src.application.models.auth.user_crud_model import (
    UserCreateModel, UserPasswordUpdateModel,
)
from src.application.services.user_service import UserService
from src.application.exception_handler import TokenInvalidError, TokenExpiredError
from src.presentation.api.dependency import get_current_user
from src.configuration.config import config
from src.domain.entities.user import User
from sqlalchemy import select
from src.domain.entities.tenant import Tenant
from src.domain.entities.store import Store
from src.infrastructure.auth.security import hash_password


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    body: RegisterRequest,
    db: AsyncSession = Depends(get_session),
):
    tenant = await db.scalar(
        select(Tenant).where(Tenant.slug == body.tenant_slug)
    )
    if not tenant:
        raise HTTPException(404, f"Tenant '{body.tenant_slug}' not found")

    store = await db.scalar(
        select(Store).where(
            Store.id == body.store_id,
            Store.tenant_id == tenant.id,
        )
    )
    if not store:
        raise HTTPException(404, "Store not found")

    service = UserService(db)
    user = await service.register(
        UserCreateModel(
            tenant_id=tenant.id,
            store_id=store.id,
            email=body.email,
            name=body.name,
            password=body.password,
        )
    )

    raw_token = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + timedelta(hours=24)

    await service.create_email_verification_token(
        user_id=user.id,
        token_hash=raw_token,
        expires_at=expires_at,
    )

    await db.commit()

    try:
        await EmailService.send_verification_email(
            to=user.email,
            token=raw_token,
        )
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")

    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        status=user.status,
        tenant_id=user.tenant_id,
        store_id=user.store_id,
        roles=[r.slug for r in user.roles],
    )


@router.get("/verify-email")
async def verify_email(
    token: str,
    db: AsyncSession = Depends(get_session),
):
    service = UserService(db)

    try:
        await service.verify_email(token_hash=token)
    except TokenInvalidError:
        raise HTTPException(400, "Invalid or already used verification link")
    except TokenExpiredError:
        raise HTTPException(400, "Verification link has expired, please register again")

    await db.commit()

    return {"message": "Email verified successfully. You can now log in."}


@router.post("/login", response_model=TokenResponse)
async def login(
    body: LoginRequest,
    db: AsyncSession = Depends(get_session),
):
    service = UserService(db)
    user = await service.repository.get_authenticate_by_email(body.email)

    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(401, "Invalid email or password")

    if user.status != "active":
        raise HTTPException(403, "Account not verified. Please check your email.")

    return TokenResponse(
        access_token=create_access_token(
            str(user.id),
            timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES),
        ),
        refresh_token=create_refresh_token(
            str(user.id),
            timedelta(days=config.REFRESH_TOKEN_EXPIRE_DAYS),
        ),
        expires_in=config.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.get("/me", response_model=UserResponse)
async def me(current_user: User = Depends(get_current_user)):
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        name=current_user.name,
        status=current_user.status,
        tenant_id=current_user.tenant_id,
        store_id=current_user.store_id,
        roles=[r.slug for r in current_user.roles],
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    body: RefreshTokenRequest,
    db: AsyncSession = Depends(get_session),
):
    try:
        payload = decode_token(body.refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(401, "Invalid token type")
        user_id = int(payload.get("sub"))
    except (JWTError, TypeError, ValueError):
        raise HTTPException(401, "Invalid or expired refresh token")

    service = UserService(db)
    user = await service.get_by_id(user_id)

    return TokenResponse(
        access_token=create_access_token(
            str(user.id),
            timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES),
        ),
        refresh_token=create_refresh_token(
            str(user.id),
            timedelta(days=config.REFRESH_TOKEN_EXPIRE_DAYS),
        ),
        expires_in=config.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.post("/change-password", status_code=200)
async def change_password(
    body: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    service = UserService(db)
    await service.change_password(
        current_user.id,
        UserPasswordUpdateModel(
            current_password=body.current_password,
            new_password=body.new_password,
        ),
    )
    return {"message": "Password changed successfully"}


@router.post("/forgot-password", status_code=200)
async def forgot_password(
    body: ForgotPasswordRequest,
    db: AsyncSession = Depends(get_session),
):
    service = UserService(db)

    try:
        user = await service.get_by_email(body.email)
    except Exception:
        return {"message": "If that email exists, a reset link has been sent."}

    raw_token = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + timedelta(hours=1)

    await service.create_password_reset_token(
        user_id=user.id,
        token_hash=raw_token,
        expires_at=expires_at,
    )

    await db.commit()

    try:
        await EmailService.send_password_reset_email(
            to=user.email,
            token=raw_token,
        )
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")

    return {"message": "If that email exists, a reset link has been sent."}


@router.get("/reset-password", status_code=200)
async def reset_password_validate(
    token: str,
    db: AsyncSession = Depends(get_session),
):
    service = UserService(db)

    token_record = await service.get_password_reset_token(token_hash=token)
    if not token_record:
        raise HTTPException(400, "Invalid or expired reset link")

    expires_at = token_record.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if expires_at < datetime.now(timezone.utc):
        raise HTTPException(400, "Reset link has expired, please request a new one")

    if token_record.used_at:
        raise HTTPException(400, "Reset link has already been used")

    return {"message": "Token valid. Submit your new password.", "token": token}


@router.post("/reset-password", status_code=200)
async def reset_password(
    body: ResetPasswordRequest,
    db: AsyncSession = Depends(get_session),
):
    service = UserService(db)

    token_record = await service.get_password_reset_token(token_hash=body.token)
    if not token_record:
        raise HTTPException(400, "Invalid or expired reset link")

    expires_at = token_record.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if expires_at < datetime.now(timezone.utc):
        raise HTTPException(400, "Reset link has expired, please request a new one")

    if token_record.used_at:
        raise HTTPException(400, "Reset link has already been used")

    user = await service.get_by_id(token_record.user_id)
    user.password_hash = hash_password(body.new_password)
    db.add(user)

    token_record.used_at = datetime.now(timezone.utc)
    

    token_record.status = "used"   # ← add this
    db.add(token_record)


    await db.commit()

    return {"message": "Password reset successfully. You can now log in."}