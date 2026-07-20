from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.inventory.stock_movement import (
    StockMovement
)
from src.domain.entities.product.product_stock import (
    ProductStock
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
    # Get Stock Movement By Id
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

    async def create(self, data):

    # ---------------------------------------
    # Get Source Product Stock
    # ---------------------------------------

        result = await self.db.execute(

            select(ProductStock).where(

                ProductStock.product_id == data.product_id,

                ProductStock.store_id == data.store_id

            )

        )

        product_stock = result.scalar_one_or_none()

        if not product_stock:

            raise Exception("Product stock record not found")

        previous_stock = product_stock.stock

    # ---------------------------------------
    # STOCK IN
    # ---------------------------------------

        if data.movement_type == "STOCK_IN":

            product_stock.stock += data.quantity

    # ---------------------------------------
    # STOCK OUT
    # ---------------------------------------

        elif data.movement_type == "STOCK_OUT":

            if product_stock.stock < data.quantity:

                raise Exception("Insufficient Stock")

            product_stock.stock -= data.quantity

    # ---------------------------------------
    # ADJUSTMENT
    # ---------------------------------------

        elif data.movement_type == "ADJUSTMENT":

            product_stock.stock = data.current_qty

    # ---------------------------------------
    # TRANSFER
    # ---------------------------------------

        elif data.movement_type == "TRANSFER":

            if not data.destination_store_id:

                raise Exception("Destination store is required")

            if data.store_id == data.destination_store_id:

                raise Exception(
                    "Source and destination stores cannot be the same"
                )

            if product_stock.stock < data.quantity:

                raise Exception("Insufficient Stock")

        # Reduce stock from source store

            product_stock.stock -= data.quantity

        # ---------------------------------------
        # Find Destination Stock
        # ---------------------------------------

            destination_result = await self.db.execute(

                select(ProductStock).where(

                    ProductStock.product_id == data.product_id,

                    ProductStock.store_id == data.destination_store_id

                )

            )

            destination_stock = destination_result.scalar_one_or_none()

        # ---------------------------------------
        # Update Destination Stock
        # ---------------------------------------

            if destination_stock:

                destination_stock.stock += data.quantity

            else:

                destination_stock = ProductStock(

                    product_id=data.product_id,

                    store_id=data.destination_store_id,

                    stock=data.quantity,

                    minimum_stock=product_stock.minimum_stock

                )

                self.db.add(destination_stock)

    # ---------------------------------------
    # Invalid Movement Type
    # ---------------------------------------

        else:

            raise Exception("Invalid Stock Movement Type")

    # ---------------------------------------
    # Save Destination ProductStock
    # ---------------------------------------

        await self.db.flush()

    # ---------------------------------------
    # Create Stock Movement Entry
    # ---------------------------------------

        movement = StockMovement(

            tenant_id=data.tenant_id,

            store_id=data.store_id,

            destination_store_id=data.destination_store_id,

            product_id=data.product_id,

            movement_type=data.movement_type,

            quantity=data.quantity,

            previous_qty=previous_stock,

            current_qty=product_stock.stock,

            reference=data.reference,

            note=data.note,

            moved_by=data.moved_by

        )

        self.db.add(movement)

    # ---------------------------------------
    # Commit
    # ---------------------------------------

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

        if hasattr(data, "destination_store_id"):

            movement.destination_store_id = data.destination_store_id

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



