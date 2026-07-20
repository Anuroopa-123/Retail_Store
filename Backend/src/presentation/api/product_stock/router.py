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

from src.application.services.product_stock_service import (
    ProductStockService
)

from src.application.models.inventory.product_stock_model import (
    ProductStockCreateRequest,
    ProductStockUpdateRequest
)

router = APIRouter(

    prefix="/product-stock",

    tags=["Product Stock"]

)


# --------------------------------------------------
# Get All Product Stock By Store
# --------------------------------------------------

@router.get("/{store_id}")
async def get_product_stock(

    store_id: int,

    db: AsyncSession = Depends(get_session)

):

    service = ProductStockService(db)

    return await service.get_all(

        store_id

    )


# --------------------------------------------------
# Get Product Stock By Id
# --------------------------------------------------

@router.get("/id/{stock_id}")
async def get_product_stock_by_id(

    stock_id: int,

    db: AsyncSession = Depends(get_session)

):

    try:

        service = ProductStockService(db)

        return await service.get_by_id(

            stock_id

        )

    except Exception as e:

        raise HTTPException(

            status_code=404,

            detail=str(e)

        )


# --------------------------------------------------
# Get Product Stock By Product & Store
# --------------------------------------------------

@router.get("/product/{product_id}/{store_id}")
async def get_stock(

    product_id: int,

    store_id: int,

    db: AsyncSession = Depends(get_session)

):

    try:

        service = ProductStockService(db)

        return await service.get_product_stock(

            product_id,

            store_id

        )

    except Exception as e:

        raise HTTPException(

            status_code=404,

            detail=str(e)

        )


# --------------------------------------------------
# Create Product Stock
# --------------------------------------------------

@router.post("/")
async def create_product_stock(

    payload: ProductStockCreateRequest,

    db: AsyncSession = Depends(get_session)

):

    try:

        service = ProductStockService(db)

        return await service.create(

            payload

        )

    except Exception as e:

        raise HTTPException(

            status_code=400,

            detail=str(e)

        )


# --------------------------------------------------
# Update Product Stock
# --------------------------------------------------

@router.put("/{stock_id}")
async def update_product_stock(

    stock_id: int,

    payload: ProductStockUpdateRequest,

    db: AsyncSession = Depends(get_session)

):

    try:

        service = ProductStockService(db)

        return await service.update(

            stock_id,

            payload

        )

    except Exception as e:

        raise HTTPException(

            status_code=400,

            detail=str(e)

        )


# --------------------------------------------------
# Delete Product Stock
# --------------------------------------------------

@router.delete("/{stock_id}")
async def delete_product_stock(

    stock_id: int,

    db: AsyncSession = Depends(get_session)

):

    try:

        service = ProductStockService(db)

        return await service.delete(

            stock_id

        )

    except Exception as e:

        raise HTTPException(

            status_code=400,

            detail=str(e)

        )


# --------------------------------------------------
# Increase Stock
# --------------------------------------------------

@router.put("/increase/{product_id}/{store_id}/{quantity}")
async def increase_stock(

    product_id: int,

    store_id: int,

    quantity: int,

    db: AsyncSession = Depends(get_session)

):

    try:

        service = ProductStockService(db)

        return await service.increase_stock(

            product_id,

            store_id,

            quantity

        )

    except Exception as e:

        raise HTTPException(

            status_code=400,

            detail=str(e)

        )


# --------------------------------------------------
# Decrease Stock
# --------------------------------------------------

@router.put("/decrease/{product_id}/{store_id}/{quantity}")
async def decrease_stock(

    product_id: int,

    store_id: int,

    quantity: int,

    db: AsyncSession = Depends(get_session)

):

    try:

        service = ProductStockService(db)

        return await service.decrease_stock(

            product_id,

            store_id,

            quantity

        )

    except Exception as e:

        raise HTTPException(

            status_code=400,

            detail=str(e)

        )


# --------------------------------------------------
# Set Exact Stock
# --------------------------------------------------

@router.put("/set/{product_id}/{store_id}/{quantity}")
async def set_stock(

    product_id: int,

    store_id: int,

    quantity: int,

    db: AsyncSession = Depends(get_session)

):

    try:

        service = ProductStockService(db)

        return await service.update_stock(

            product_id,

            store_id,

            quantity

        )

    except Exception as e:

        raise HTTPException(

            status_code=400,

            detail=str(e)

        )