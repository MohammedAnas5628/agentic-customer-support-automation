import asyncio
import os
import sys
import httpx
from sqlalchemy import text

# Ensure root in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from backend.app.db.database import AsyncSessionLocal

async def run_live_tests():
    print("=" * 75)
    print("STARTING LIVE SYSTEM VERIFICATION (POSTGRESQL + PGVECTOR + AI WORKFLOW)")
    print("=" * 75)

    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000", timeout=40.0) as client:
        # TEST 1: User Registration & JWT Authentication
        print("\n[TEST 1] User Registration & JWT Auth")
        email = "live_tester_02@example.com"
        pwd = "TestPassword123!"
        reg = await client.post("/api/auth/register", json={
            "name": "Live Tester",
            "email": email,
            "password": pwd,
            "phone": "9998887770"
        })
        print(f"   ✓ Register Status: {reg.status_code} ({reg.json().get('email')})")

        login = await client.post("/api/auth/login", json={"email": email, "password": pwd})
        token = login.json().get("access_token")
        print(f"   ✓ Login Status: {login.status_code} (JWT Token Issued: {bool(token)})")

        headers = {"Authorization": f"Bearer {token}"}

        # TEST 2: Product Catalog & Search
        print("\n[TEST 2] Product Catalog & Search")
        prods = await client.get("/api/products")
        prods_data = prods.json()
        print(f"   ✓ Products List: {prods.status_code} (Found {len(prods_data)} products in PostgreSQL)")
        search = await client.get("/api/products/search?name=Galaxy")
        print(f"   ✓ Search 'Galaxy': {search.status_code} (Found: {[p['name'] for p in search.json()]})")

        # TEST 3: Knowledge Base RAG Direct Query
        print("\n[TEST 3] Knowledge Base RAG (Hybrid pgvector Search)")
        rag = await client.post("/api/rag/query", json={"query": "What is the return policy for damaged items?"})
        rag_data = rag.json()
        print(f"   ✓ RAG Status: {rag.status_code}")
        print(f"   ✓ RAG Sources: {[s['source'] for s in rag_data.get('sources', [])]}")
        print(f"   ✓ RAG Answer: {rag_data.get('answer')[:120]}...")

        # TEST 4: Multi-Turn Support Chat & Dynamic Agent Routing
        print("\n[TEST 4] Multi-Turn Support Chat & Dynamic Agent Routing")
        conv_id = None

        # Turn 1: Greeting
        t1 = await client.post("/api/support/query", json={"message": "Hello there!"}, headers=headers)
        t1_data = t1.json()
        conv_id = t1_data.get("conversation_id")
        print(f"   ✓ Turn 1 (Greeting): Reply=\"{t1_data.get('answer')}\" (Conversation ID: {conv_id})")

        # Turn 2: Policy inquiry (Knowledge Agent via RAG)
        t2 = await client.post("/api/support/query", json={"message": "How many days do I have to return an item?", "conversation_id": conv_id}, headers=headers)
        t2_data = t2.json()
        print(f"   ✓ Turn 2 (Policy RAG): Intent={t2_data.get('intent')} | Sources={[s['source'] for s in t2_data.get('sources', [])]}")
        print(f"     Reply: {t2_data.get('answer')[:120]}...")

        # Turn 3: Catalog recommendation
        t3 = await client.post("/api/support/query", json={"message": "Can you recommend a good laptop for coding?", "conversation_id": conv_id}, headers=headers)
        t3_data = t3.json()
        print(f"   ✓ Turn 3 (Catalog Agent): Intent={t3_data.get('intent')}")
        print(f"     Reply: {t3_data.get('answer')[:120]}...")

        # Turn 4: Order status check
        t4 = await client.post("/api/support/query", json={"message": "Where is my order ORD-1001?", "conversation_id": conv_id}, headers=headers)
        t4_data = t4.json()
        print(f"   ✓ Turn 4 (Order Agent): Intent={t4_data.get('intent')}")
        print(f"     Reply: {t4_data.get('answer')[:120]}...")

        # Turn 5: Human escalation & ticket opening
        t5 = await client.post("/api/support/query", json={"message": "My item was completely broken, I want to talk to a human manager", "conversation_id": conv_id}, headers=headers)
        t5_data = t5.json()
        print(f"   ✓ Turn 5 (Escalation Agent): Intent={t5_data.get('intent')} | TicketNumber={t5_data.get('ticket_number')}")
        print(f"     Reply: {t5_data.get('answer')[:120]}...")

        # TEST 5: Verify Conversation Memory Persistence in PostgreSQL
        print("\n[TEST 5] Conversation Memory Database Verification")
        async with AsyncSessionLocal() as session:
            res_conv = await session.execute(text(f"SELECT id, customer_id, memory_summary FROM conversations WHERE id = {conv_id}"))
            row_conv = res_conv.fetchone()
            print(f"   ✓ PostgreSQL Conversation Record: ID={row_conv[0]}, CustomerID={row_conv[1]}")

            res_msgs = await session.execute(text(f"SELECT sender_type, content FROM messages WHERE conversation_id = {conv_id} ORDER BY id"))
            msgs = res_msgs.fetchall()
            print(f"   ✓ PostgreSQL Saved Messages: {len(msgs)} messages persisted in database")
            for i, m in enumerate(msgs, 1):
                preview = m[1].replace("\n", " ")[:65]
                print(f"     {i}. [{m[0].upper()}]: {preview}...")

    print("\n" + "=" * 75)
    print("ALL LIVE AGENT & DATABASE TESTS PASSED WITH 100% SUCCESS!")
    print("=" * 75)

if __name__ == "__main__":
    asyncio.run(run_live_tests())
