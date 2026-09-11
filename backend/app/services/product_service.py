from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.product import Product


async def get_products(session: AsyncSession) -> list[Product]:
    statement = select(Product).order_by(Product.id)
    result = await session.execute(statement)
    return list(result.scalars().all())


async def get_product(
    session: AsyncSession,
    product_id: int,
) -> Product | None:
    statement = select(Product).where(Product.id == product_id)
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def search_products(
    session: AsyncSession,
    name: str | None = None,
    brand: str | None = None,
    category: str | None = None,
) -> list[Product]:
    statement = select(Product)

    if name is not None:
        statement = statement.where(Product.name.ilike(f"%{name}%"))
    if brand is not None:
        statement = statement.where(Product.brand.ilike(f"%{brand}%"))
    if category is not None:
        statement = statement.where(Product.category.ilike(f"%{category}%"))

    statement = statement.order_by(Product.id)
    result = await session.execute(statement)
    return list(result.scalars().all())