import logging
import sys
import time
import uuid

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
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

logger = logging.getLogger("electromart.access")

app = FastAPI(
    title=settings.app_name,
    description="AI-powered customer support automation platform for ElectroMart.",
    version="1.0.0",
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS for allowed origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID"],
)


@app.middleware("http")
async def request_lifecycle_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or uuid.uuid4().hex
    request.state.request_id = request_id
    start_time = time.perf_counter()

    response = await call_next(request)

    duration_ms = (time.perf_counter() - start_time) * 1000.0
    response.headers["X-Request-ID"] = request_id

    # Security Headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none'"
    if settings.app_env.lower() not in {"development", "test"}:
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

    client_ip = request.client.host if request.client else "unknown"
    logger.info(
        f"method={request.method} path={request.url.path} status={response.status_code} "
        f"duration_ms={duration_ms:.2f} ip={client_ip} request_id={request_id}"
    )

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
