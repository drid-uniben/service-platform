# DRID Services Platform – Architecture

## Overview

This document describes the technical architecture of the DRID Services Platform, including how services communicate, how authentication is handled, and how requests flow through the system.

---

## High-Level Architecture

The platform consists of the following components:

### Backend Services
- Authentication Service
- Storage Service
- Email Service

### Frontend
- Service Dashboard (Control Panel)

Each backend service:
- Runs independently
- Has its own codebase and deployment pipeline
- Exposes its own API
- Verifies authentication tokens locally

The Service Dashboard provides a centralized interface for interacting with these services.

---

## Core Design Principles

### 1. Service Independence

Each service is fully independent:

- Own codebase
- Own database (if applicable)
- Own deployment lifecycle

Services do **not share code** and do not rely on each other for request-time operations unless explicitly required.

---

### 2. Stateless Authentication (JWT)

Authentication is handled using JSON Web Tokens (JWT):

- The Auth Service issues signed tokens
- Other services verify tokens locally using a public key
- No per-request call to Auth Service is required

---

### 3. Separation of Concerns

- Auth Service → identity + token issuance
- Services → business logic + authorization
- Dashboard → management and developer interaction

---

## Service Dashboard (Control Panel)

The Service Dashboard is a frontend application similar to a cloud provider control panel (e.g., AWS console).

It communicates with backend services via their public APIs.

### Responsibilities

- User authentication (via Auth Service)
- API token generation and management
- Application/service registration
- Viewing usage and activity
- Managing configurations:
  - Email templates
  - Storage limits
  - Permissions

### Role in Architecture

```
User → Dashboard → Auth Service → JWT
User → Dashboard → Other Services (via API using JWT)
```

The dashboard acts as a **privileged client**, not a backend service.

---

## Authentication Flow

### Step 1: User Login

Client (Dashboard or external app):

```
Client → Auth Service → JWT
```

Auth Service:
- Validates credentials
- Issues a signed JWT

---

### Step 2: Accessing Services

```
Client → Storage Service (Authorization: Bearer <token>)
```

---

### Step 3: Token Verification

Each service:

- Verifies JWT signature locally
- Checks expiration
- Extracts user identity and roles

No call to Auth Service is made during this process.

---

## Authorization Model

JWT contains:

- User ID (`sub`)
- Roles/permissions
- Expiry time

Each service enforces its own authorization rules.

Examples:
- Storage Service controls file access
- Email Service controls sending permissions

---

## Service Communication

### External Requests

All clients (including Dashboard) interact directly with services:

```
Client → Auth Service
Client → Storage Service
Client → Email Service
```

---

### Internal Communication

Services communicate directly only when necessary:

```
Storage Service → Email Service
```

There is no central routing layer at this stage.

---

## API Gateway (Future Consideration)

An API Gateway may be introduced to:

- Provide a unified entry point (`api.unitman.edu`)
- Handle rate limiting
- Centralize logging and monitoring
- Simplify client interaction

Future flow:

```
Client → API Gateway → Services
```

---

## Deployment Model

Each service is deployed independently:

- Separate containers/instances
- Independent scaling
- Independent updates

This ensures:
- Fault isolation
- Flexibility in scaling
- Technology freedom per service

---

## Security Considerations

- JWT tokens must:
  - Be securely signed (RSA recommended)
  - Have short expiration times
- Services must validate tokens correctly
- No sensitive data stored in JWT payloads
- All communication must use HTTPS
- Dashboard access must be role-restricted

---

## Future Improvements

- Token refresh mechanism
- Role-Based Access Control (RBAC)
- API Gateway integration
- Audit logging (especially for dashboard actions)
- Service discovery mechanisms

---

## Summary

The platform follows a decentralized architecture:

- Auth Service issues trusted tokens
- Services validate tokens independently
- No shared code between services
- No central bottleneck for authentication

This design ensures strong isolation, scalability, and long-term flexibility.