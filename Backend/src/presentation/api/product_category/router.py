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

from src.application.services.product_category_service import (
    ProductCategoryService
)

from src.application.models.product.product_category_model import (
    ProductCategoryCreateRequest,
    ProductCategoryUpdateRequest
)

router = APIRouter(
    prefix="/product-categories",
    tags=["Product Categories"]
)


# ---------------------------------------------
# Get All Categories
# ---------------------------------------------
@router.get("/{tenant_id}/{store_id}")
async def get_categories(

    tenant_id: int,

    store_id: int,

    db: AsyncSession = Depends(get_session)

):

    service = ProductCategoryService(db)

    return await service.get_all(

        tenant_id,

        store_id

    )


# ---------------------------------------------
# Get Category By Id
# ---------------------------------------------
@router.get("/id/{category_id}")
async def get_category(

    category_id: int,

    db: AsyncSession = Depends(get_session)

):

    try:

        service = ProductCategoryService(db)

        return await service.get_by_id(

            category_id

        )

    except Exception as e:

        raise HTTPException(

            status_code=404,

            detail=str(e)

        )


# ---------------------------------------------
# Create Category
# ---------------------------------------------
@router.post("/")
async def create_category(

    payload: ProductCategoryCreateRequest,

    db: AsyncSession = Depends(get_session)

):

    try:

        service = ProductCategoryService(db)

        return await service.create(

            payload

        )

    except Exception as e:

        raise HTTPException(

            status_code=400,

            detail=str(e)

        )


# ---------------------------------------------
# Update Category
# ---------------------------------------------
@router.put("/{category_id}")
async def update_category(

    category_id: int,

    payload: ProductCategoryUpdateRequest,

    db: AsyncSession = Depends(get_session)

):

    try:

        service = ProductCategoryService(db)

        return await service.update(

            category_id,

            payload

        )

    except Exception as e:

        raise HTTPException(

            status_code=400,

            detail=str(e)

        )


# ---------------------------------------------
# Delete Category
# ---------------------------------------------
@router.delete("/{category_id}")
async def delete_category(

    category_id: int,

    db: AsyncSession = Depends(get_session)

):

    try:

        service = ProductCategoryService(db)

        return await service.delete(

            category_id

        )

    except Exception as e:

        raise HTTPException(

            status_code=400,

            detail=str(e)

        )