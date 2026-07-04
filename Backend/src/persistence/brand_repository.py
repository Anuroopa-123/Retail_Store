from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select

from sqlalchemy.orm import joinedload

from src.domain.entities.product.brand import Brand

from src.domain.entities.product.product_category import ProductCategory


class BrandRepository:

    def __init__(
        self,
        db: AsyncSession
    ):
        self.db = db

    # ---------------------------------------
    # Get All Brands
    # ---------------------------------------

    async def get_all(
        self,
        tenant_id: int,
        store_id: int
    ):

        result = await self.db.execute(

            select(Brand)

            .options(
                joinedload(Brand.category)
            )

            .where(

                Brand.tenant_id == tenant_id,

                Brand.store_id == store_id

            )

            .order_by(
                Brand.id.desc()
            )

        )

        brands = result.scalars().all()

        return [

            {

                "id": brand.id,

                "tenant_id": brand.tenant_id,

                "store_id": brand.store_id,

                "category_id": brand.category_id,

                "category_name": (
                    brand.category.name
                    if brand.category
                    else ""
                ),

                "name": brand.name,

                "description": brand.description,

                "logo_url": brand.logo_url,

                "status": brand.status,

                "created_by": brand.created_by,

                "created_at": brand.created_at,

                "updated_at": brand.updated_at

            }

            for brand in brands

        ]

    # ---------------------------------------
    # Get Brand By Id
    # ---------------------------------------

    async def get_by_id(
        self,
        brand_id: int
    ):

        result = await self.db.execute(

            select(Brand)

            .options(
                joinedload(Brand.category)
            )

            .where(

                Brand.id == brand_id

            )

        )

        return result.scalar_one_or_none()

    # ---------------------------------------
    # Check Duplicate Brand
    # ---------------------------------------

    async def get_by_name(

        self,

        tenant_id: int,

        store_id: int,

        name: str

    ):

        result = await self.db.execute(

            select(Brand)

            .where(

                Brand.tenant_id == tenant_id,

                Brand.store_id == store_id,

                Brand.name == name

            )

        )

        return result.scalar_one_or_none()

    # ---------------------------------------
    # Create Brand
    # ---------------------------------------

    async def create(

        self,

        data

    ):

        brand = Brand(

            tenant_id=data.tenant_id,

            store_id=data.store_id,

            category_id=data.category_id,

            name=data.name,

            description=data.description,

            logo_url=data.logo_url,

            status=data.status,

            created_by=data.created_by

        )

        self.db.add(brand)

        await self.db.commit()

        await self.db.refresh(brand)

        return brand

    # ---------------------------------------
    # Update Brand
    # ---------------------------------------

    async def update(

        self,

        brand: Brand,

        data

    ):

        if data.category_id is not None:

            brand.category_id = data.category_id

        if data.name is not None:

            brand.name = data.name

        if data.description is not None:

            brand.description = data.description

        if data.logo_url is not None:

            brand.logo_url = data.logo_url

        if data.status is not None:

            brand.status = data.status

        await self.db.commit()

        await self.db.refresh(brand)

        return brand

    # ---------------------------------------
    # Delete Brand
    # ---------------------------------------

    async def delete(

        self,

        brand: Brand

    ):

        await self.db.delete(brand)

        await self.db.commit()

        return {

            "message": "Brand Deleted Successfully"

        }