# ElectroMart RAG

## Architecture

Knowledge-base Markdown files are loaded, split into 145 chunks, embedded with
`models/gemini-embedding-001`, and stored as `VECTOR(3072)` values in
`rag_document_chunks`. A knowledge question is embedded with the same model,
searched using pgvector cosine distance, filtered at a default similarity of
`0.55`, and sent to Gemini only when relevant context exists.

The Knowledge Agent owns retrieval and grounded generation. LangGraph routes
knowledge intents to that agent; other agent routes are unchanged.

## Commands

Populate or replace the knowledge snapshot transactionally:

```powershell
backend\venv\Scripts\python.exe -m backend.app.rag.ingest
```

Run the evaluation questions:

```powershell
backend\venv\Scripts\python.exe -m backend.app.rag.evaluation
```

Run the non-live test suite:

```powershell
backend\venv\Scripts\python.exe -m pytest -q tests/test_document_loader.py backend/tests
```

The tests mock Gemini and database retrieval. Live ingestion and evaluation
require a working `GEMINI_API_KEY` and available Gemini quota.

## Query API

```http
POST /api/rag/query
Content-Type: application/json

{"query":"What is ElectroMart's return policy?"}
```

The response contains `answer`, `sources` with filename and score, and a
`status` of `answered`, `no_context`, or `error`. Weak or empty retrieval is
returned safely without calling the generation model.