# src/presentation/api/user/router.py
from __future__ import annotations

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.postgresql import get_session
from src.domain.entities.user import User
from src.application.models.auth.auth_user_model import UserResponse
from src.application.models.auth.user_crud_model import UserStatusUpdateModel
from src.application.services.user_service import UserService
from src.presentation.api.dependency import get_current_user, require_role

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserResponse])
async def list_users(
    store_id: Optional[int] = Query(None),
    limit: int = Query(50),
    offset: int = Query(0),
    current_user: User = Depends(require_role("admin", "super_admin", "store_manager")),
    db: AsyncSession = Depends(get_session),
):
    service = UserService(db)
    result = await service.get_all_by_tenant(
        tenant_id=current_user.tenant_id,
        store_id=store_id,
        limit=limit,
        offset=offset,
    )
    return [
        UserResponse(
            id=u.id,
            email=u.email,
            name=u.name,
            status=u.status,
            tenant_id=u.tenant_id,
            store_id=u.store_id,
            roles=[r.slug for r in u.roles],
        )
        for u in result["data"]
    ]


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: User = Depends(require_role("admin", "super_admin", "store_manager")),
    db: AsyncSession = Depends(get_session),
):
    service = UserService(db)
    user = await service.get_by_id(user_id)

    if user.tenant_id != current_user.tenant_id:
        raise HTTPException(404, "User not found")

    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        status=user.status,
        tenant_id=user.tenant_id,
        store_id=user.store_id,
        roles=[r.slug for r in user.roles],
    )


@router.patch("/{user_id}/status", status_code=200)
async def update_status(
    user_id: int,
    body: UserStatusUpdateModel,
    current_user: User = Depends(require_role("admin", "super_admin")),
    db: AsyncSession = Depends(get_session),
):
    service = UserService(db)
    user = await service.get_by_id(user_id)

    if user.tenant_id != current_user.tenant_id:
        raise HTTPException(404, "User not found")

    await service.update_status(user_id, body)
    return {"message": f"User status updated to '{body.status}'"}


@router.delete("/{user_id}", status_code=200)
async def soft_delete_user(
    user_id: int,
    current_user: User = Depends(require_role("admin", "super_admin")),
    db: AsyncSession = Depends(get_session),
):
    if user_id == current_user.id:
        raise HTTPException(400, "You cannot delete yourself")

    service = UserService(db)
    user = await service.get_by_id(user_id)

    if user.tenant_id != current_user.tenant_id:
        raise HTTPException(404, "User not found")

    await service.soft_delete(user_id)
    await db.commit()  # ← add this

    return {"message": "User deactivated successfully"}