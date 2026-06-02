# src/presentation/api/roles/router.py
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.infrastructure.database.postgresql import get_session
from src.domain.entities.auth.role import Role
from src.domain.entities.user import User
from src.application.models.auth.role_model import (
    RoleResponse, AssignRoleRequest, AssignRoleBySlugModel
)
from src.application.services.user_service import UserService
from src.application.exception_handler import (
    UserNotFoundError,
    TenantAccessError,
)
from src.presentation.api.dependency import get_current_user, require_role

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get("/", response_model=list[RoleResponse])
async def list_roles(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    result = await db.execute(
        select(Role).where(Role.tenant_id == current_user.tenant_id)
    )
    return result.scalars().all()


@router.post("/assign", status_code=200)
async def assign_role(
    body: AssignRoleRequest,
    user_id: int,
    current_user: User = Depends(require_role("admin", "super_admin")),
    db: AsyncSession = Depends(get_session),
):
    service = UserService(db)

    # Check 3: role exists in current tenant
    role = await db.scalar(
        select(Role).where(
            Role.slug == body.role_slug,
            Role.tenant_id == current_user.tenant_id,
        )
    )
    if not role:
        raise HTTPException(
            status_code=404,
            detail=f"Role '{body.role_slug}' not found for this tenant",
        )

    # Check 4: only super_admin can assign super_admin
    if (
        role.slug == "super_admin"
        and not any(r.slug == "super_admin" for r in current_user.roles)
    ):
        raise HTTPException(
            status_code=403,
            detail="Only super admins can assign the super_admin role",
        )

    # Check 2 + assign — service owns tenant isolation
    try:
        await service.assign_role(
            user_id=user_id,
            data=AssignRoleBySlugModel(role_slug=body.role_slug),
            current_tenant_id=current_user.tenant_id,
        )
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    except TenantAccessError:
        raise HTTPException(status_code=403, detail="Cannot manage users from another tenant")

    await db.commit()

    return {"message": f"Role '{role.slug}' assigned to user {user_id} successfully"}