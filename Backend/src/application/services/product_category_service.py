from src.persistence.product_category_repository import (
    ProductCategoryRepository
)


class ProductCategoryService:

    def __init__(self, db):
        self.repository = ProductCategoryRepository(db)

    # ---------------------------------------
    # Get All Categories
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
    # Get Category By Id
    # ---------------------------------------

    async def get_by_id(
        self,
        category_id: int
    ):

        category = await self.repository.get_by_id(
            category_id
        )

        if not category:

            raise Exception(
                "Category Not Found"
            )

        return category

    # ---------------------------------------
    # Create Category
    # ---------------------------------------

    async def create(
        self,
        data
    ):

        # Check Duplicate Category

        existing = await self.repository.get_by_name(

            data.tenant_id,

            data.store_id,

            data.name

        )

        if existing:

            raise Exception(
                "Category Already Exists"
            )

        return await self.repository.create(data)

    # ---------------------------------------
    # Update Category
    # ---------------------------------------

    async def update(
        self,
        category_id: int,
        data
    ):

        category = await self.repository.get_by_id(
            category_id
        )

        if not category:

            raise Exception(
                "Category Not Found"
            )

        return await self.repository.update(

            category,

            data

        )

    # ---------------------------------------
    # Delete Category
    # ---------------------------------------

    async def delete(
        self,
        category_id: int
    ):

        category = await self.repository.get_by_id(
            category_id
        )

        if not category:

            raise Exception(
                "Category Not Found"
            )

        return await self.repository.delete(
            category
        )