# EcoAudio Mapper Implemented Features

## Scope of This Document
This document summarizes only the features that are implemented in the repository at the current stage.

It does not describe the full planned product.

## 1. Backend Bootstrap Features

### 1.1 Application startup
The backend application can be created and started from [`backend/app/main.py`](../../backend/app/main.py).

Implemented behavior:
- app factory setup
- FastAPI initialization
- optional docs exposure through configuration
- router registration for the observation API

### 1.2 Health check endpoint
The system exposes a health endpoint in [`backend/app/main.py`](../../backend/app/main.py).

Implemented behavior:
- `GET /health`
- returns service status and current environment name

## 2. Configuration Features

Configuration is implemented in [`backend/app/core/config.py`](../../backend/app/core/config.py).

Implemented behavior:
- environment-based settings loading
- defaults for local development
- separate Alembic database URL support
- docs enable/disable toggle

Related example file:
- [`.env.example`](../../.env.example)

## 3. Database Wiring Features

### 3.1 SQLAlchemy base and engine setup
Implemented in:
- [`backend/app/db/base.py`](../../backend/app/db/base.py)
- [`backend/app/db/session.py`](../../backend/app/db/session.py)

Implemented behavior:
- shared declarative base
- engine creation from configured database URL
- session factory creation
- request-scoped DB session dependency

### 3.2 Alembic bootstrap readiness
Implemented in:
- [`alembic.ini`](../../alembic.ini)
- [`alembic/env.py`](../../alembic/env.py)
- [`alembic/versions/0001_initial_schema.py`](../../alembic/versions/0001_initial_schema.py)

Implemented behavior:
- Alembic environment setup
- migration configuration using application settings
- initial schema revision available in the repository

## 4. Observation Data Features

### 4.1 Minimal observation ORM model
Implemented in [`backend/app/db/models/observation.py`](../../backend/app/db/models/observation.py).

Implemented behavior:
- minimal mapping for the `observations` table
- fields aligned with the documented initial schema intent for the first read-only slice

### 4.2 Observation list API
Implemented in [`backend/app/api/v1/observations.py`](../../backend/app/api/v1/observations.py).

Implemented behavior:
- `GET /api/v1/observations`
- supports `limit` and `offset`
- excludes soft-deleted rows
- orders by newest created rows first
- returns a minimal response structure

### 4.3 Observation response schema
Implemented in [`backend/app/schemas/observation.py`](../../backend/app/schemas/observation.py).

Implemented behavior:
- summary item shape
- list response shape with paging metadata

## 5. Backend Test Coverage

Implemented in:
- [`backend/tests/conftest.py`](../../backend/tests/conftest.py)
- [`backend/tests/api/test_bootstrap.py`](../../backend/tests/api/test_bootstrap.py)

Implemented behavior:
- temporary SQLite-backed test database
- health endpoint verification
- empty observation list verification
- seeded observation list verification

## 6. Frontend First UI Slice

### 6.1 Frontend application scaffold
Implemented in:
- [`frontend/package.json`](../../frontend/package.json)
- [`frontend/tsconfig.json`](../../frontend/tsconfig.json)
- [`frontend/next-env.d.ts`](../../frontend/next-env.d.ts)
- [`frontend/src/app/layout.tsx`](../../frontend/src/app/layout.tsx)
- [`frontend/src/app/page.tsx`](../../frontend/src/app/page.tsx)

Implemented behavior:
- minimal Next.js app setup
- root layout and page entry
- type-checkable frontend baseline

### 6.2 Desktop workspace shell
Implemented in [`frontend/src/components/workspace-shell.tsx`](../../frontend/src/components/workspace-shell.tsx).

Implemented behavior:
- top toolbar with primary actions
- left navigation sidebar
- center workspace with overview, state section, and observation table
- right inspector pane
- explicit state presentation for required UI conditions

### 6.3 UI styling and accessibility baseline
Implemented in [`frontend/src/app/globals.css`](../../frontend/src/app/globals.css).

Implemented behavior:
- restrained neutral desktop styling
- pane-based composition
- visible keyboard focus styling
- skip link support
- responsive stacking for narrower widths

## 7. What Is Not Yet Implemented
- full observation CRUD
- live frontend integration with backend API
- analytics screens and services
- ML inference workflows
- authentication and authorization flows for production use
- protected-species masking workflow enforcement in the UI
- full review workflow implementation

## 8. Public Safety Notes
- no secrets were introduced in the implemented slice
- no raw private field recordings are included
- no protected-species coordinates are exposed by the implemented documentation or UI mock data
- current sample UI data is static demonstration content

