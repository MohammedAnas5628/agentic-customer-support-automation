# Pre-Production Readiness Checklist

## Current Decision

**Current status: NOT PRODUCTION-READY. Suitable for staging only.**

The backend test suite currently passes 64 tests, but passing unit/integration tests is not enough for production approval. The items below must be completed, evidenced, and signed off before release.

---

## P0: Release Blockers

### Production Environment

- [ ] Create a separate production environment.
- [ ] Use a production PostgreSQL instance with `pgvector` enabled.
- [ ] Confirm production `DATABASE_URL` uses `postgresql+asyncpg`.
- [ ] Store secrets in a secret manager, not in source code or committed `.env` files.
- [ ] Generate a unique production `JWT_SECRET` with at least 32 random characters.
- [ ] Configure a real production Gemini API key with usage limits.
- [ ] Decide whether LangSmith tracing is enabled in production.
- [ ] Set `DEBUG=false` in production.
- [x] Configure allowed frontend/backend origins (CORS middleware & settings.cors_origins implemented).
- [ ] Confirm production domain, DNS, TLS certificate, and renewal process.

### Database

- [ ] Run all Alembic migrations against a staging database first.
- [ ] Run the conversation-summary migration in staging.
- [ ] Run migrations against production using a controlled release process.
- [ ] Verify all indexes and constraints.
- [ ] Verify the pgvector extension and vector dimension are correct.
- [ ] Seed or ingest the approved knowledge base.
- [ ] Verify the ingestion count and source-document count.
- [ ] Test rollback procedures for migrations.
- [x] Configure connection pool size for expected traffic (`db_pool_size` and `db_max_overflow` implemented in settings and database engine).
- [ ] Configure statement timeout and idle connection handling.
- [ ] Confirm database encryption at rest and in transit.

### Authentication and Authorization

- [ ] Verify registration, login, token expiration, and logout/session behavior.
- [ ] Test invalid, expired, malformed, and forged JWTs.
- [ ] Test customer-to-customer data isolation.
- [ ] Test customer, support, and admin role permissions.
- [ ] Test conversation ownership and cross-user conversation access.
- [ ] Test inactive-account behavior.
- [ ] Add brute-force protection and account lockout or progressive delays.
- [ ] Define JWT rotation/revocation behavior.
- [ ] Verify passwords are never logged or returned by APIs.
- [ ] Verify API keys and database URLs are never logged.

---

## P1: Security Validation

### API Security

- [ ] Run authenticated and unauthenticated API tests against staging.
- [ ] Verify rate limits for login, registration, support, and RAG endpoints.
- [ ] Test rate-limit behavior under concurrent requests.
- [ ] Verify request body and query-size limits.
- [ ] Test malformed JSON and invalid content types.
- [ ] Test SQL injection payloads against every input-bearing endpoint.
- [ ] Test XSS payloads in customer names, tickets, messages, and search fields.
- [ ] Test prompt injection and jailbreak payloads through support and RAG APIs.
- [ ] Test path traversal and command-injection payloads where file or shell input exists.
- [ ] Test SSRF only if the application accepts customer-controlled URLs.
- [x] Verify CORS policy is restrictive and production-specific.
- [x] Verify security headers in production responses (nosniff, DENY, no-referrer, CSP, HSTS).
- [ ] Run dependency vulnerability scanning.
- [ ] Run secret scanning on the Git history and repository.
- [ ] Perform an external or internal penetration test.

### Data Protection

- [ ] Define PII and sensitive-data classification.
- [ ] Confirm customer messages and conversation summaries do not contain secrets.
- [ ] Define retention and deletion rules for conversations and messages.
- [ ] Test customer data export/deletion requirements if applicable.
- [ ] Encrypt backups.
- [ ] Restrict database and log access by role.
- [ ] Document incident response for data exposure.

---

## P1: Logging and Monitoring

### What Exists Now

- [x] Python `logging` calls exist in RAG, workflow, ingestion, and memory-compaction code.
- [x] RAG failures and workflow-agent failures are logged with stack traces.
- [x] `/health` endpoint exists.
- [x] `/health/db` endpoint exists.
- [x] Optional LangSmith configuration exists.
- [x] Rate limiting exists in the application.

### What Is Missing or Incomplete

