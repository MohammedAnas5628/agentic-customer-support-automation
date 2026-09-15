from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from backend.app.core.config import settings


# Configure engine kwargs with connection pool tuning for production PostgreSQL
engine_kwargs: dict = {
    "echo": settings.debug,
    "pool_pre_ping": True,
}

if not settings.database_url.startswith("sqlite"):
    engine_kwargs.update({
        "pool_size": settings.db_pool_size,
        "max_overflow": settings.db_max_overflow,
        "pool_timeout": settings.db_pool_timeout,
        "pool_recycle": settings.db_pool_recycle,
    })

# Create the database engine
engine = create_async_engine(
    settings.database_url,
    **engine_kwargs,
)


# Create database sessions
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# Dependency used by FastAPI endpoints
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session