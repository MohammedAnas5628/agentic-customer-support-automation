import asyncio
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from backend.app.core.config import settings
from backend.app.models import (
    Conversation,
    Customer,
    Message,
    Order,
    OrderItem,
    Payment,
    Product,
    Refund,
    Ticket,
)


engine = create_async_engine(
    settings.database_url,
    echo=False,
    pool_pre_ping=True,
)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def clear_seed_data(session: AsyncSession) -> None:
    """Clear existing development data in dependency-safe order."""

    await session.execute(delete(Message))
    await session.execute(delete(Conversation))
    await session.execute(delete(Ticket))
    await session.execute(delete(Refund))
    await session.execute(delete(Payment))
    await session.execute(delete(OrderItem))
    await session.execute(delete(Order))
    await session.execute(delete(Product))
    await session.execute(delete(Customer))

    await session.commit()


async def seed_database() -> None:
    """Populate the ElectroMart development database with sample data."""

    async with SessionLocal() as session:
        print("Clearing existing development data...")
        await clear_seed_data(session)

        # ---------------------------------------------------------
        # Customers
        # ---------------------------------------------------------

        customers = [
            Customer(
                name="Anas Khan",
                email="anas@example.com",
                phone="9876500001",
                password_hash="DEMO_HASH_001",
            ),
            Customer(
                name="Rahul Sharma",
                email="rahul@example.com",
                phone="9876500002",
                password_hash="DEMO_HASH_002",
            ),
            Customer(
                name="Aisha Patel",
                email="aisha@example.com",
                phone="9876500003",
                password_hash="DEMO_HASH_003",
            ),
            Customer(
                name="Arjun Reddy",
                email="arjun@example.com",
                phone="9876500004",
                password_hash="DEMO_HASH_004",
            ),
            Customer(
                name="Sara Ahmed",
                email="sara@example.com",
                phone="9876500005",
                password_hash="DEMO_HASH_005",
            ),
        ]

        session.add_all(customers)
        await session.flush()

        # ---------------------------------------------------------
        # Products
        # ---------------------------------------------------------

        products = [
            Product(
                sku="EM-PH-001",
                name="Galaxy S26",
                brand="Samsung",
                category="Smartphones",
                description="Flagship Android smartphone with advanced camera and performance.",
                price=Decimal("74999.00"),
                stock_quantity=25,
            ),
            Product(
                sku="EM-PH-002",
                name="iPhone 17",
                brand="Apple",
                category="Smartphones",
                description="Premium smartphone with powerful performance and advanced camera system.",
                price=Decimal("79999.00"),
                stock_quantity=18,
            ),
            Product(
                sku="EM-PH-003",
                name="Pixel 10",
                brand="Google",
                category="Smartphones",
                description="Google smartphone with AI-powered features and clean Android experience.",
                price=Decimal("69999.00"),
                stock_quantity=20,
            ),
            Product(
                sku="EM-LT-001",
                name="Inspiron 15",
                brand="Dell",
                category="Laptops",
                description="15-inch everyday laptop suitable for work, study, and productivity.",
                price=Decimal("64999.00"),
                stock_quantity=15,
            ),
            Product(
                sku="EM-LT-002",
                name="MacBook Air M4",
                brand="Apple",
                category="Laptops",
                description="Lightweight laptop powered by Apple's M4 chip.",
                price=Decimal("99999.00"),
                stock_quantity=12,
            ),
            Product(
                sku="EM-LT-003",
                name="IdeaPad Slim 5",
                brand="Lenovo",
                category="Laptops",
                description="Slim productivity laptop designed for everyday computing.",
                price=Decimal("58999.00"),
                stock_quantity=22,
            ),
            Product(
                sku="EM-TB-001",
                name="iPad Air",
                brand="Apple",
                category="Tablets",
                description="Versatile tablet for productivity, entertainment, and creative work.",
                price=Decimal("59999.00"),
                stock_quantity=14,
            ),
            Product(
                sku="EM-TB-002",
                name="Galaxy Tab S11",
                brand="Samsung",
                category="Tablets",
                description="Premium Android tablet with a high-resolution display.",
                price=Decimal("54999.00"),
                stock_quantity=17,
            ),
            Product(
                sku="EM-AU-001",
                name="AirPods Pro",
                brand="Apple",
                category="Headphones",
                description="Wireless earbuds with active noise cancellation.",
                price=Decimal("24999.00"),
                stock_quantity=30,
            ),
            Product(
                sku="EM-AU-002",
                name="WH-1000XM6",
                brand="Sony",
                category="Headphones",
                description="Premium wireless over-ear headphones with active noise cancellation.",
                price=Decimal("34999.00"),
                stock_quantity=16,
            ),
            Product(
                sku="EM-SW-001",
                name="Apple Watch Series 11",
                brand="Apple",
                category="Smartwatches",
                description="Smartwatch with fitness, health, and notification features.",
                price=Decimal("44999.00"),
                stock_quantity=11,
            ),
            Product(
                sku="EM-SW-002",
                name="Galaxy Watch 8",
                brand="Samsung",
                category="Smartwatches",
                description="Android-compatible smartwatch with fitness and smart features.",
                price=Decimal("32999.00"),
                stock_quantity=19,
            ),
            Product(
                sku="EM-GM-001",
                name="PlayStation 5",
                brand="Sony",
                category="Gaming",
                description="Current-generation gaming console with high-performance graphics.",
                price=Decimal("54999.00"),
                stock_quantity=8,
            ),
            Product(
                sku="EM-GM-002",
                name="Xbox Series X",
                brand="Microsoft",
                category="Gaming",
                description="High-performance gaming console for demanding games.",
                price=Decimal("52999.00"),
                stock_quantity=9,
            ),
            Product(
                sku="EM-AC-001",
                name="65W USB-C Charger",
                brand="Anker",
                category="Accessories",
                description="Compact USB-C charger suitable for phones, tablets, and compatible laptops.",
                price=Decimal("3499.00"),
                stock_quantity=45,
            ),
            Product(
                sku="EM-AC-002",
                name="100W USB-C Cable",
                brand="Belkin",
                category="Accessories",
                description="High-power USB-C charging and data cable.",
                price=Decimal("1999.00"),
                stock_quantity=50,
            ),
            Product(
                sku="EM-AC-003",
                name="Wireless Keyboard",
                brand="Logitech",
                category="Accessories",
                description="Wireless keyboard designed for everyday desktop productivity.",
                price=Decimal("2999.00"),
                stock_quantity=35,
            ),
            Product(
                sku="EM-AC-004",
                name="Wireless Mouse",
                brand="Logitech",
                category="Accessories",
                description="Comfortable wireless mouse for work and everyday computing.",
                price=Decimal("1799.00"),
                stock_quantity=40,
            ),
            Product(
                sku="EM-TV-001",
                name="55-inch 4K Smart TV",
                brand="Sony",
                category="Electronics",
                description="4K smart television with streaming and smart-home features.",
                price=Decimal("69999.00"),
                stock_quantity=10,
            ),
            Product(
                sku="EM-TV-002",
                name="50-inch 4K Smart TV",
                brand="Samsung",
                category="Electronics",
                description="4K smart television with HDR and popular streaming apps.",
                price=Decimal("57999.00"),
                stock_quantity=13,
            ),
        ]

        session.add_all(products)
        await session.flush()

        # ---------------------------------------------------------
        # Orders
        # ---------------------------------------------------------

        orders = [
            Order(
                order_number="EM10001",
                customer_id=customers[0].id,
                status="processing",
                subtotal=Decimal("74999.00"),
                shipping_fee=Decimal("0.00"),
                discount=Decimal("1000.00"),
                total_amount=Decimal("73999.00"),
                shipping_address="Hyderabad, Telangana",
            ),
            Order(
                order_number="EM10002",
                customer_id=customers[0].id,
                status="shipped",
                subtotal=Decimal("24999.00"),
                shipping_fee=Decimal("0.00"),
                discount=Decimal("500.00"),
                total_amount=Decimal("24499.00"),
                shipping_address="Hyderabad, Telangana",
                tracking_number="EMTRK10002",
            ),
            Order(
                order_number="EM10003",
                customer_id=customers[1].id,
                status="delivered",
                subtotal=Decimal("64999.00"),
                shipping_fee=Decimal("0.00"),
                discount=Decimal("2000.00"),
                total_amount=Decimal("62999.00"),
                shipping_address="Bengaluru, Karnataka",
                tracking_number="EMTRK10003",
            ),
            Order(
                order_number="EM10004",
                customer_id=customers[1].id,
                status="cancelled",
                subtotal=Decimal("54999.00"),
                shipping_fee=Decimal("0.00"),
                discount=Decimal("0.00"),
                total_amount=Decimal("54999.00"),
                shipping_address="Bengaluru, Karnataka",
            ),
            Order(
                order_number="EM10005",
                customer_id=customers[2].id,
                status="packed",
                subtotal=Decimal("99999.00"),
                shipping_fee=Decimal("0.00"),
                discount=Decimal("5000.00"),
                total_amount=Decimal("94999.00"),
                shipping_address="Mumbai, Maharashtra",
            ),
            Order(
                order_number="EM10006",
                customer_id=customers[2].id,
                status="shipped",
                subtotal=Decimal("34999.00"),
                shipping_fee=Decimal("99.00"),
                discount=Decimal("0.00"),
                total_amount=Decimal("35098.00"),
                shipping_address="Mumbai, Maharashtra",
                tracking_number="EMTRK10006",
            ),
            Order(
                order_number="EM10007",
                customer_id=customers[3].id,
                status="processing",
                subtotal=Decimal("59999.00"),
                shipping_fee=Decimal("0.00"),
                discount=Decimal("1500.00"),
                total_amount=Decimal("58499.00"),
                shipping_address="Chennai, Tamil Nadu",
            ),
            Order(
                order_number="EM10008",
                customer_id=customers[3].id,
                status="delivered",
                subtotal=Decimal("24999.00"),
                shipping_fee=Decimal("0.00"),
                discount=Decimal("0.00"),
                total_amount=Decimal("24999.00"),
                shipping_address="Chennai, Tamil Nadu",
                tracking_number="EMTRK10008",
            ),
            Order(
                order_number="EM10009",
                customer_id=customers[4].id,
                status="shipped",
                subtotal=Decimal("54999.00"),
                shipping_fee=Decimal("0.00"),
                discount=Decimal("1000.00"),
                total_amount=Decimal("53999.00"),
                shipping_address="Delhi, India",
                tracking_number="EMTRK10009",
            ),
            Order(
                order_number="EM10010",
                customer_id=customers[4].id,
                status="processing",
                subtotal=Decimal("3499.00"),
                shipping_fee=Decimal("49.00"),
                discount=Decimal("0.00"),
                total_amount=Decimal("3548.00"),
                shipping_address="Delhi, India",
            ),
        ]

        session.add_all(orders)
        await session.flush()

        # ---------------------------------------------------------
        # Order Items
        # ---------------------------------------------------------

        order_items = [
            OrderItem(
                order_id=orders[0].id,
                product_id=products[0].id,
                quantity=1,
                unit_price=Decimal("74999.00"),
                total_price=Decimal("74999.00"),
            ),
            OrderItem(
                order_id=orders[1].id,
                product_id=products[8].id,
                quantity=1,
                unit_price=Decimal("24999.00"),
                total_price=Decimal("24999.00"),
            ),
            OrderItem(
                order_id=orders[2].id,
                product_id=products[3].id,
                quantity=1,
                unit_price=Decimal("64999.00"),
                total_price=Decimal("64999.00"),
            ),
            OrderItem(
                order_id=orders[3].id,
                product_id=products[12].id,
                quantity=1,
                unit_price=Decimal("54999.00"),
                total_price=Decimal("54999.00"),
            ),
            OrderItem(
                order_id=orders[4].id,
                product_id=products[4].id,
                quantity=1,
                unit_price=Decimal("99999.00"),
                total_price=Decimal("99999.00"),
            ),
            OrderItem(
                order_id=orders[5].id,
                product_id=products[9].id,
                quantity=1,
                unit_price=Decimal("34999.00"),
                total_price=Decimal("34999.00"),
            ),
            OrderItem(
                order_id=orders[6].id,
                product_id=products[6].id,
                quantity=1,
                unit_price=Decimal("59999.00"),
                total_price=Decimal("59999.00"),
            ),
            OrderItem(
                order_id=orders[7].id,
                product_id=products[8].id,
                quantity=1,
                unit_price=Decimal("24999.00"),
                total_price=Decimal("24999.00"),
            ),
            OrderItem(
                order_id=orders[8].id,
                product_id=products[12].id,
                quantity=1,
                unit_price=Decimal("54999.00"),
                total_price=Decimal("54999.00"),
            ),
            OrderItem(
                order_id=orders[9].id,
                product_id=products[14].id,
                quantity=1,
                unit_price=Decimal("3499.00"),
                total_price=Decimal("3499.00"),
            ),
        ]

        session.add_all(order_items)

        # ---------------------------------------------------------
        # Payments
        # ---------------------------------------------------------

        payments = [
            Payment(
                order_id=orders[0].id,
                payment_method="upi",
                payment_status="completed",
                transaction_id="TXN10001",
                amount=Decimal("73999.00"),
                paid_at=datetime.now(timezone.utc),
            ),
            Payment(
                order_id=orders[1].id,
                payment_method="card",
                payment_status="completed",
                transaction_id="TXN10002",
                amount=Decimal("24499.00"),
                paid_at=datetime.now(timezone.utc),
            ),
            Payment(
                order_id=orders[2].id,
                payment_method="card",
                payment_status="completed",
                transaction_id="TXN10003",
                amount=Decimal("62999.00"),
                paid_at=datetime.now(timezone.utc),
            ),
            Payment(
                order_id=orders[3].id,
                payment_method="upi",
                payment_status="refunded",
                transaction_id="TXN10004",
                amount=Decimal("54999.00"),
                paid_at=datetime.now(timezone.utc),
            ),
            Payment(
                order_id=orders[4].id,
                payment_method="card",
                payment_status="completed",
                transaction_id="TXN10005",
                amount=Decimal("94999.00"),
                paid_at=datetime.now(timezone.utc),
            ),
            Payment(
                order_id=orders[5].id,
                payment_method="cod",
                payment_status="completed",
                transaction_id=None,
                amount=Decimal("35098.00"),
                paid_at=datetime.now(timezone.utc),
            ),
            Payment(
                order_id=orders[6].id,
                payment_method="upi",
                payment_status="pending",
                transaction_id="TXN10007",
                amount=Decimal("58499.00"),
            ),
            Payment(
                order_id=orders[7].id,
                payment_method="card",
                payment_status="completed",
                transaction_id="TXN10008",
                amount=Decimal("24999.00"),
                paid_at=datetime.now(timezone.utc),
            ),
            Payment(
                order_id=orders[8].id,
                payment_method="upi",
                payment_status="completed",
                transaction_id="TXN10009",
                amount=Decimal("53999.00"),
                paid_at=datetime.now(timezone.utc),
            ),
            Payment(
                order_id=orders[9].id,
                payment_method="card",
                payment_status="failed",
                transaction_id="TXN10010",
                amount=Decimal("3548.00"),
            ),
        ]

        session.add_all(payments)
        await session.flush()

        # ---------------------------------------------------------
        # Refunds
        # ---------------------------------------------------------

        refunds = [
            Refund(
                payment_id=payments[3].id,
                refund_status="completed",
                amount=Decimal("54999.00"),
                refund_transaction_id="REF10004",
                reason="Customer cancelled order",
                processed_at=datetime.now(timezone.utc),
            ),
            Refund(
                payment_id=payments[1].id,
                refund_status="pending",
                amount=Decimal("500.00"),
                refund_transaction_id="REF10002",
                reason="Partial refund for promotional adjustment",
            ),
        ]

        session.add_all(refunds)

        # ---------------------------------------------------------
        # Tickets
        # ---------------------------------------------------------

        tickets = [
            Ticket(
                ticket_number="TKT10001",
                customer_id=customers[0].id,
                order_id=orders[1].id,
                subject="Order delivery delayed",
                description="My shipped order has not arrived yet and the tracking has not changed.",
                status="open",
                priority="high",
                assigned_to="support_agent_01",
            ),
            Ticket(
                ticket_number="TKT10002",
                customer_id=customers[1].id,
                order_id=orders[2].id,
                subject="Product arrived damaged",
                description="The laptop arrived with visible physical damage.",
                status="open",
                priority="high",
                assigned_to="support_agent_02",
            ),
            Ticket(
                ticket_number="TKT10003",
                customer_id=customers[2].id,
                order_id=orders[5].id,
                subject="Refund status request",
                description="Customer wants an update on a refund.",
                status="pending",
                priority="normal",
                assigned_to="support_agent_01",
            ),
            Ticket(
                ticket_number="TKT10004",
                customer_id=customers[3].id,
                order_id=None,
                subject="General product question",
                description="Customer needs help choosing a tablet.",
                status="open",
                priority="normal",
            ),
            Ticket(
                ticket_number="TKT10005",
                customer_id=customers[4].id,
                order_id=orders[8].id,
                subject="Request for human support",
                description="Customer requested to speak with a human support representative.",
                status="open",
                priority="high",
                assigned_to="human_support",
            ),
        ]

        session.add_all(tickets)

        # ---------------------------------------------------------
        # Conversations
        # ---------------------------------------------------------

        conversations = [
            Conversation(
                customer_id=customers[0].id,
                status="active",
                channel="web",
            ),
            Conversation(
                customer_id=customers[1].id,
                status="closed",
                channel="web",
            ),
            Conversation(
                customer_id=customers[2].id,
                status="active",
                channel="web",
            ),
        ]

        session.add_all(conversations)
        await session.flush()

        # ---------------------------------------------------------
        # Messages
        # ---------------------------------------------------------

        messages = [
            Message(
                conversation_id=conversations[0].id,
                sender_type="customer",
                content="Where is my order EM10002?",
            ),
            Message(
                conversation_id=conversations[0].id,
                sender_type="assistant",
                content="Your order EM10002 is currently shipped. The tracking number is EMTRK10002.",
            ),
            Message(
                conversation_id=conversations[1].id,
                sender_type="customer",
                content="My laptop arrived damaged.",
            ),
            Message(
                conversation_id=conversations[1].id,
                sender_type="assistant",
                content="I'm sorry about that. I've created a support ticket so our team can help with the replacement process.",
            ),
            Message(
                conversation_id=conversations[2].id,
                sender_type="customer",
                content="What is the status of my refund?",
            ),
            Message(
                conversation_id=conversations[2].id,
                sender_type="assistant",
                content="Your refund request is currently being processed.",
            ),
        ]

        session.add_all(messages)

        await session.commit()

        print("ElectroMart database seeded successfully.")
        print("Created:")
        print("- 5 customers")
        print("- 20 products")
        print("- 10 orders")
        print("- 10 order items")
        print("- 10 payments")
        print("- 2 refunds")
        print("- 5 tickets")
        print("- 3 conversations")
        print("- 6 messages")


async def main() -> None:
    try:
        await seed_database()
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())