- [ ] Centralized structured application logs.
- [ ] JSON log format for production ingestion.
- [x] Request ID or correlation ID on every request (`X-Request-ID` attached to all incoming/outgoing requests).
- [x] Request method, route, status, duration, and request ID logging (`electromart.access` logger).
- [ ] Authentication success/failure event logging without credentials.
- [ ] Authorization-denied event logging without sensitive payloads.
- [ ] Conversation and escalation audit events.
- [ ] Database error and slow-query logging.
- [ ] Log redaction for passwords, tokens, API keys, cookies, and PII.
- [ ] Log retention, rotation, access control, and deletion policy.
- [ ] Error tracking service such as Sentry or an equivalent.
- [ ] Metrics endpoint or metrics exporter.
- [ ] Request throughput metrics.
- [ ] API latency metrics, including p50, p95, and p99.
- [ ] HTTP error-rate metrics by route.
- [ ] Rate-limit rejection metrics.
- [ ] Database connection-pool metrics.
- [ ] Database query-latency metrics.
- [ ] Gemini request latency, error, retry, and timeout metrics.
- [ ] Gemini token and cost tracking.
- [ ] RAG embedding latency metrics.
- [ ] RAG retrieval latency metrics.
- [ ] Recall, precision, hit rate, MRR, and nDCG tracking over evaluation runs.
- [ ] Hallucination and citation-quality tracking.
- [ ] Conversation-memory compaction count, duration, and failure metrics.
- [ ] Dashboard for service, database, API, and AI health.
- [ ] Alerts for uptime, error rate, latency, database health, rate-limit spikes, AI failures, and cost thresholds.
- [ ] On-call ownership and alert escalation policy.

### Minimum Production Alerts

- [ ] Backend health check fails.
- [ ] Database health check fails.
- [ ] HTTP 5xx rate exceeds threshold.
- [ ] p95 API latency exceeds threshold.
- [ ] Authentication failure spike occurs.
- [ ] Rate-limit rejection spike occurs.
- [ ] Gemini failure or timeout rate exceeds threshold.
- [ ] RAG no-context rate exceeds threshold.
- [ ] Database pool exhaustion occurs.
- [ ] Disk, memory, or CPU usage exceeds threshold.
- [ ] Gemini spend exceeds budget.

---

## P1: AI and RAG Quality

### Knowledge Base

- [ ] Approve all production knowledge documents.
- [ ] Remove stale, duplicate, contradictory, and test documents.
- [ ] Define document ownership and review dates.
- [ ] Define an ingestion approval process.
- [ ] Test parsing, cleaning, chunking, metadata, and embedding generation.
- [ ] Verify every source document is represented after ingestion.
- [ ] Define incremental indexing behavior for changed documents.
- [ ] Define deletion behavior for removed documents.

### Retrieval

- [ ] Create a versioned golden evaluation dataset.
- [ ] Measure Recall@K on real representative questions.
- [ ] Measure Precision@K, hit rate, MRR, and nDCG.
- [ ] Compare current reranking against the previous baseline.
- [ ] Evaluate top-k and relevance-threshold settings.
- [ ] Test ambiguous, misspelled, short, and multi-intent questions.
- [ ] Evaluate product catalog retrieval separately from policy retrieval.
- [x] Evaluate hybrid keyword/vector search (hybrid dense vector + lexical overlap scoring and multi-query expansion implemented in retrieval.py).
- [ ] Evaluate metadata filtering and category filtering.
- [ ] Test embedding model version changes before deployment.
- [ ] Define retrieval regression thresholds that block releases.

### Generation

- [ ] Measure groundedness and faithfulness using a golden dataset.
- [ ] Measure citation accuracy and citation completeness.
- [ ] Detect unsupported claims.
- [ ] Measure hallucination rate with human or automated review.
- [ ] Test prompt injection, jailbreaks, and retrieved-document injection.
- [ ] Test refusal behavior for unsupported questions.
- [ ] Test product recommendations for relevance, disclosure, alternatives, and no-pressure behavior.
- [ ] Test that support requests are resolved before any recommendation.
- [ ] Test that the assistant does not invent prices, discounts, stock, compatibility, or urgency.
- [ ] Test model timeout, quota, malformed output, and provider outage behavior.
- [ ] Define model version pinning and fallback behavior.

### Conversation Memory

