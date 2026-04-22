# DRID Services Platform

## Goal

We are building a **centralized services platform** for DRID (Directorate of Research and Innovation, University of Benin) that will provide reusable backend capabilities for current and future applications.

Instead of each project implementing its own authentication, storage, or email system, this platform will act as a **shared infrastructure layer**.

---

## Core Services

### 1. Authentication Service

Handles:

* User registration and login
* JWT-based authentication
* Role/permission management

Purpose: Ensure secure and consistent access control across all DRID applications.

---

### 2. Storage Service

Handles:

* File uploads (documents, images, etc.)
* File retrieval and management
* Access control for stored files

Purpose: Provide a unified system for managing files across the platform.

---

### 3. Email Service

Handles:

* Sending transactional emails (verification, password reset, notifications)
* Template management

Purpose: Centralize all email communication logic.

---

## Service Dashboard

We will also include a **Service Dashboard** to make the platform easier to use and manage.

The dashboard will allow developers and administrators to:

* Generate and manage API tokens
* View and manage applications/services using the platform
* Monitor usage and basic activity
* Configure service-specific settings (e.g., email templates, storage limits)

Purpose: Provide a user-friendly interface for interacting with the platform without needing to manually handle tokens or direct API calls.

---

## Architecture Approach

We are using a **monorepo structure**:

* All services live in a single repository
* Each service is developed as an independent module
* Shared utilities (e.g., database config, types) are reused across services

This allows faster development and easier maintenance while keeping services logically separate.

---

## How It Works Together

* Applications (e.g., journal systems, portals) will **call these services via APIs**
* Each service can run independently but integrates as part of the overall platform

Example:

* A user logs in → Auth Service verifies identity
* User uploads a file → Storage Service handles it
* System sends confirmation → Email Service sends message

---

## Why This Approach

* Avoids duplication of effort
* Ensures consistency across projects
* Makes the system easier to scale and maintain
* Allows future expansion (e.g., adding payments, notifications, analytics)

---

## Summary

We are building a **modular backend platform** with shared services (auth, storage, email) using a single repository for simplicity and speed. Each service is independent but designed to work together as a unified system.

## Documentation
[Architecture](docs/architecture.md)