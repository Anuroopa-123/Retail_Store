from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from src.application.exception_handler import (
    TenantAccessError,
    UserNotFoundError
)

from src.application.models.auth.role_model import (
    AssignRoleBySlugModel,
    AssignRoleRequest
)

from src.application.services.user_service import (
    UserService
)

from src.domain.entities.user import User

from src.presentation.api.dependency import (
    require_role
)
from slugify import slugify

from src.infrastructure.database.postgresql import get_session
from src.domain.entities.auth.role import Role

router = APIRouter(
    prefix="/roles",
    tags=["Roles"]
)

class CreateRoleRequest(BaseModel):
    tenant_id: int
    name: str

class UpdateRoleRequest(BaseModel):
    name: str


@router.get("/")
async def list_roles(
    db: AsyncSession = Depends(get_session)
):
    result = await db.execute(
        select(Role)
    )

    return result.scalars().all()
@router.post("/create")
async def create_role(
    body: CreateRoleRequest,
    db: AsyncSession = Depends(get_session)
):
    try:

        print("BODY =", body)

        role = Role(
            tenant_id=body.tenant_id,
            name=body.name,
            slug=slugify(body.name)
        )

        db.add(role)

        await db.commit()

        await db.refresh(role)

        return role

    except Exception as e:
        print("ROLE CREATE ERROR =", repr(e))
        raise


@router.put("/{role_id}")
async def update_role(
    role_id: int,
    body: UpdateRoleRequest,
    db: AsyncSession = Depends(get_session)
):

    role = await db.get(
        Role,
        role_id
    )

    if not role:
        raise HTTPException(
            status_code=404,
            detail="Role not found"
        )

    role.name = body.name
    role.slug = slugify(body.name)

    await db.commit()

    await db.refresh(role)

    return role


@router.delete("/{role_id}")
async def delete_role(
    role_id: int,
    db: AsyncSession = Depends(get_session)
):

    role = await db.get(
        Role,
        role_id
    )

    if not role:
        raise HTTPException(
            status_code=404,
            detail="Role not found"
        )

    await db.delete(role)

    await db.commit()

    return {
        "message":
        "Role deleted successfully"
    }

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