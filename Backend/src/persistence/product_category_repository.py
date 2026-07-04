from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select

from src.domain.entities.product.product_category import (
    ProductCategory
)


class ProductCategoryRepository:

    def __init__(
        self,
        db: AsyncSession
    ):
        self.db = db

    # ---------------------------------------
    # Get All Categories
    # ---------------------------------------

    async def get_all(
        self,
        tenant_id: int,
        store_id: int
    ):

        result = await self.db.execute(

            select(ProductCategory)

            .where(

                ProductCategory.tenant_id == tenant_id,

                ProductCategory.store_id == store_id

            )

            .order_by(
                ProductCategory.id.desc()
            )

        )

        return result.scalars().all()

    # ---------------------------------------
    # Get Category By Id
    # ---------------------------------------

    async def get_by_id(
        self,
        category_id: int
    ):

        result = await self.db.execute(

            select(ProductCategory)

            .where(

                ProductCategory.id == category_id

            )

        )

        return result.scalar_one_or_none()

    # ---------------------------------------
    # Check Duplicate Category
    # ---------------------------------------

    async def get_by_name(

        self,

        tenant_id: int,

        store_id: int,

        name: str

    ):

        result = await self.db.execute(

            select(ProductCategory)

            .where(

                ProductCategory.tenant_id == tenant_id,

                ProductCategory.store_id == store_id,

                ProductCategory.name == name

            )

        )

        return result.scalar_one_or_none()

    # ---------------------------------------
    # Create Category
    # ---------------------------------------

    async def create(
        self,
        data
    ):

        slug = (
            data.slug
            if data.slug
            else data.name.lower()
                .replace("&", "and")
                .replace(" ", "-")
        )

        category = ProductCategory(

            tenant_id=data.tenant_id,

            store_id=data.store_id,

            name=data.name,

            slug=slug,

            description=data.description,

            status=data.status,

            created_by=data.created_by

        )

        self.db.add(category)

        await self.db.commit()

        await self.db.refresh(category)

        return category

    # ---------------------------------------
    # Update Category
    # ---------------------------------------

    async def update(

        self,

        category: ProductCategory,

        data

    ):

        if data.name is not None:

            category.name = data.name
            category.slug = (
            data.name.lower()
            .replace("&", "and")
            .replace(" ", "-")
        )

        if data.description is not None:

            category.description = data.description

        if data.status is not None:

            category.status = data.status

        await self.db.commit()

        await self.db.refresh(category)

        return category

    # ---------------------------------------
    # Delete Category
    # ---------------------------------------

    async def delete(

        self,

        category: ProductCategory

    ):

        await self.db.delete(category)

        await self.db.commit()

        return {
            "message": "Category Deleted Successfully"
        }