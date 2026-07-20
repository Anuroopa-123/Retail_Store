from src.persistence.product_stock_repository import (
    ProductStockRepository
)


class ProductStockService:

    def __init__(

        self,

        db

    ):

        self.repository = ProductStockRepository(db)

    # ---------------------------------------
    # Get All Product Stock
    # ---------------------------------------

    async def get_all(

        self,

        store_id: int

    ):

        return await self.repository.get_all(

            store_id

        )

    # ---------------------------------------
    # Get Product Stock By Id
    # ---------------------------------------

    async def get_by_id(

        self,

        stock_id: int

    ):

        stock = await self.repository.get_by_id(

            stock_id

        )

        if not stock:

            raise Exception(

                "Product Stock Not Found"

            )

        return stock

    # ---------------------------------------
    # Get Product Stock
    # ---------------------------------------

    async def get_product_stock(

        self,

        product_id: int,

        store_id: int

    ):

        stock = await self.repository.get_product_stock(

            product_id,

            store_id

        )

        if not stock:

            raise Exception(

                "Product Stock Not Found"

            )

        return stock

    # ---------------------------------------
    # Create Product Stock
    # ---------------------------------------

    async def create(

        self,

        data

    ):

        existing = await self.repository.get_product_stock(

            data.product_id,

            data.store_id

        )

        if existing:

            raise Exception(

                "Product Stock Already Exists"

            )

        return await self.repository.create(

            data

        )

    # ---------------------------------------
    # Update Product Stock
    # ---------------------------------------

    async def update(

        self,

        stock_id: int,

        data

    ):

        stock = await self.repository.get_by_id(

            stock_id

        )

        if not stock:

            raise Exception(

                "Product Stock Not Found"

            )

        return await self.repository.update(

            stock,

            data

        )

    # ---------------------------------------
    # Update Stock Quantity
    # ---------------------------------------

    async def update_stock(

        self,

        product_id: int,

        store_id: int,

        quantity: int

    ):

        stock = await self.repository.get_product_stock(

            product_id,

            store_id

        )

        if not stock:

            raise Exception(

                "Product Stock Not Found"

            )

        stock.stock = quantity

        return await self.repository.update(

            stock,

            stock

        )

    # ---------------------------------------
    # Increase Stock
    # ---------------------------------------

    async def increase_stock(

        self,

        product_id: int,

        store_id: int,

        quantity: int

    ):

        stock = await self.repository.get_product_stock(

            product_id,

            store_id

        )

        if not stock:

            raise Exception(

                "Product Stock Not Found"

            )

        stock.stock += quantity

        return await self.repository.update(

            stock,

            stock

        )

    # ---------------------------------------
    # Decrease Stock
    # ---------------------------------------

    async def decrease_stock(

        self,

        product_id: int,

        store_id: int,

        quantity: int

    ):

        stock = await self.repository.get_product_stock(

            product_id,

            store_id

        )

        if not stock:

            raise Exception(

                "Product Stock Not Found"

            )

        if stock.stock < quantity:

            raise Exception(

                "Insufficient Stock"

            )

        stock.stock -= quantity

        return await self.repository.update(

            stock,

            stock

        )

    # ---------------------------------------
    # Delete Product Stock
    # ---------------------------------------

    async def delete(

        self,

        stock_id: int

    ):

        stock = await self.repository.get_by_id(

            stock_id

        )

        if not stock:

            raise Exception(

                "Product Stock Not Found"

            )

        return await self.repository.delete(

            stock

        )