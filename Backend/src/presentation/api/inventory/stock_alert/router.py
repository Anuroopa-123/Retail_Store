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

from src.application.services.stock_alert_service import (
    StockAlertService
)

from src.application.models.inventory.stock_alert_model import (
    StockAlertCreateRequest,
    StockAlertUpdateRequest
)

router = APIRouter(
    prefix="/stock-alerts",
    tags=["Stock Alerts"]
)


# ---------------------------------------------
# Get All Stock Alerts
# ---------------------------------------------
@router.get("/{tenant_id}/{store_id}")
async def get_stock_alerts(

    tenant_id: int,

    store_id: int,

    db: AsyncSession = Depends(get_session)

):

    service = StockAlertService(db)

    return await service.get_all(

        tenant_id,

        store_id

    )


# ---------------------------------------------
# Get Stock Alert By Id
# ---------------------------------------------
@router.get("/id/{alert_id}")
async def get_stock_alert(

    alert_id: int,

    db: AsyncSession = Depends(get_session)

):

    try:

        service = StockAlertService(db)

        return await service.get_by_id(

            alert_id

        )

    except Exception as e:

        raise HTTPException(

            status_code=404,

            detail=str(e)

        )


# ---------------------------------------------
# Create Stock Alert
# ---------------------------------------------
@router.post("/")
async def create_stock_alert(

    payload: StockAlertCreateRequest,

    db: AsyncSession = Depends(get_session)

):

    try:

        service = StockAlertService(db)

        return await service.create(

            payload

        )

    except Exception as e:

        raise HTTPException(

            status_code=400,

            detail=str(e)

        )


# ---------------------------------------------
# Update Stock Alert
# ---------------------------------------------
@router.put("/{alert_id}")
async def update_stock_alert(

    alert_id: int,

    payload: StockAlertUpdateRequest,

    db: AsyncSession = Depends(get_session)

):

    try:

        service = StockAlertService(db)

        return await service.update(

            alert_id,

            payload

        )

    except Exception as e:

        raise HTTPException(

            status_code=400,

            detail=str(e)

        )


# ---------------------------------------------
# Delete Stock Alert
# ---------------------------------------------
@router.delete("/{alert_id}")
async def delete_stock_alert(

    alert_id: int,

    db: AsyncSession = Depends(get_session)

):

    try:

        service = StockAlertService(db)

        return await service.delete(

            alert_id

        )

    except Exception as e:

        raise HTTPException(

            status_code=400,

            detail=str(e)

        )