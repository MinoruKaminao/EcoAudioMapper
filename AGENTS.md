# AGENTS.md

## Project
EcoAudio Mapper

## Mission
Build a public GitHub project for extracting audio from geo-tagged and time-stamped videos, identifying candidate biological sounds, and visualizing spatial and temporal distribution on maps and analysis views.

## Repository Working Rules
- This repository is public.
- Never commit secrets, private keys, tokens, real credentials, or personal location data that should not be disclosed.
- Never commit raw private field recordings unless they are explicitly approved for publication.
- Prefer synthetic, anonymized, or masked sample data for tests and demos.
- Treat protected species coordinates and precise timestamps as sensitive outputs even if the codebase is public.
- Keep documentation and implementation aligned. If behavior changes, update docs in the same change set when practical.

## Source-of-Truth Design References
Before any UI proposal or implementation, read and follow:
1. `docs/design/ui-design-policy.md`
2. `docs/design/ui-review-checklist.md`
3. `docs/design/apple-hig-short.md`
4. `docs/design/agent-instructions.md`

## UI Direction
Use Apple Human Interface Guidelines as the authority for:
- interaction behavior
- navigation
- accessibility
- readability
- platform conventions

Use NeXTSTEP / OPENSTEP / GNUstep only as inspiration for:
- pane-based composition
- workspace seriousness
- inspector-oriented workflows
- restrained neutral visual tone
- disciplined toolbar and sidebar structure

Priority rule:
- behavior = Apple
- usability = Apple
- accessibility = Apple
- visual spirit = OpenStep-inspired modern workstation UI

Do not create a nostalgic replica.
Do not introduce generic SaaS card-heavy layouts on desktop.
Do not sacrifice clarity or accessibility for retro styling.

## Product UI Character
The product should feel:
- calm
- precise
- technical
- professional
- structured
- minimal
- efficient
- timeless

Avoid:
- flashy gradients
- toy-like styling
- oversized rounded cards
- decorative shadows
- excessive empty space
- mobile-first sparse layouts on desktop

## Expected Desktop Composition
Prefer this structure when appropriate:
- left sidebar: navigation, hierarchy, source list
- center pane: main workspace
- right pane: inspector / metadata / detail editing
- top toolbar: essential actions only
- bottom status area: only when operational awareness clearly benefits

## Mandatory UI Output Format
For every UI-related proposal, review, or implementation plan, use these headings exactly:
- Purpose
- Apple HIG Basis
- NeXT / OPENSTEP / GNUstep Influence
- Layout Description
- Interaction Behavior
- Visual Styling Notes
- Accessibility Notes
- Implementation Considerations
- Self-Check Result

## Agent Roles
Multiple agents may collaborate. Use the following responsibilities.

### 1. Product / Requirements Agent
Responsible for:
- requirements refinement
- use cases
- scope management
- acceptance criteria
- traceability

Outputs:
- requirements docs
- issue breakdown
- acceptance checklist

### 2. System Architecture Agent
Responsible for:
- service boundaries
- async pipeline design
- data flow
- deployment topology
- external integrations

Outputs:
- architecture docs
- sequence and component diagrams
- technical decision proposals

### 3. Backend Agent
Responsible for:
- API design
- domain logic
- job orchestration
- permissions
- validation
- export logic

Outputs:
- endpoint specs
- service implementation
- tests

### 4. Database Agent
Responsible for:
- PostgreSQL/PostGIS schema
- migration design
- indexing
- data lifecycle
- auditability
- masking strategy

Outputs:
- DDL
- migration files
- ORM models
- query tuning notes

### 5. ML / Audio Agent
Responsible for:
- audio preprocessing
- segment extraction
- inference pipeline
- model integration
- reproducibility
- evaluation metrics

Outputs:
- inference modules
- experiment notes
- model version handling
- evaluation reports

### 6. GIS / Analytics Agent
Responsible for:
- spatial queries
- clustering / heatmaps
- time-bucket aggregation
- trend analysis
- export formats such as GeoJSON

Outputs:
- geospatial service logic
- analytical query specs
- dashboard data contracts

### 7. UI / UX Agent
Responsible for:
- information architecture
- screen design
- workflow efficiency
- Apple HIG compliance
- OpenStep-inspired composition
- accessibility review

Outputs:
- screen specs
- interaction notes
- UI review findings
- implementation-ready behavior definitions

### 8. QA / Test Agent
Responsible for:
- test strategy
- API and UI test cases
- accessibility checks
- regression design
- acceptance validation

Outputs:
- test plans
- test cases
- release readiness review

### 9. Documentation Agent
Responsible for:
- README
- setup guides
- architecture docs
- contributor guidance
- developer onboarding
- changelog support

Outputs:
- repository docs
- public-facing technical explanations
- docs consistency updates

### 10. Security / Privacy Agent
Responsible for:
- secret handling
- data exposure review
- masking rules
- protected species disclosure controls
- dependency review

Outputs:
- security notes
- privacy risk register
- mitigation guidance

## Standard Prompt Stack
When an agent starts work, it should use this prompt stack in order.

1. `docs/agents/common/project-context.md`
2. `docs/agents/common/repository-rules.md`
3. `docs/design/ui-design-policy.md`
4. `docs/design/ui-review-checklist.md`
5. `docs/design/apple-hig-short.md`
6. `docs/design/agent-instructions.md`
7. role-specific prompt from `docs/agents/roles/`
8. task-specific brief from `docs/plan/` or issue text

## Required Delivery Behavior for All Agents
- State assumptions explicitly.
- Prefer concrete outputs over abstract advice.
- Preserve compatibility with existing docs unless the task is a redesign.
- For changes touching public-facing behavior, propose acceptance criteria.
- For UI work, define normal, loading, empty, error, offline, success, and permission-denied states.
- For database work, mention migration impact and rollback considerations.
- For ML work, include reproducibility and evaluation notes.
- For privacy-sensitive features, identify masking and disclosure implications.

## Coding and Review Rules
- Keep commits focused and explain intent.
- Prefer small, reviewable changes.
- Do not silently rename major concepts without updating docs.
- Add or update tests when changing behavior.
- Avoid introducing unnecessary dependencies.
- Use native platform patterns in UI unless deviation is justified.

## Self-Check Before Finalizing
Every agent should verify:
- Does this change fit the project mission?
- Does it preserve public-repo safety?
- Does it keep protected data out of the repository?
- Does it align with Apple usability and accessibility expectations?
- Does it reflect OpenStep-like structure through composition, not imitation?
- Is it implementation-oriented and testable?

If any answer is no, revise before finalizing.
