from src.persistence.product_repository import (
    ProductRepository
)


class ProductService:

    def __init__(self, db):

        self.repository = ProductRepository(db)

    # ---------------------------------------
    # Get All Products
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
    # Get Product By Id
    # ---------------------------------------

    async def get_by_id(

        self,

        product_id: int

    ):

        product = await self.repository.get_by_id(

            product_id

        )

        if not product:

            raise Exception(

                "Product Not Found"

            )

        return product

    # ---------------------------------------
    # Create Product
    # ---------------------------------------

    async def create(

        self,

        data

    ):

        # Check duplicate product name
        existing = await self.repository.get_by_name(

            data.tenant_id,

            data.store_id,

            data.product_name

        )

        if existing:

            raise Exception(

                "Product Already Exists"

            )

        return await self.repository.create(

            data

        )

    # ---------------------------------------
    # Update Product
    # ---------------------------------------

    async def update(

        self,

        product_id: int,

        data

    ):

        product = await self.repository.get_by_id(

            product_id

        )

        if not product:

            raise Exception(

                "Product Not Found"

            )

        return await self.repository.update(

            product,

            data

        )

    # ---------------------------------------
    # Delete Product
    # ---------------------------------------

    async def delete(

        self,

        product_id: int

    ):

        product = await self.repository.get_by_id(

            product_id

        )

        if not product:

            raise Exception(

                "Product Not Found"

            )

        return await self.repository.delete(

            product

        )
