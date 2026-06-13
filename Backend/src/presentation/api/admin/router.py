from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import random

import secrets

from datetime import (
    datetime,
    timedelta,
    timezone
)

from src.application.services.user_service import UserService

from src.infrastructure.email_service import EmailService

from src.infrastructure.database.postgresql import get_session

from src.domain.entities.user import User
from src.domain.entities.auth.role import Role

from src.infrastructure.auth.security import (
    hash_password
)

from src.application.models.admin.admin_model import (
    CreateAdminRequest
)

router = APIRouter(
    prefix="/admins",
    tags=["Admins"]
)

@router.post("/")
async def create_admin(
    body: CreateAdminRequest,
    db: AsyncSession = Depends(get_session)
):

    user = User(
        tenant_id=body.tenant_id,
        store_id=body.store_id,
        name=body.name,
        email=body.email,
        password_hash=hash_password(
            body.password
        ),
        status="pending"
    )

    role = await db.scalar(
        select(Role).where(
            Role.slug == "admin",
            Role.tenant_id ==
            body.tenant_id
        )
    )

    user.roles.append(role)

    db.add(user)

    await db.commit()

    await db.refresh(user)
    
    service = UserService(db)

    raw_token =  str(
    random.randint(
        100000,
        999999
    )
)

    expires_at = (
    datetime.now(timezone.utc)
    + timedelta(minutes=1)
    )

    await service.create_email_verification_token(
    user_id=user.id,
    token_hash=raw_token,
    expires_at=expires_at,
    )

    await db.commit()
    try:

        await EmailService.send_verification_email(
        to=user.email,
        token=raw_token
        )

    except Exception as e:

        print(e)

    return user



@router.get("/")
async def list_admins(
    db: AsyncSession = Depends(get_session)
):

    result = await db.execute(
        select(User).options(
            selectinload(User.roles)
        )
    )

    users = result.scalars().all()

    admins = []

    for user in users:

        role_names = [
            role.slug
            for role in user.roles
        ]

        if "admin" in role_names:

            admins.append({
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "status": user.status,

                "tenant_id": user.tenant_id,
                "store_id": user.store_id
            })

    return admins