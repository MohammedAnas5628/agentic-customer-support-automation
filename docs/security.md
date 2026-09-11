# Authentication and Authorization

## Authentication

Register with `POST /api/auth/register`, then log in with
`POST /api/auth/login` using the registered email and password. Login returns
a JWT bearer token. Send it on protected requests as:

```http
Authorization: Bearer <access_token>
```

Set `JWT_SECRET` in the backend environment to a random value of at least 32
bytes. Tokens use the configured expiration and `HS256` by default. Passwords
are stored as Argon2 hashes, never plaintext.

## Roles and ownership

New accounts have the `customer` role. Customers can access only their own
profile, orders, refunds, and tickets. `support` and `admin` users may access
broader customer-scoped resources. The role is stored on `customers.role`.

Path IDs and request-body customer IDs are not authorization credentials. API
dependencies derive identity from the verified JWT and compare ownership
before calling existing services.

## Agents and tools

Agents receive authenticated identity context separately from user/LLM text.
Order, Support, and Escalation tools validate ownership and business rules
before delegating to SQLAlchemy services. LLM-provided customer, order, or
ticket identifiers cannot grant access or bypass those checks.

## Local setup

Required environment variable:

```env
JWT_SECRET=<random-secret-at-least-32-bytes>
```

Apply migrations with:

```powershell
backend\venv\Scripts\alembic.exe -c backend\alembic.ini upgrade head
```