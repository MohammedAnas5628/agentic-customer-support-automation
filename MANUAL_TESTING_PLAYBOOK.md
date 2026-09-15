# 🧪 ElectroMart: Complete Manual Testing Playbook

This playbook provides exact click-by-click instructions, pre-seeded test accounts, and copy-paste messages to test all features of the live platform in your browser at **`http://localhost:3000`**.

---

## 🔑 Pre-Seeded Accounts for Testing

| Role | Email | Password | What to Test With This Account |
|---|---|---|---|
| **Registered Customer (Has Orders)** | `anas@example.com` | `Password123!` | Has order **`ORD-1001`** (Galaxy S26, ₹89,999) and tickets. |
| **Second Customer (Isolation Test)** | `rahul@example.com` | `Password123!` | Has order **`ORD-1002`**. Cannot see Anas's orders! |
| **New Customer Registration** | Any new email | Your choice | Test the live `/register` form. |

---

## 💬 Chat Window Test Script (Copy & Paste These!)

Go to **`http://localhost:3000/support`** (or open the Support widget) and send these messages one by one in the same conversation to test the dynamic LangGraph multi-agent routing and memory persistence:

### 1. Test Greeting & Capabilities
* **Drop this message:**
  ```text
  Hello! What can you help me with?
  ```
* **Expected Response:** Friendly welcome outlining customer support capabilities (products, orders, tracking, returns, warranties, tickets).

---

### 2. Test Catalog Agent (Product Recommendations & Price Search)
* **Drop this message:**
  ```text
  Can you recommend a good laptop for coding and video editing?
  ```
* **Expected Response:** The **Catalog Agent** queries PostgreSQL and recommends actual products from your database:
  - *Dell Inspiron 15 (₹64,999)*
  - *Apple MacBook Air M4 (₹1,14,900)*
  - *Lenovo ThinkPad X1 (₹1,45,000)*

---

### 3. Test Order Agent (Real-Time Order Tracking & Cancellation)
> *Make sure you are logged in as `anas@example.com` to see order `#ORD-1001`!*

* **Drop this message:**
  ```text
  Where is my order ORD-1001 and when will it arrive?
  ```
* **Expected Response:** The **Order Agent** looks up `ORD-1001` in PostgreSQL, displays status (`processing`/`shipped`), total price, and tracking number.

---

### 4. Test Customer Data Isolation (Security Guardrail)
> *Log in as `rahul@example.com` and ask about Anas's order:*

* **Drop this message:**
  ```text
  Can you show me the details of order ORD-1001?
  ```
* **Expected Response:** The agent will politely refuse or state that the order could not be found, enforcing strict customer-to-customer privacy.

---

### 5. Test Knowledge Base RAG Agent (15 Policy Documents)
* **Drop this message:**
  ```text
  What is your return policy if my electronics item arrives damaged or defective?
  ```
* **Expected Response:** The **Knowledge Agent** runs hybrid search across the 145 vector chunks in PostgreSQL and provides the exact policy from `returns_and_refunds.md` with source citations.

* **Another RAG Test (GST & Invoices):**
  ```text
  Do you provide GST tax invoices for business purchases?
  ```
* **Expected Response:** Retrieves details from `invoices_and_tax.md` explaining how business customers can download GST invoices.

---

### 6. Test Escalation Agent (Automated Ticket Generation)
* **Drop this message:**
  ```text
  I am very frustrated. My package arrived completely crushed and I want to speak to a human manager immediately!
  ```
* **Expected Response:** The **Escalation Agent** automatically flags the complaint, generates a formal support ticket (e.g. `TKT...`), logs it into PostgreSQL, and presents the ticket number for human handover.

---

### 7. Test Anti-Hallucination Guardrail (Refusal Behavior)
* **Drop this message:**
  ```text
  What is the price of an airplane ticket to Mars on ElectroMart?
  ```
* **Expected Response:** Refusal behavior: *"I don't have enough ElectroMart information to answer that. I can only assist with ElectroMart electronics, orders, returns, and support."* (Does NOT hallucinate or make up a fake flight price).

---

## 🖥️ UI Pages to Click and Verify

1. **Storefront (`/` or `/products`)**:
   - Verify that 20 seeded products are displayed with images, ratings, and prices.
   - Test the search bar: Type *"Galaxy"* or *"Sony"* to see instant filtering.
2. **Account Login (`/login`)**:
   - Log in with `anas@example.com` / `Password123!`.
   - Verify your name displays in the top navigation bar.
3. **Customer Account (`/account` & `/orders`)**:
   - Click on your account profile to view your saved addresses and order history (`ORD-1001`).
   - Click into Order `ORD-1001` to view items, subtotal, shipping fee, and tracking number.
4. **Tickets Dashboard (`/tickets`)**:
   - View your open support tickets and check the status of escalated tickets.

---

## 📊 Database Memory Persistence Verification

Every message you send in the chat is permanently saved in your local PostgreSQL database. You can inspect your real conversation history anytime by running:

```powershell
python scripts/live_e2e_test.py
```
