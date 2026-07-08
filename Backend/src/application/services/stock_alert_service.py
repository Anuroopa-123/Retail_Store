from src.persistence.stock_alert_repository import (
    StockAlertRepository
)


class StockAlertService:

    def __init__(self, db):

        self.repository = StockAlertRepository(db)

    # ---------------------------------------
    # Get All Stock Alerts
    # ---------------------------------------

    async def get_all(

        self,

        tenant_id: int,

        store_id: int

    ):

        return await self.repository.get_all(

            tenant_id,

            store_id

        )

    # ---------------------------------------
    # Get Alert By Id
    # ---------------------------------------

    async def get_by_id(

        self,

        alert_id: int

    ):

        alert = await self.repository.get_by_id(

            alert_id

        )

        if not alert:

            raise Exception(

                "Stock Alert Not Found"

            )

        return alert

    # ---------------------------------------
    # Create Stock Alert
    # ---------------------------------------

    async def create(

        self,

        data

    ):

        existing = await self.repository.get_by_product(

            data.tenant_id,

            data.store_id,

            data.product_id

        )

        if existing:

            raise Exception(

                "Stock Alert Already Exists"

            )

        return await self.repository.create(

            data

        )

    # ---------------------------------------
    # Update Stock Alert
    # ---------------------------------------

    async def update(

        self,

        alert_id: int,

        data

    ):

        alert = await self.repository.get_by_id(

            alert_id

        )

        if not alert:

            raise Exception(

                "Stock Alert Not Found"

            )

        return await self.repository.update(

            alert,

            data

        )

    # ---------------------------------------
    # Delete Stock Alert
    # ---------------------------------------

    async def delete(

        self,

        alert_id: int

    ):

        alert = await self.repository.get_by_id(

            alert_id

        )

        if not alert:

            raise Exception(

                "Stock Alert Not Found"

            )

        return await self.repository.delete(

            alert

        )