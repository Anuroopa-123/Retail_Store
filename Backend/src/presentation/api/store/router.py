from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from slugify import slugify
from pydantic import BaseModel

from src.infrastructure.database.postgresql import get_session
from src.domain.entities.store import Store
from src.domain.entities.tenant import Tenant

router = APIRouter(
    prefix="/stores",
    tags=["Stores"]
)


class StoreCreateRequest(BaseModel):
    tenant_id: int
    name: str
    email: str | None = None
    phone: str | None = None


@router.get("/")
async def list_stores(
    db: AsyncSession = Depends(get_session)
):
    result = await db.execute(
        select(Store)
    )

    return result.scalars().all()


@router.post("/")
async def create_store(
    body: StoreCreateRequest,
    db: AsyncSession = Depends(get_session)
):

    tenant = await db.get(
        Tenant,
        body.tenant_id
    )

    if not tenant:
        return {
            "message": "Tenant not found"
        }

    store = Store(
        tenant_id=body.tenant_id,
        name=body.name,
        slug=slugify(body.name),
        email=body.email,
        phone=body.phone
    )

    db.add(store)

    await db.commit()

    await db.refresh(store)

    return store