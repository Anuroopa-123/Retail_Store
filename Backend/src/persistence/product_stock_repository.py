from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import (
    select
)

from sqlalchemy.orm import (
    joinedload
)

from src.domain.entities.inventory.product_stock import (
    ProductStock
)


class ProductStockRepository:

    def __init__(

        self,

        db: AsyncSession

    ):

        self.db = db

    # -----------------------------------------
    # Get All
    # -----------------------------------------

    async def get_all(

        self,

        store_id: int

    ):

        result = await self.db.execute(

            select(ProductStock)

            .options(

                joinedload(ProductStock.product),

                joinedload(ProductStock.store)

            )

            .where(

                ProductStock.store_id == store_id

            )

            .order_by(

                ProductStock.id.desc()

            )

        )

        return result.scalars().all()

    # -----------------------------------------
    # Get By Id
    # -----------------------------------------

    async def get_by_id(

        self,

        stock_id: int

    ):

        result = await self.db.execute(

            select(ProductStock)

            .where(

                ProductStock.id == stock_id

            )

        )

        return result.scalar_one_or_none()

    # -----------------------------------------
    # Get Product In Store
    # -----------------------------------------

    async def get_product_stock(

        self,

        product_id: int,

        store_id: int

    ):

        result = await self.db.execute(

            select(ProductStock)

            .where(

                ProductStock.product_id == product_id,

                ProductStock.store_id == store_id

            )

        )

        return result.scalar_one_or_none()

    # -----------------------------------------
    # Create
    # -----------------------------------------

    async def create(

        self,

        data

    ):

        stock = ProductStock(

            product_id=data.product_id,

            store_id=data.store_id,

            stock=data.stock,

            minimum_stock=data.minimum_stock

        )

        self.db.add(stock)

        await self.db.commit()

        await self.db.refresh(stock)

        return stock

    # -----------------------------------------
    # Update
    # -----------------------------------------

    async def update(

        self,

        stock: ProductStock,

        data

    ):

        if data.stock is not None:

            stock.stock = data.stock

        if data.minimum_stock is not None:

            stock.minimum_stock = data.minimum_stock

        await self.db.commit()

        await self.db.refresh(stock)

        return stock

    # -----------------------------------------
    # Delete
    # -----------------------------------------

    async def delete(

        self,

        stock: ProductStock

    ):

        await self.db.delete(stock)

        await self.db.commit()

        return {

            "message": "Product Stock Deleted Successfully"

        }