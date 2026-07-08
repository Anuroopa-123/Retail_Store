from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.inventory.stock_alert import (
    StockAlert
)


class StockAlertRepository:

    def __init__(
        self,
        db: AsyncSession
    ):
        self.db = db

    # ---------------------------------------
    # Get All Alerts
    # ---------------------------------------

    async def get_all(
        self,
        tenant_id: int,
        store_id: int
    ):

        result = await self.db.execute(

            select(StockAlert)

            .where(

                StockAlert.tenant_id == tenant_id,

                StockAlert.store_id == store_id

            )

            .order_by(

                StockAlert.id.desc()

            )

        )

        return result.scalars().all()

    # ---------------------------------------
    # Get Alert By Id
    # ---------------------------------------

    async def get_by_id(
        self,
        alert_id: int
    ):

        result = await self.db.execute(

            select(StockAlert)

            .where(

                StockAlert.id == alert_id

            )

        )

        return result.scalar_one_or_none()

    # ---------------------------------------
    # Get Alert By Product
    # ---------------------------------------

    async def get_by_product(

        self,

        tenant_id: int,

        store_id: int,

        product_id: int

    ):

        result = await self.db.execute(

            select(StockAlert)

            .where(

                StockAlert.tenant_id == tenant_id,

                StockAlert.store_id == store_id,

                StockAlert.product_id == product_id

            )

        )

        return result.scalar_one_or_none()

    # ---------------------------------------
    # Create Alert
    # ---------------------------------------

    async def create(
        self,
        data
    ):

        alert = StockAlert(

            tenant_id=data.tenant_id,

            store_id=data.store_id,

            product_id=data.product_id,

            current_qty=data.current_qty,

            threshold_qty=data.threshold_qty,

            alert_type=data.alert_type,

            status=data.status

        )

        self.db.add(alert)

        await self.db.commit()

        await self.db.refresh(alert)

        return alert

    # ---------------------------------------
    # Update Alert
    # ---------------------------------------

    async def update(

        self,

        alert: StockAlert,

        data

    ):

        if data.current_qty is not None:
            alert.current_qty = data.current_qty

        if data.threshold_qty is not None:
            alert.threshold_qty = data.threshold_qty

        if data.alert_type is not None:
            alert.alert_type = data.alert_type

        if data.status is not None:
            alert.status = data.status

        await self.db.commit()

        await self.db.refresh(alert)

        return alert

    # ---------------------------------------
    # Delete Alert
    # ---------------------------------------

    async def delete(

        self,

        alert: StockAlert

    ):

        await self.db.delete(alert)

        await self.db.commit()

        return {

            "message": "Stock Alert Deleted Successfully"

        }