- [ ] Apply the conversation-summary migration in staging and production.
- [ ] Test raw-message retention and summary persistence.
- [ ] Test compaction at the configured message threshold.
- [ ] Test summary failure without losing the customer turn.
- [ ] Test summary prompt injection resistance.
- [ ] Test conversation ownership and deletion behavior.
- [ ] Test long conversations, repeated compaction, and summary drift.
- [ ] Define summary retention and maximum storage limits.
- [ ] Measure memory retrieval quality on follow-up questions.

---

## P1: Functional and End-to-End Testing

- [ ] Run the full backend suite in CI.
- [ ] Add frontend unit/component tests.
- [ ] Run frontend typecheck.
- [ ] Run frontend production build.
- [ ] Test registration and login through the browser.
- [ ] Test authenticated support chat through the browser.
- [ ] Test conversation follow-up and refresh persistence.
- [ ] Test product listing, search, and detail pages.
- [ ] Test customer profile and account pages.
- [ ] Test order viewing and ownership restrictions.
- [ ] Test cancellation and refund flows.
- [ ] Test ticket creation and updates.
- [ ] Test RAG API responses and source citations.
- [ ] Test database transaction rollback paths.
- [ ] Test empty, null, oversized, duplicate, and malformed inputs.
- [ ] Test network timeout and provider failure behavior.
- [ ] Test smoke tests after deployment.
- [ ] Test regression tests after every release.
- [ ] Obtain business-owner acceptance approval.

---

## P1: Performance and Scalability

- [ ] Define traffic, concurrency, latency, and availability targets.
- [ ] Run API load tests.
- [ ] Run spike tests.
- [ ] Run endurance/soak tests.
- [ ] Measure login and CRUD latency.
- [ ] Measure RAG retrieval latency.
- [ ] Measure Gemini first-token and total response latency.
- [ ] Test concurrent support conversations.
- [ ] Test database pool behavior under load.
- [ ] Test rate limiter behavior under load.
- [ ] Identify CPU, memory, database, embedding, and LLM bottlenecks.
- [ ] Define horizontal-scaling requirements.
- [ ] Define worker/background-job requirements if ingestion moves off-request.
- [ ] Estimate cost per support request and per RAG request.
- [ ] Define Gemini quota and cost controls.
- [ ] Configure caching only after measuring a real bottleneck.

---

## P1: Reliability and Disaster Recovery

- [ ] Configure automated database backups.
- [ ] Test database restore from backup.
- [ ] Define RPO and RTO.
- [ ] Test application restart and health recovery.
- [ ] Test database outage behavior.
- [ ] Test Gemini outage and timeout behavior.
- [ ] Test partial RAG/indexing failure behavior.
- [ ] Test migration rollback or recovery.
- [ ] Define disaster-recovery runbook.
- [ ] Define business-continuity runbook.
- [ ] Define incident severity and escalation process.
- [ ] Test rollback to the previous application release.

---

## P2: Deployment and Operations

- [ ] Create reproducible CI/CD pipeline.
- [ ] Add automated tests to pull requests.
- [ ] Add dependency and secret scanning to CI.
- [ ] Build a production artifact or container.
- [ ] Pin and audit dependency versions.
- [ ] Add startup and readiness checks.
- [ ] Configure reverse proxy/load balancer.
- [ ] Configure HTTPS termination.
- [ ] Configure process supervision and automatic restart.
- [ ] Define blue-green or canary deployment strategy.
- [ ] Test deployment rollback.
- [ ] Separate development, staging, and production configuration.
- [ ] Document deployment ownership and release approval.
- [ ] Remove generated synthetic reports/tests if they are not authoritative project artifacts.
- [x] Review the corrupted root filename and remove it (deleted confirmed corrupted PowerShell paste file).

---

## Production Approval Evidence

Before approval, attach or link:

- [ ] Test report with pass/fail results.
- [ ] Security assessment and remediation evidence.
- [ ] Dependency vulnerability report.
- [ ] RAG evaluation report with baseline comparison.
- [ ] Performance/load-test report.
- [ ] Browser E2E test report.
- [ ] Database migration result.
- [ ] Backup and restore evidence.
- [ ] Monitoring dashboard link.
- [ ] Alert test evidence.
- [ ] Incident-response runbook.
- [ ] Rollback test evidence.
- [ ] Business-owner/UAT approval.

## Final Release Gate

Production release is approved only when all P0 and P1 items are complete, evidence is attached, staging smoke tests pass, and an accountable owner signs off.
