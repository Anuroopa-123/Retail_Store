from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import (
    select,
    func
)

from sqlalchemy.orm import (
    joinedload
)

from src.domain.entities.product.product import Product


class ProductRepository:

    def __init__(self, db: AsyncSession):

        self.db = db

    # ----------------------------------
    # Get All Products
    # ----------------------------------

    async def get_all(

        self,

        tenant_id: int,

        store_id: int

    ):

        result = await self.db.execute(

            select(Product)

            .options(

                joinedload(Product.category),

                joinedload(Product.brand)

            )

            .where(

                Product.tenant_id == tenant_id,

                Product.store_id == store_id

            )

            .order_by(

                Product.id.desc()

            )

        )

        return result.scalars().all()

    # ----------------------------------
    # Get Product By Id
    # ----------------------------------

    async def get_by_id(

        self,

        product_id: int

    ):

        result = await self.db.execute(

            select(Product)

            .where(

                Product.id == product_id

            )

        )

        return result.scalar_one_or_none()

    # ----------------------------------
    # Check Duplicate Product
    # ----------------------------------

    async def get_by_name(

        self,

        tenant_id: int,

        store_id: int,

        product_name: str

    ):

        result = await self.db.execute(

            select(Product)

            .where(

                Product.tenant_id == tenant_id,

                Product.store_id == store_id,

                Product.product_name == product_name

            )

        )

        return result.scalar_one_or_none()

    # ----------------------------------
    # Create Product
    # ----------------------------------

    async def create(

        self,

        data

    ):

        total = await self.db.scalar(

            select(func.count(Product.id))

        )

        sku = f"SKU{total+1:05d}"

        barcode = f"890000000{total+1:04d}"

        product = Product(

            tenant_id=data.tenant_id,

            store_id=data.store_id,

            category_id=data.category_id,

            brand_id=data.brand_id,

            product_name=data.product_name,

            sku=sku,

            barcode=barcode,

            purchase_price=data.purchase_price,

            selling_price=data.selling_price,

            tax=data.tax,

            stock=data.stock,

            minimum_stock=data.minimum_stock,

            unit=data.unit,

            image_url=data.image_url,

            description=data.description,

            status=data.status,

            created_by=data.created_by

        )

        self.db.add(product)

        await self.db.commit()

        await self.db.refresh(product)

        return product

    # ----------------------------------
    # Update Product
    # ----------------------------------

    async def update(

        self,

        product: Product,

        data

    ):

        if data.category_id is not None:
            product.category_id = data.category_id

        if data.brand_id is not None:
            product.brand_id = data.brand_id

        if data.product_name is not None:
            product.product_name = data.product_name

        if data.purchase_price is not None:
            product.purchase_price = data.purchase_price

        if data.selling_price is not None:
            product.selling_price = data.selling_price

        if data.tax is not None:
            product.tax = data.tax

        if data.stock is not None:
            product.stock = data.stock

        if data.minimum_stock is not None:
            product.minimum_stock = data.minimum_stock

        if data.unit is not None:
            product.unit = data.unit

        if data.description is not None:
            product.description = data.description

        if data.image_url is not None:
            product.image_url = data.image_url

        if data.status is not None:
            product.status = data.status

        await self.db.commit()

        await self.db.refresh(product)

        return product

    # ----------------------------------
    # Delete Product
    # ----------------------------------

    async def delete(

        self,

        product: Product

    ):

        await self.db.delete(product)

        await self.db.commit()

        return {

            "message": "Product Deleted Successfully"

        }