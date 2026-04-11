# Security Policy

Email Service takes security seriously. If you find a vulnerability, report it privately.

## Reporting a vulnerability (private)

Preferred:

1. Go to the repository's Security tab.
2. Click Report a vulnerability.
3. Submit a private report (GitHub Security Advisory).

If private reporting is unavailable, contact maintainers directly via GitHub.
Do not open a public issue with exploit details.

## What to include

Please include as much of the following as possible:

- A clear description of the vulnerability and its impact
- Affected component(s): API, email delivery, CI/workflows, Docker/deployment
- Steps to reproduce (or a proof-of-concept)
- Any relevant logs, request/response examples, or screenshots
- Whether the issue is reliably reproducible
- Suggested mitigation/fix (if you have one)

## Scope

In-scope examples include:

- Authentication/authorization issues
- API key handling and secrets exposure
- Injection issues (SQL/ORM, command injection)
- Sensitive data exposure in responses, logs, or workflows
- Email/webhook signature and replay handling
- GitHub Actions/workflow security issues (token leakage, unsafe script usage, over-broad permissions)

Out-of-scope (unless there is a real security impact):

- Purely theoretical issues without a plausible exploit
- Low-severity UX bugs that do not expose data or change authorization

## Supported versions

Security fixes are applied to the default branch (`main`) and may be backported by maintainers.

## Coordinated disclosure

- Keep vulnerability details private until a fix is released.
- Maintainers will acknowledge receipt and coordinate verification/remediation timelines.

## Safe testing guidelines

- Do not run denial-of-service tests against shared/public environments.
- Do not access or modify real user data.
- Use test accounts and local/dev environments whenever possible.
