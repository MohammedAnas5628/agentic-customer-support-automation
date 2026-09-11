from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.database import get_db
from backend.app.schemas.product import ProductResponse
from backend.app.services.product_service import (
    get_product,
    get_products,
    search_products,
)


router = APIRouter(prefix="/api/products", tags=["products"])


@router.get("", response_model=list[ProductResponse])
async def read_products(
    session: AsyncSession = Depends(get_db),
) -> list[ProductResponse]:
    return await get_products(session)


@router.get("/search", response_model=list[ProductResponse])
async def read_product_search(
    name: str | None = Query(default=None),
    brand: str | None = Query(default=None),
    category: str | None = Query(default=None),
    session: AsyncSession = Depends(get_db),
) -> list[ProductResponse]:
    return await search_products(session, name=name, brand=brand, category=category)


@router.get("/{product_id}", response_model=ProductResponse)
async def read_product(
    product_id: int,
    session: AsyncSession = Depends(get_db),
) -> ProductResponse:
    product = await get_product(session, product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return product