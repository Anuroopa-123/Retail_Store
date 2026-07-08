from src.persistence.stock_movement_repository import (
    StockMovementRepository
)


class StockMovementService:

    def __init__(self, db):

        self.repository = StockMovementRepository(db)

    # ---------------------------------------
    # Get All Stock Movements
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
    # Get Movement By Id
    # ---------------------------------------

    async def get_by_id(

        self,

        movement_id: int

    ):

        movement = await self.repository.get_by_id(

            movement_id

        )

        if not movement:

            raise Exception(

                "Stock Movement Not Found"

            )

        return movement

    # ---------------------------------------
    # Create Stock Movement
    # ---------------------------------------

    async def create(

        self,

        data

    ):

        return await self.repository.create(

            data

        )

    # ---------------------------------------
    # Update Stock Movement
    # ---------------------------------------

    async def update(

        self,

        movement_id: int,

        data

    ):

        movement = await self.repository.get_by_id(

            movement_id

        )

        if not movement:

            raise Exception(

                "Stock Movement Not Found"

            )

        return await self.repository.update(

            movement,

            data

        )

    # ---------------------------------------
    # Delete Stock Movement
    # ---------------------------------------

    async def delete(

        self,

        movement_id: int

    ):

        movement = await self.repository.get_by_id(

            movement_id

        )

        if not movement:

            raise Exception(

                "Stock Movement Not Found"

            )

        return await self.repository.delete(

            movement

        )