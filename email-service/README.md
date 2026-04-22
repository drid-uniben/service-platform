# Email Abstraction Service

API-first, provider-agnostic email delivery backend built with NestJS, TypeScript, PostgreSQL (Prisma), and Redis (BullMQ).

## Setup

Set `SHADOW_DATABASE_URL` in `.env` for local development migrations if Prisma requests a shadow database.

1. Copy environment variables:

```bash
cp .env.example .env
```

2. Install dependencies:

```bash
pnpm install
```

3. Generate Prisma client:

```bash
pnpm prisma:generate
```

4. Run database migrations:

```bash
pnpm prisma:migrate
```

5. Start in development:

```bash
pnpm dev
```

## OpenAPI Docs

- Swagger UI: `http://localhost:3000/docs`
- OpenAPI JSON: `http://localhost:3000/docs-json`
- OpenAPI YAML (committed): `docs/openapi.yaml`
- Auth: click `Authorize` in Swagger UI and provide `x-api-key`.

## Core Endpoints

- `POST /auth/keys` create an account + API key
- `POST /emails/send` queue email send (requires `x-api-key`)
- `POST /emails/send-invitation` queue DRID invitation email using a built-in template (requires `x-api-key`)
- `GET /emails/:id` check email status (requires `x-api-key`)
- `POST /webhooks` register webhook endpoint (requires `x-api-key`)

## Architecture Highlights

- Provider abstraction via `EmailProvider` interface
- SMTP-based delivery provider (Nodemailer)
- In-process retry strategy (3 attempts)
- Hashed API key auth
- Provider attempt logging and webhook event emission

## Local Setup and Verification

### Prerequisites
- Node.js installed
- pnpm installed (`npm install -g pnpm`)
- PostgreSQL running locally

### Environment
1. Copy env template:
   ```bash
   cp .env.example .env
   ```
2. Set required variables in `.env` (at minimum):
   - `DATABASE_URL`
   - other required SMTP/Redis/JWT vars from `.env.example`

Example:
```env
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/email_service?schema=public"
```

### Run locally
```bash
pnpm install
pnpm prisma:generate
pnpm prisma:migrate
pnpm dev
```

### OpenAPI docs
- `http://localhost:3000/docs`
- `http://localhost:3000/docs-json`

### Functional test flow
1. `POST /auth/keys`
2. `POST /emails/send` (include `x-api-key`)
3. `GET /emails/{id}`

### CI/CD container publish
GitHub Actions workflow:
- `.github/workflows/deploy-email-service.yml`
Builds and publishes email-service image to GHCR on `staging` updates.
