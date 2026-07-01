from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.postgresql import (
    get_session
)

from src.application.services.admin_profile_service import (
    AdminProfileService
)

from src.application.models.admin.admin_profile_model import (
    AdminProfileUpdateRequest
)

from src.presentation.api.dependency import get_current_user
from src.domain.entities.user import User

router = APIRouter(

    prefix="/admin/profile",

    tags=["Admin Profile"]

)


@router.get("/")

async def get_profile(

    current_user: User = Depends(
        get_current_user
    ),

    db: AsyncSession = Depends(
        get_session
    )

):

    service = AdminProfileService(db)

    return await service.get_profile(
        current_user.id
    )


@router.put("/")

async def update_profile(

    body: AdminProfileUpdateRequest,

    current_user: User = Depends(
        get_current_user
    ),

    db: AsyncSession = Depends(
        get_session
    )

):

    service = AdminProfileService(db)

    return await service.update_profile(

        current_user,

        body

    )