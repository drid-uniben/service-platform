# Storage Service

Object-storage API built with FastAPI, SQLAlchemy, Alembic, PostgreSQL, and VPS-mounted disk storage.

## Setup

1. Copy environment variables:

```bash
cp .env.example .env
```

2. Install dependencies (uv-managed virtual environment):

```bash
uv sync --group dev
```

Use uv dependency management commands directly:

```bash
uv add <package>
uv add --dev <package>
uv remove <package>
```

3. Run migrations:

```bash
uv run alembic upgrade head
```

4. Start development server:

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 3000
```

## Migration Workflow

Migrations are intentionally created manually by developers when schema changes are made.

```bash
uv run alembic revision --autogenerate -m "describe_change"
uv run alembic upgrade head
```

## Run With Docker Compose

```bash
docker compose up --build
```

The compose setup only runs the storage service. Provide `DATABASE_URL` in `.env` so it can connect to your external PostgreSQL database.

## Required Env

- `DATABASE_URL`: PostgreSQL SQLAlchemy connection string for an existing database.
- `STORAGE_ROOT`: absolute path where files are written (default: `/data/storage`).
- `API_KEY_RATE_LIMIT_PER_MINUTE`: set `0` to disable rate limiting.

## Core Endpoints

- `POST /auth/keys`: create an account and API key.
- `POST /objects/store`: queue object storage to local disk (requires `x-api-key`).
- `POST /objects/upload`: upload a file directly to local disk as `multipart/form-data` (requires `x-api-key`).
- Include `visibility=public` when creating or uploading if you want the file served without auth; default is `private`.
- `GET /objects/public/{accountId}/{objectKey:path}`: fetch a public file directly by path.
- `GET /objects/{id}`: check object status (requires `x-api-key`).
- `POST /webhooks`: register webhook endpoint (requires `x-api-key`).

## Modular Structure

```text
app/
	api/            # HTTP layer: routes and router composition
	core/           # cross-cutting concerns (errors, request context)
	dependencies/   # FastAPI dependencies (auth, db)
	models/         # SQLAlchemy models by domain
	repositories/   # persistence access patterns
	schemas/        # Pydantic schemas and response mappers
	services/       # business logic orchestration
```

Detailed architecture notes: `docs/architecture.md`

## Architecture Highlights

- Thin route handlers with service orchestration and schema mappers.
- Repository layer to isolate SQLAlchemy query/write concerns.
- Background storage processing to mounted disk (`STORAGE_ROOT`).
- Hashed API key auth and in-memory rate limiting.
- Provider attempt logging and signed webhook dispatch.
