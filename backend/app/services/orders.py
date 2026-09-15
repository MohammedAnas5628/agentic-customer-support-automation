from datetime import datetime, timezone
from decimal import Decimal
import re
import uuid
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.app.models.customer import Customer
from backend.app.models.order import Order
from backend.app.models.order_item import OrderItem
from backend.app.models.payment import Payment
from backend.app.models.product import Product
from backend.app.schemas.order import OrderCreate


async def get_order_by_number(
    session: AsyncSession,
    order_number: str,
) -> Order | None:
    clean = re.sub(r"[-_\s]", "", order_number).upper()
    digits = re.sub(r"\D", "", order_number)
    conditions = [
        Order.order_number.ilike(order_number.strip()),
        Order.order_number.ilike(clean),
    ]
    if digits:
        conditions.extend([
            Order.order_number.ilike(f"EM{digits}"),
            Order.order_number.ilike(f"EM-{digits}"),
            Order.order_number.ilike(f"ORD-{digits}"),
        ])

    statement = (
        select(Order)
        .where(or_(*conditions))
        .options(
            selectinload(Order.customer),
            selectinload(Order.items).selectinload(OrderItem.product),
            selectinload(Order.payment).selectinload(Payment.refunds),
        )
    )

    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def create_order(
    session: AsyncSession,
    customer_id: int,
    data: OrderCreate,
) -> Order:
    customer_res = await session.execute(select(Customer).where(Customer.id == customer_id))
    customer = customer_res.scalar_one_or_none()
    if customer is None:
        raise ValueError("Customer not found")

    product_ids = [item.product_id for item in data.items]
    prod_stmt = select(Product).where(Product.id.in_(product_ids))
    prod_res = await session.execute(prod_stmt)
    products_by_id = {p.id: p for p in prod_res.scalars().all()}

    for item in data.items:
        if item.product_id not in products_by_id:
            raise ValueError(f"Product ID {item.product_id} not found")

    max_id_res = await session.execute(select(func.max(Order.id)))
    max_id = max_id_res.scalar() or 20
    next_num = max_id + 1
    order_number = f"EM{10000 + next_num}"

    while (await get_order_by_number(session, order_number)) is not None:
        next_num += 1
        order_number = f"EM{10000 + next_num}"

    subtotal = Decimal("0.00")
    for item in data.items:
        prod = products_by_id[item.product_id]
        subtotal += prod.price * item.quantity

    shipping_fee = Decimal("0.00")
    discount = Decimal("0.00")
    total_amount = subtotal + shipping_fee - discount

    shipping_address = (
        data.shipping_address.strip()
        if data.shipping_address and data.shipping_address.strip()
        else "Plot 42, Hitech City, Hyderabad, Telangana 500081"
    )

    order = Order(
        order_number=order_number,
        customer_id=customer_id,
        status="processing",
        subtotal=subtotal,
        shipping_fee=shipping_fee,
        discount=discount,
        total_amount=total_amount,
        shipping_address=shipping_address,
    )
    session.add(order)
    await session.flush()

    for item in data.items:
        prod = products_by_id[item.product_id]
        order_item = OrderItem(
            order_id=order.id,
            product_id=prod.id,
            quantity=item.quantity,
            unit_price=prod.price,
            total_price=prod.price * item.quantity,
        )
        session.add(order_item)

    payment = Payment(
        order_id=order.id,
        payment_method=data.payment_method or "UPI",
        payment_status="completed",
        transaction_id=f"TXN-{uuid.uuid4().hex[:10].upper()}",
        amount=total_amount,
        paid_at=datetime.now(timezone.utc),
    )
    session.add(payment)

    await session.commit()

    created_order = await get_order_by_number(session, order_number)
    return created_order