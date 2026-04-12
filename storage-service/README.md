# Storage Service

API-first object storage backend built with FastAPI, SQLAlchemy, Alembic, PostgreSQL, and VPS-mounted disk storage.

## Setup

1. Copy environment variables:

```bash
cp .env.example .env
```

2. Install dependencies:

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

3. Create and run database migrations:

```bash
uv run alembic revision --autogenerate -m "init"
uv run alembic upgrade head
```

4. Start in development:

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 3000
```

## Run With Docker Compose

```bash
docker compose up --build
```

## Required Env

- `DATABASE_URL` PostgreSQL SQLAlchemy connection string
- `STORAGE_ROOT` absolute path where files are written (default: `/data/storage`)
- `API_KEY_RATE_LIMIT_PER_MINUTE` set `0` to disable rate limiting

## Core Endpoints

- `POST /auth/keys` create an account + API key
- `POST /objects/store` queue object storage to local disk (requires `x-api-key`)
- `GET /objects/{id}` check object status (requires `x-api-key`)
- `POST /webhooks` register webhook endpoint (requires `x-api-key`)

## Architecture Highlights

- FastAPI request lifecycle with request-id logging middleware
- SQLAlchemy ORM models and Alembic migrations
- Background storage processing to mounted disk (`STORAGE_ROOT`)
- Hashed API key auth + in-memory rate limiting
- Provider attempt logging and signed webhook dispatch
