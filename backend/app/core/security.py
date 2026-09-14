from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.config import settings
from backend.app.db.database import AsyncSessionLocal, get_db
from backend.app.models.customer import Customer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
optional_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)
password_hash = PasswordHash.recommended()


def _jwt_secret() -> str:
    value = settings.jwt_secret
    return value.get_secret_value() if hasattr(value, "get_secret_value") else str(value)


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    try:
        return password_hash.verify(password, hashed_password)
    except Exception:
        return False


def create_access_token(customer: Customer) -> str:
    secret = _jwt_secret()
    if not secret:
        raise RuntimeError("JWT_SECRET is not configured.")
    expires = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    payload = {"sub": str(customer.id), "role": customer.role, "exp": expires}
    return jwt.encode(payload, secret, algorithm=settings.jwt_algorithm)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db),
) -> Customer:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    secret = _jwt_secret()
    if not secret:
        raise credentials_error
    try:
        payload = jwt.decode(token, secret, algorithms=[settings.jwt_algorithm])
        customer_id = int(payload["sub"])
    except (jwt.PyJWTError, KeyError, TypeError, ValueError):
        raise credentials_error

    customer = await session.get(Customer, customer_id)
    if customer is None or not customer.is_active:
        raise credentials_error
    return customer


def require_roles(*roles: str):
    async def dependency(customer: Customer = Depends(get_current_user)) -> Customer:
        if customer.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return customer

    return dependency


async def authenticate_customer(session: AsyncSession, email: str, password: str) -> Customer | None:
    result = await session.execute(select(Customer).where(Customer.email == email.lower()))
    customer = result.scalar_one_or_none()
    if customer is None or not customer.is_active or not verify_password(password, customer.password_hash):
        return None
    return customer


async def get_optional_current_user(
    token: str | None = Depends(optional_oauth2_scheme),
    session: AsyncSession = Depends(get_db),
) -> Customer | None:
    """Return the signed-in customer when a valid bearer token is supplied.

    Public support questions remain available without a session; protected actions
    are explicitly rejected by the support endpoint before workflow execution.
    """
    if token is None:
        return None
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    secret = _jwt_secret()
    if not secret:
        raise credentials_error
    try:
        payload = jwt.decode(token, secret, algorithms=[settings.jwt_algorithm])
        customer_id = int(payload["sub"])
    except (jwt.PyJWTError, KeyError, TypeError, ValueError):
        raise credentials_error
    customer = await session.get(Customer, customer_id)
    if customer is None or not customer.is_active:
        raise credentials_error
    return customer
