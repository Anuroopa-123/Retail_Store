from src.persistence.brand_repository import (
    BrandRepository
)


class BrandService:

    def __init__(self, db):
        self.repository = BrandRepository(db)

    # ---------------------------------------
    # Get All Brands
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
    # Get Brand By Id
    # ---------------------------------------

    async def get_by_id(
        self,
        brand_id: int
    ):

        brand = await self.repository.get_by_id(
            brand_id
        )

        if not brand:

            raise Exception(
                "Brand Not Found"
            )

        return brand

    # ---------------------------------------
    # Create Brand
    # ---------------------------------------

    async def create(
        self,
        data
    ):

        # Check Duplicate Brand

        existing = await self.repository.get_by_name(

            data.tenant_id,

            data.store_id,

            data.name

        )

        if existing:

            raise Exception(
                "Brand Already Exists"
            )

        return await self.repository.create(
            data
        )

    # ---------------------------------------
    # Update Brand
    # ---------------------------------------

    async def update(
        self,
        brand_id: int,
        data
    ):

        brand = await self.repository.get_by_id(
            brand_id
        )

        if not brand:

            raise Exception(
                "Brand Not Found"
            )

        return await self.repository.update(

            brand,

            data

        )

    # ---------------------------------------
    # Delete Brand
    # ---------------------------------------

    async def delete(
        self,
        brand_id: int
    ):

        brand = await self.repository.get_by_id(
            brand_id
        )

        if not brand:

            raise Exception(
                "Brand Not Found"
            )

        return await self.repository.delete(
            brand
        )