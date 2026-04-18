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