# EcoAudio Mapper

EcoAudio Mapper is a system for extracting audio from geo-tagged and time-stamped videos, identifying candidate biological sounds, and visualizing their spatial and temporal distribution on maps and analysis views.

## Goals
- turn everyday field video into structured ecological observation data
- support non-expert observation collection
- preserve expert review and correction workflows
- enable seasonal and long-term environmental analysis
- provide a safe public-repository development model

## Core Capabilities
- upload geo-tagged and time-stamped videos
- extract metadata, audio, and observation context
- segment audio for analysis
- run bioacoustic inference and rank candidate species
- support expert review and correction
- visualize observations on maps
- analyze occurrence by time, season, and year
- export filtered results for GIS and analytics use

## Product Direction
This product should behave like a modern Apple-native application while expressing the structural discipline and professional atmosphere of NeXTSTEP / OPENSTEP / GNUstep.

### UI Principles
- Apple HIG first for behavior, usability, and accessibility
- OpenStep-inspired composition for layout and atmosphere
- desktop productivity density where appropriate
- restrained neutral styling
- pane-based workflows with sidebar / main workspace / inspector when useful

## Repository Structure
```text
docs/        documentation, requirements, design, plans, tests, operations
openapi/     API specifications
db/          DDL, seeds, migrations support, query examples
alembic/     database migrations
backend/     backend application and services
frontend/    frontend application
ml/          audio and inference related code
scripts/     local development scripts
docker/      container definitions
```

## Development History

### Implemented initial backend slice
- added backend bootstrap and app entrypoint in `backend/app/main.py`
- added configuration loading in `backend/app/core/config.py`
- added SQLAlchemy base and session wiring in `backend/app/db/base.py` and `backend/app/db/session.py`
- added Alembic bootstrap files in `alembic.ini` and `alembic/env.py`
- added minimal observation list API in `backend/app/api/v1/observations.py`
- added minimal observation schema and ORM model in `backend/app/schemas/observation.py` and `backend/app/db/models/observation.py`
- added backend bootstrap and observation API tests in `backend/tests/conftest.py` and `backend/tests/api/test_bootstrap.py`

### Implemented initial frontend slice
- added Next.js frontend bootstrap in `frontend/package.json`, `frontend/tsconfig.json`, and `frontend/next-env.d.ts`
- added app entry files in `frontend/src/app/layout.tsx` and `frontend/src/app/page.tsx`
- added first desktop-oriented workspace shell in `frontend/src/components/workspace-shell.tsx`
- added global desktop UI styling in `frontend/src/app/globals.css`
- changed frontend dev and start port to `3102` in `frontend/package.json`

### Added operation and implementation documentation
- added operation guides in `docs/operation/operation_guide_en.md` and `docs/operation/operation_guide_ja.md`
- added implemented feature guides in `docs/operation/implemented_features_en.md` and `docs/operation/implemented_features_ja.md`

### Added PostgreSQL-oriented backend environment example
- expanded `.env.example` with PostgreSQL host, port, database, user, and password variables
