# Project Context

## Project
EcoAudio Mapper

## Summary
EcoAudio Mapper is a system for extracting audio from geo-tagged and time-stamped videos, identifying candidate biological sounds, and visualizing their spatial and temporal distribution on maps and analysis views.

## Core User Value
- turn everyday field video into structured ecological observation data
- support non-expert observation collection
- preserve a path for expert review and correction
- enable seasonal and long-term trend analysis
- present results safely in a public-repository development model

## Core Workflows
1. upload a video with location and datetime metadata
2. extract metadata and normalize location/timezone/datetime
3. extract audio and segment relevant intervals
4. run bioacoustic inference and rank candidate species
5. review and correct detections when needed
6. display observations on maps and time-based analytics views
7. export filtered results for GIS and analysis

## Product Constraints
- repository is public
- code must not assume access to private field recordings
- protected species coordinates and precise timestamps may require masking
- reproducibility matters for ML and analytics workflows
- Apple HIG governs behavior and usability
- NeXT / OPENSTEP / GNUstep influence is limited to visual structure and atmosphere

## Primary Target
Desktop-first productivity application with prolonged use, high information density, keyboard support, and pane/inspector workflows where appropriate.

## Expected Architecture Direction
- Web or desktop-oriented client
- API backend
- asynchronous job pipeline
- PostgreSQL + PostGIS
- object storage for media artifacts
- inference pipeline with model versioning
- analytics layer with time-zone-aware aggregation

## Sensitive Data Notes
Treat the following as potentially sensitive:
- exact coordinates for protected species
- exact timestamps that could expose nest/roost patterns
- raw private media
- user identity data
- secret keys, environment files, infrastructure credentials

## Current Repository Goals
- establish repository-safe development structure
- define shared prompt and design rules for multiple agents
- prepare implementation-ready documentation and scaffolding
