# Security Remediation Approach

## Scope
This pass addresses the reported **critical and high-priority** issues only. Medium and low-priority quality, performance, and observability work will be reviewed separately after these fixes are verified.

## Approach

1. **JWT secret enforcement**
   - Make `JWT_SECRET` a required setting.
   - Reject empty or short secrets during application startup/configuration.
   - Keep the existing runtime guard in token creation and verification as defense in depth.
   - Add focused tests for missing, short, and valid secrets.

2. **Secret handling**
   - Represent Gemini and LangSmith credentials as secret values so their normal string representation is masked.
   - Pass the underlying value only at the SDK boundary where it is required.
   - Keep credentials sourced from environment/configuration rather than source code.

3. **Request validation and abuse-resistant input boundaries**
   - Enforce trimmed, bounded text fields at Pydantic schema boundaries for authentication, RAG, support, and ticket inputs.
   - Reject control characters and common payloads that are not valid for the corresponding field.
   - Do not rely on regexes as SQL protection; database access must continue to use SQLAlchemy bound parameters.
   - Treat prompt-injection text as untrusted user content and preserve the existing grounding boundary.

4. **Rate limiting**
   - Add application-wide request limiting with stricter limits for authentication and expensive AI endpoints.
   - Use client IP as the default limiter key and return HTTP 429 when a limit is exceeded.
   - Keep the configuration explicit and environment-controlled so deployment can tune it.

5. **Security headers**
   - Add middleware for `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, and a conservative `Content-Security-Policy`.
   - Add HSTS only when the application is running in a non-development environment, since HSTS on local HTTP can make development awkward.

6. **Verification**
   - Run focused security/configuration tests first.
   - Run the existing authentication tests and import/compile checks.
   - Record unresolved medium/low issues and any environment-dependent checks for the next decision point.

## Explicit Non-goals for This Pass

- RAG recall/reranking and hallucination-rate improvements.
- Full penetration testing or production load testing.
- Database migration, schema redesign, or deployment changes.
- Rewriting the earlier synthetic test suite; its reported metrics are treated as indicators, not production measurements.

## Verified Result

- Focused hardening and authentication tests: **9 passed**.
- Full backend test suite: **62 passed**.
- Remaining warnings are dependency deprecations, not test failures.

## Remaining Work for Approval

- Improve RAG recall, reranking, and hallucination controls.
- Add production-grade load, performance, and deployment tests.
- Add deeper security testing for SSRF, CSRF semantics, dependency scanning, and abuse scenarios.
- Decide whether to add rate-limit response headers through explicit `Response` return types or keep enforcement-only behavior.
- Remove or correct the previously generated synthetic test/report artifacts if they should not be treated as authoritative project tests.
