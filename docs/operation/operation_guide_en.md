# EcoAudio Mapper Operation Guide

## Purpose
This guide explains how to run and use the currently implemented first slices of EcoAudio Mapper.

The current implementation includes:
- a minimal backend bootstrap API
- a minimal database-backed observation list endpoint
- a first desktop-oriented UI shell

This guide covers only implemented behavior.

## Public Repository Safety Notes
- Do not place real secrets in checked-in files.
- Do not use real private field recordings in this repository.
- Do not expose exact protected-species coordinates or precise timestamps in public materials.
- Use masked, synthetic, or approved demo data for validation.

## Current Implemented Components

### Backend
- application entrypoint
- health endpoint
- observation list endpoint
- configuration loading from environment variables
- SQLAlchemy session wiring
- Alembic bootstrap configuration

### Frontend
- desktop-first workspace shell
- top toolbar
- left navigation sidebar
- central observation workspace
- right inspector pane
- explicit UI state presentation for normal, loading, empty, error, offline, success, and permission-denied style conditions

## Backend Operation

### 1. Prepare the backend environment
From the repository root:

```bash
cd backend
python3 -m venv .venv
./.venv/bin/python -m pip install -e '.[dev]'
```

### 2. Configure environment variables
Use [`backend/app/core/config.py`](../../backend/app/core/config.py) together with [`.env.example`](../../.env.example) as the configuration reference.

Important variables:
- `APP_NAME`
- `ENVIRONMENT`
- `DEBUG`
- `API_V1_PREFIX`
- `ENABLE_DOCS`
- `DATABASE_URL`
- `ALEMBIC_DATABASE_URL`

For local testing, you may provide a local SQLite URL or a local PostgreSQL URL depending on your validation target.

### 3. Run the backend application
From [`backend`](../../backend):

```bash
./.venv/bin/python -m uvicorn app.main:app --reload
```

### 4. Verify backend availability
Open the health endpoint:

- `GET /health`

Expected response structure:

```json
{
  "status": "ok",
  "environment": "development"
}
```

### 5. Use the observation list endpoint
Available endpoint:

- `GET /api/v1/observations?limit=20&offset=0`

Current behavior:
- returns non-deleted observations
- sorts by newest creation time first
- returns a minimal list shape with `id`, `status`, `visibility_level`, and `recorded_at_utc`

## Database Operation

### 1. Migration readiness
Alembic bootstrap files are present in:
- [`alembic.ini`](../../alembic.ini)
- [`alembic/env.py`](../../alembic/env.py)
- [`alembic/versions/0001_initial_schema.py`](../../alembic/versions/0001_initial_schema.py)

### 2. Migration caution
The initial migration targets PostgreSQL/PostGIS-oriented schema behavior.

Before applying to a real database:
- confirm PostgreSQL availability
- confirm PostGIS availability
- confirm safe non-production credentials
- confirm that sample data does not expose sensitive coordinates or timestamps

### 3. Rollback note
At the current stage, newly added application-side DB wiring can be rolled back by reverting code changes.
No new migration revision was introduced in the latest minimal DB slice.

## Frontend Operation

### 1. Prepare the frontend environment
From the repository root:

```bash
cd frontend
npm install
```

### 2. Run the frontend application
From [`frontend`](../../frontend):

```bash
npm run dev
```

The current frontend dev server is configured to use port `3102` in [`frontend/package.json`](../../frontend/package.json).

### 3. Validate the frontend slice
The first UI slice currently presents a static workstation-style shell.

What to look for:
- top toolbar with primary actions
- left navigation sidebar
- center workspace with state list and observation table
- right inspector panel
- visible keyboard focus states
- skip link for direct navigation to the main content

### 4. Type-check the frontend

```bash
npm run typecheck
```

## User Workflow for the Current Slice

### Backend workflow
1. Start the backend.
2. Confirm [`/health`](../../backend/app/main.py).
3. Query [`/api/v1/observations`](../../backend/app/api/v1/observations.py).
4. Confirm the response shape and ordering.

### Frontend workflow
1. Start the frontend.
2. Open the root page.
3. Review the three-pane workspace composition.
4. Confirm that operational states are visible.
5. Confirm that the selected observation details appear in the inspector.

## Troubleshooting

### Backend test command
From [`backend`](../../backend):

```bash
./.venv/bin/python -m pytest
```

### Common issues
- Missing Python dependencies: recreate the virtual environment and reinstall.
- Missing Node dependencies: run `npm install` again in [`frontend`](../../frontend).
- Database connection issues: verify `DATABASE_URL` and DB availability.
- Migration issues: verify PostgreSQL/PostGIS compatibility before applying the initial schema.

## Current Limitations
- no full CRUD observation workflow yet
- no analytics workflow yet
- no ML inference workflow yet
- no live API-connected frontend data flow yet
- no production-ready auth or authorization workflow yet

## Related Implemented Files
- [`backend/app/main.py`](../../backend/app/main.py)
- [`backend/app/api/v1/observations.py`](../../backend/app/api/v1/observations.py)
- [`backend/app/db/models/observation.py`](../../backend/app/db/models/observation.py)
- [`backend/app/db/session.py`](../../backend/app/db/session.py)
- [`frontend/src/app/page.tsx`](../../frontend/src/app/page.tsx)
- [`frontend/src/components/workspace-shell.tsx`](../../frontend/src/components/workspace-shell.tsx)
- [`frontend/src/app/globals.css`](../../frontend/src/app/globals.css)
