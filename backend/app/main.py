from fastapi import FastAPI
from sqlalchemy import text

from backend.app.api.customers import router as customers_router
from backend.app.api.cancellation import router as cancellation_router
from backend.app.api.orders import router as orders_router
from backend.app.api.products import router as products_router
from backend.app.api.refunds import router as refunds_router
from backend.app.api.tickets import router as tickets_router
from backend.app.api.rag import router as rag_router
from backend.app.api.auth import router as auth_router
from backend.app.api.support import router as support_router
from backend.app.core.config import settings
from backend.app.db.database import AsyncSessionLocal


app = FastAPI(
    title=settings.app_name,
    description="AI-powered customer support automation platform for ElectroMart.",
    version="1.0.0",
)

app.include_router(orders_router)
app.include_router(cancellation_router)
app.include_router(customers_router)
app.include_router(products_router)
app.include_router(refunds_router)
app.include_router(tickets_router)
app.include_router(rag_router)
app.include_router(auth_router)
app.include_router(support_router)


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "environment": settings.app_env,
    }


@app.get("/health/db")
async def database_health_check():
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT 1"))
        value = result.scalar()

    return {
        "database": "connected",
        "test_result": value,
    }
