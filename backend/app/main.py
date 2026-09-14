from fastapi import FastAPI, Request
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
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
from backend.app.core.limiter import limiter


app = FastAPI(
    title=settings.app_name,
    description="AI-powered customer support automation platform for ElectroMart.",
    version="1.0.0",
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none'"
    if settings.app_env.lower() not in {"development", "test"}:
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

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
