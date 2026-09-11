from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.security import authenticate_customer, create_access_token, hash_password, get_current_user
from backend.app.db.database import get_db
from backend.app.models.customer import Customer
from backend.app.schemas.auth import CurrentUserResponse, LoginRequest, RegisterRequest, TokenResponse


router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=CurrentUserResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest, session: AsyncSession = Depends(get_db)) -> Customer:
    existing = await session.execute(select(Customer).where(Customer.email == payload.email.lower()))
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is already registered")
    customer = Customer(
        name=payload.name.strip(),
        email=payload.email.lower(),
        phone=payload.phone,
        password_hash=hash_password(payload.password),
        role="customer",
    )
    session.add(customer)
    await session.commit()
    await session.refresh(customer)
    return customer


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, session: AsyncSession = Depends(get_db)) -> TokenResponse:
    customer = await authenticate_customer(session, payload.email, payload.password)
    if customer is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    return TokenResponse(access_token=create_access_token(customer))


@router.get("/me", response_model=CurrentUserResponse)
async def me(customer: Customer = Depends(get_current_user)) -> Customer:
    return customer