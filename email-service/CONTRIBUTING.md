# Contributing

Thanks for contributing to Email Service.

## Setup

Prerequisites:

- Node.js 20+
- pnpm 10+
- PostgreSQL

Install dependencies:

```bash
pnpm install
```

Run locally:

```bash
pnpm dev
```

## Branches and PRs

- Branch from `staging` by default when available, otherwise `main`.
- Open PRs to `staging` for active development and `main` for release-ready changes.
- Keep PRs focused and small when possible.
- Link issues in PRs using `Closes #<issue-number>`.

## CI expectations

CI runs lint and build on pushes and pull requests.

Run before opening a PR:

```bash
pnpm lint
pnpm build
```

## Deployment

Container deployment workflow runs on pushes to `main` and can be run manually.

Required repository secrets for SSH deploy step:

- `DEPLOY_HOST`
- `DEPLOY_USER`
- `DEPLOY_KEY`

If deploy secrets are missing, only image build/push runs.

## Security

- Never commit secrets.
- Use `.env` locally and keep `.env.example` updated when config changes.
