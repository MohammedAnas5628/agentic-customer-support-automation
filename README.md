# ElectroMart - Agentic Customer Support Automation Platform

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-15-black?style=flat&logo=next.js&logoColor=white)](https://nextjs.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-Agentic_Workflow-blue)](https://langchain-ai.github.io/langgraph/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-pgvector-336791?style=flat&logo=postgresql&logoColor=white)](https://github.com/pgvector/pgvector)
[![Google Gemini](https://img.shields.io/badge/Google_Gemini-3.6_Flash-4285F4?style=flat&logo=google)](https://ai.google.dev)

ElectroMart is an enterprise-grade AI customer support automation system designed to handle real-world e-commerce support queries autonomously. Using a **LangGraph** multi-agent state machine and **pgvector RAG**, it routes customer inquiries, checks orders, processes cancellations, initiates refunds, creates support tickets, and answers complex policy questions with strict hallucination controls.

---

## 🏛 Architecture Overview

```
                          ┌────────────────────────┐
                          │   Next.js 15 Web App   │
                          │ (Tailwind, Zod, Query) │
                          └───────────┬────────────┘
                                      │ REST API / JWT
                                      ▼
             ┌──────────────────────────────────────────────────┐
             │                 FastAPI Backend                  │
             │  • SlowAPI Rate Limiting   • CORS Security       │
             │  • Request ID Tracing      • Security Headers    │
             └────────────────────────┬─────────────────────────┘
                                      │
                         ┌────────────▼────────────┐
                         │   LangGraph Workflow    │
                         │   StateGraph Router     │
                         └────────────┬────────────┘
                                      │
          ┌──────────────┬────────────┼────────────┬──────────────┐
          │              │            │            │              │
          ▼              ▼            ▼            ▼              ▼
  ┌──────────────┐ ┌───────────┐ ┌──────────┐ ┌───────────┐ ┌─────────────┐
  │  Knowledge   │ │  Catalog  │ │  Order   │ │  Support  │ │ Escalation  │
  │    Agent     │ │   Agent   │ │  Agent   │ │   Agent   │ │    Agent    │
  │ (pgvector    │ │ (Product  │ │ (Status, │ │ (Tickets, │ │ (Human      │
  │  RAG + BGE)  │ │  Search)  │ │  Cancel) │ │  Refunds) │ │  Handoff)  │
  └──────┬───────┘ └─────┬─────┘ └────┬─────┘ └─────┬─────┘ └──────┬──────┘
         │               │            │             │              │
         └───────────────┴────────────┼─────────────┴──────────────┘
                                      ▼
                    ┌───────────────────────────────────┐
                    │       PostgreSQL Database         │
                    │   • pgvector (Document Chunks)    │
                    │   • Orders, Items, Payments       │
                    │   • Tickets & Conversation Memory │
                    └───────────────────────────────────┘
```

---

## 🚀 Key Features

- **Multi-Agent Orchestration**: Specialized LangGraph agents evaluate user intent and take deterministic, audited actions rather than relying on unstructured LLM output.
- **RAG Policy Engine**:
  - Embedding Model: Local `BAAI/bge-small-en-v1.5` (384-dimensional dense vectors).
  - Cosine similarity matching via PostgreSQL `pgvector`.
  - Multi-variant query expansions for high-precision recall.
  - Strict grounding prompt preventing hallucinations, invented prices, or phantom policies.
- **Order & Ticket Operations**:
  - Authenticated customer data isolation.
  - Live order lookup, cancellation eligibility validation, and refund processing.
  - Automated support ticket generation with priority tagging and human escalation.
- **Conversation Memory Compaction**:
  - Dynamically summarizes multi-turn conversations into compact memory summaries when threshold is exceeded.
- **Enterprise Security**:
  - Enforced 32+ character JWT secrets.
  - `slowapi` rate limiting on sensitive and AI endpoints.
  - Security headers (`X-Frame-Options: DENY`, `nosniff`, `Content-Security-Policy`, `HSTS`).
  - Correlation tracking with `X-Request-ID`.
  - Configurable CORS policy.

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| **Backend Framework** | FastAPI (Python 3.11 / 3.12) |
| **Agent Orchestration** | LangGraph & LangChain Core |
| **LLM Provider** | Google Gemini (`gemini-3.6-flash`) |
| **Embeddings & Vector Store** | Hugging Face SentenceTransformers (`BAAI/bge-small-en-v1.5`) + PostgreSQL `pgvector` |
| **Database ORM** | SQLAlchemy 2.0 (Async) with `asyncpg` |
| **Database Migrations** | Alembic |
| **Frontend Framework** | Next.js 15 (App Router), React 19, TypeScript |
| **Styling & Icons** | Tailwind CSS, Lucide React, Framer Motion |
| **State & Forms** | TanStack React Query, React Hook Form, Zod |

---

## ⚙️ Environment Configuration

Copy `.env.example` to `.env` in the repository root or backend folder:

```bash
cp .env.example .env
```

| Variable | Description | Example |
|---|---|---|
| `APP_NAME` | Name of the service | `"Agentic Customer Support Automation"` |
| `APP_ENV` | Environment (`development`, `staging`, `production`) | `production` |
| `DEBUG` | Enable debug logs | `false` |
| `DATABASE_URL` | PostgreSQL async connection string | `postgresql+asyncpg://user:pass@host:5432/db` |
| `JWT_SECRET` | Strong secret key (min 32 chars) | `your-secure-random-32-character-secret` |
| `GEMINI_API_KEY` | Google AI Studio API Key | `AIzaSy...` |
| `CORS_ORIGINS` | Comma-separated allowed web origins | `http://localhost:3000,https://app.example.com` |
| `DB_POOL_SIZE` | Async database connection pool size | `20` |
| `DB_MAX_OVERFLOW`| Max overflow connections | `10` |
| `RAG_TOP_K` | Number of document chunks to retrieve | `5` |
| `RAG_RELEVANCE_THRESHOLD`| Cosine similarity threshold for RAG | `0.55` |

---

## 🏁 Quickstart & Local Setup

### 1. Backend Setup

```bash
# Create and activate Python virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1    # On Windows
# source .venv/bin/activate     # On macOS/Linux

# Install dependencies
pip install -r backend/requirements.txt

# Run database migrations
cd backend
alembic upgrade head
cd ..

# Ingest Knowledge Base documents
python -m backend.app.rag.ingest

# Start backend dev server (port 8000)
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Frontend Setup

```bash
cd frontend

# Install Node dependencies
npm install

# Start Next.js development server (port 3000)
npm run dev
```

Visit **`http://localhost:3000`** in your browser to interact with the customer portal and AI support assistant.

---

## 🧪 Running Tests

```bash
# Run backend test suite
pytest backend/tests

# Run specific security hardening tests
pytest backend/tests/test_security_hardening.py
```

---

## 📡 API Endpoints Reference

- `POST /api/auth/register` - Create customer account
- `POST /api/auth/login` - Obtain JWT access token
- `GET /api/auth/me` - Current authenticated user
- `POST /api/support/query` - Multi-agent conversation endpoint
- `POST /api/rag/query` - Direct knowledge base query
- `GET /api/orders/{order_number}` - Authenticated order status
- `POST /api/orders/{order_number}/cancel` - Request order cancellation
- `POST /api/orders/{order_number}/refund` - Request order refund
- `GET /api/tickets/{ticket_number}` - Support ticket status
- `POST /api/tickets` - Open new support ticket
- `GET /health` - System health check & request ID
- `GET /health/db` - Database connectivity verification
