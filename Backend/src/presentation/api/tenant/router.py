from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from slugify import slugify

from src.infrastructure.database.postgresql import get_session
from src.domain.entities.tenant import Tenant
from pydantic import BaseModel

router = APIRouter(
    prefix="/tenants",
    tags=["Tenants"]
)


class TenantCreateRequest(BaseModel):
    name: str


@router.get("/")
async def list_tenants(
    db: AsyncSession = Depends(get_session)
):

    result = await db.execute(
        select(Tenant)
    )

    return result.scalars().all()


@router.post("/")
async def create_tenant(
    body: TenantCreateRequest,
    db: AsyncSession = Depends(get_session)
):

    tenant = Tenant(
        name=body.name,
        slug=slugify(body.name)
    )

    db.add(tenant)

    await db.commit()

    await db.refresh(tenant)

    return tenant