from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from src.infrastructure.database.postgresql import (
    get_session
)

from src.application.services.brand_service import (
    BrandService
)

from src.application.models.brand.brand_model import (
    BrandCreateRequest,
    BrandUpdateRequest
)

router = APIRouter(
    prefix="/brands",
    tags=["Brands"]
)


# ---------------------------------------------
# Get All Brands
# ---------------------------------------------
@router.get("/{tenant_id}/{store_id}")
async def get_brands(

    tenant_id: int,

    store_id: int,

    db: AsyncSession = Depends(get_session)

):

    service = BrandService(db)

    return await service.get_all(

        tenant_id,

        store_id

    )


# ---------------------------------------------
# Get Brand By Id
# ---------------------------------------------
@router.get("/id/{brand_id}")
async def get_brand(

    brand_id: int,

    db: AsyncSession = Depends(get_session)

):

    try:

        service = BrandService(db)

        return await service.get_by_id(

            brand_id

        )

    except Exception as e:

        raise HTTPException(

            status_code=404,

            detail=str(e)

        )


# ---------------------------------------------
# Create Brand
# ---------------------------------------------
@router.post("/")
async def create_brand(

    payload: BrandCreateRequest,

    db: AsyncSession = Depends(get_session)

):

    try:

        service = BrandService(db)

        return await service.create(

            payload

        )

    except Exception as e:

        raise HTTPException(

            status_code=400,

            detail=str(e)

        )


# ---------------------------------------------
# Update Brand
# ---------------------------------------------
@router.put("/{brand_id}")
async def update_brand(

    brand_id: int,

    payload: BrandUpdateRequest,

    db: AsyncSession = Depends(get_session)

):

    try:

        service = BrandService(db)

        return await service.update(

            brand_id,

            payload

        )

    except Exception as e:

        raise HTTPException(

            status_code=400,

            detail=str(e)

        )


# ---------------------------------------------
# Delete Brand
# ---------------------------------------------
@router.delete("/{brand_id}")
async def delete_brand(

    brand_id: int,

    db: AsyncSession = Depends(get_session)

):

    try:

        service = BrandService(db)

        return await service.delete(

            brand_id

        )

    except Exception as e:

        raise HTTPException(

            status_code=400,

            detail=str(e)

        )