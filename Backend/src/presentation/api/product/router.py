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

from src.application.services.product_service import (
    ProductService
)

from src.application.models.product.product_model import (
    ProductCreateRequest,
    ProductUpdateRequest
)

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


# ---------------------------------------------
# Get All Products
# ---------------------------------------------
@router.get("/{tenant_id}/{store_id}")
async def get_products(

    tenant_id: int,

    store_id: int,

    db: AsyncSession = Depends(get_session)

):

    service = ProductService(db)

    return await service.get_all(

        tenant_id,

        store_id

    )


# ---------------------------------------------
# Get Product By Id
# ---------------------------------------------
@router.get("/id/{product_id}")
async def get_product(

    product_id: int,

    db: AsyncSession = Depends(get_session)

):

    try:

        service = ProductService(db)

        return await service.get_by_id(

            product_id

        )

    except Exception as e:

        raise HTTPException(

            status_code=404,

            detail=str(e)

        )


# ---------------------------------------------
# Create Product
# ---------------------------------------------
@router.post("/")
async def create_product(

    payload: ProductCreateRequest,

    db: AsyncSession = Depends(get_session)

):

    try:

        service = ProductService(db)

        return await service.create(

            payload

        )

    except Exception as e:

        raise HTTPException(

            status_code=400,

            detail=str(e)

        )


# ---------------------------------------------
# Update Product
# ---------------------------------------------
@router.put("/{product_id}")
async def update_product(

    product_id: int,

    payload: ProductUpdateRequest,

    db: AsyncSession = Depends(get_session)

):

    try:

        service = ProductService(db)

        return await service.update(

            product_id,

            payload

        )

    except Exception as e:

        raise HTTPException(

            status_code=400,

            detail=str(e)

        )


# ---------------------------------------------
# Delete Product
# ---------------------------------------------
@router.delete("/{product_id}")
async def delete_product(

    product_id: int,

    db: AsyncSession = Depends(get_session)

):

    try:

        service = ProductService(db)

        return await service.delete(

            product_id

        )

    except Exception as e:

        raise HTTPException(

            status_code=400,

            detail=str(e)

        )