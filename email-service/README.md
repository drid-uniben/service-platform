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
