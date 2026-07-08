from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.inventory.stock_movement import (
    StockMovement
)


class StockMovementRepository:

    def __init__(
        self,
        db: AsyncSession
    ):
        self.db = db

    # ---------------------------------------
    # Get All Stock Movements
    # ---------------------------------------

    async def get_all(

        self,

        tenant_id: int,

        store_id: int

    ):

        result = await self.db.execute(

            select(StockMovement)

            .where(

                StockMovement.tenant_id == tenant_id,

                StockMovement.store_id == store_id

            )

            .order_by(

                StockMovement.id.desc()

            )

        )

        return result.scalars().all()

    # ---------------------------------------
    # Get Movement By Id
    # ---------------------------------------

    async def get_by_id(

        self,

        movement_id: int

    ):

        result = await self.db.execute(

            select(StockMovement)

            .where(

                StockMovement.id == movement_id

            )

        )

        return result.scalar_one_or_none()

    # ---------------------------------------
    # Create Stock Movement
    # ---------------------------------------

    async def create(

        self,

        data

    ):

        movement = StockMovement(

            tenant_id=data.tenant_id,

            store_id=data.store_id,

            product_id=data.product_id,

            movement_type=data.movement_type,

            quantity=data.quantity,

            previous_qty=data.previous_qty,

            current_qty=data.current_qty,

            reference=data.reference,

            note=data.note,

            moved_by=data.moved_by

        )

        self.db.add(movement)

        await self.db.commit()

        await self.db.refresh(movement)

        return movement

    # ---------------------------------------
    # Update Stock Movement
    # ---------------------------------------

    async def update(

        self,

        movement: StockMovement,

        data

    ):

        if data.movement_type is not None:
            movement.movement_type = data.movement_type

        if data.quantity is not None:
            movement.quantity = data.quantity

        if data.previous_qty is not None:
            movement.previous_qty = data.previous_qty

        if data.current_qty is not None:
            movement.current_qty = data.current_qty

        if data.reference is not None:
            movement.reference = data.reference

        if data.note is not None:
            movement.note = data.note

        if data.moved_by is not None:
            movement.moved_by = data.moved_by

        await self.db.commit()

        await self.db.refresh(movement)

        return movement

    # ---------------------------------------
    # Delete Stock Movement
    # ---------------------------------------

    async def delete(

        self,

        movement: StockMovement

    ):

        await self.db.delete(movement)

        await self.db.commit()

        return {

            "message": "Stock Movement Deleted Successfully"

        }