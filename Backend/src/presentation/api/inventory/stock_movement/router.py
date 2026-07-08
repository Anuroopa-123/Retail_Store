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

from src.application.services.stock_movement_service import (
    StockMovementService
)

from src.application.models.inventory.stock_movement_model import (
    StockMovementCreateRequest,
    StockMovementUpdateRequest
)

router = APIRouter(
    prefix="/stock-movements",
    tags=["Stock Movements"]
)


# ---------------------------------------------
# Get All Stock Movements
# ---------------------------------------------
@router.get("/{tenant_id}/{store_id}")
async def get_stock_movements(

    tenant_id: int,

    store_id: int,

    db: AsyncSession = Depends(get_session)

):

    service = StockMovementService(db)

    return await service.get_all(

        tenant_id,

        store_id

    )


# ---------------------------------------------
# Get Stock Movement By Id
# ---------------------------------------------
@router.get("/id/{movement_id}")
async def get_stock_movement(

    movement_id: int,

    db: AsyncSession = Depends(get_session)

):

    try:

        service = StockMovementService(db)

        return await service.get_by_id(

            movement_id

        )

    except Exception as e:

        raise HTTPException(

            status_code=404,

            detail=str(e)

        )


# ---------------------------------------------
# Create Stock Movement
# ---------------------------------------------
@router.post("/")
async def create_stock_movement(

    payload: StockMovementCreateRequest,

    db: AsyncSession = Depends(get_session)

):

    try:

        service = StockMovementService(db)

        return await service.create(

            payload

        )

    except Exception as e:

        raise HTTPException(

            status_code=400,

            detail=str(e)

        )


# ---------------------------------------------
# Update Stock Movement
# ---------------------------------------------
@router.put("/{movement_id}")
async def update_stock_movement(

    movement_id: int,

    payload: StockMovementUpdateRequest,

    db: AsyncSession = Depends(get_session)

):

    try:

        service = StockMovementService(db)

        return await service.update(

            movement_id,

            payload

        )

    except Exception as e:

        raise HTTPException(

            status_code=400,

            detail=str(e)

        )


# ---------------------------------------------
# Delete Stock Movement
# ---------------------------------------------
@router.delete("/{movement_id}")
async def delete_stock_movement(

    movement_id: int,

    db: AsyncSession = Depends(get_session)

):

    try:

        service = StockMovementService(db)

        return await service.delete(

            movement_id

        )

    except Exception as e:

        raise HTTPException(

            status_code=400,

            detail=str(e)

        )