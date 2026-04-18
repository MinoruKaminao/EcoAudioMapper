# Contributing to EcoAudio Mapper

Thank you for contributing to EcoAudio Mapper.

This repository is public and is intended to support disciplined, reviewable development for ecological audio analysis, geospatial visualization, and time-series observation workflows.

---

## 1. Core Principles

Please keep the following principles in mind:

- keep changes small and reviewable
- keep documentation aligned with implementation
- preserve public-repository safety
- prefer clarity over novelty
- preserve Apple usability and accessibility for UI work
- express NeXT / OPENSTEP / GNUstep influence through structure, not retro imitation

---

## 2. Read Before You Start

Please review these files before making significant changes:

- `AGENTS.md`
- `docs/agents/common/project-context.md`
- `docs/agents/common/repository-rules.md`
- `docs/agents/common/output-contract.md`
- `docs/design/ui-design-policy.md`
- `docs/design/ui-review-checklist.md`
- `docs/design/apple-hig-short.md`
- `docs/design/agent-instructions.md`

If your work affects requirements, architecture, DB design, API contracts, or UI behavior, also review the related files under:

- `docs/requirements/`
- `docs/design/`
- `docs/plan/`
- `docs/test/`
- `docs/operation/`

---

## 3. Branching

Use a focused branch for each change.

Recommended naming examples:

- `feature/map-filters`
- `feature/review-workflow`
- `fix/datetime-normalization`
- `fix/postgis-query-bug`
- `docs/ui-spec-update`

---

## 4. Commit Guidelines

Prefer commits that are:

- focused
- descriptive
- easy to review

Examples:

- `Add initial observation API scaffolding`
- `Define timezone normalization rules`
- `Implement protected species masking service`
- `Refine OpenStep-inspired map workspace layout`

Avoid mixing unrelated changes in the same commit.

---

## 5. Pull Request Expectations

Each pull request should clearly describe:

- what changed
- why it changed
- which files or modules are affected
- what validation was performed
- whether documentation was updated
- whether privacy or security implications exist

A good pull request should also mention:

- migration impact, if schema changes are included
- API contract impact, if request/response behavior changed
- UI impact, if screens, navigation, or workflows changed

---

## 6. Documentation Rule

If behavior, contracts, workflows, architecture, or repository conventions change, update the related documentation in the same change set when practical.

This includes, for example:

- API changes → update `openapi/` and relevant design docs
- DB changes → update DB design and migration docs
- UI changes → update UI specs and related review guidance
- operational changes → update setup/deployment/operation docs

---

## 7. UI Contribution Rule

For any UI-related proposal or implementation:

- Apple Human Interface Guidelines take priority for behavior, usability, and accessibility
- NeXT / OPENSTEP / GNUstep influence should appear through composition and atmosphere
- do not create a nostalgic or literal retro replica
- do not default to generic SaaS card-heavy layouts for desktop workflows
- define loading, empty, error, offline, permission-denied, and success states
- include accessibility considerations

For UI-related written proposals, use the required headings defined in `AGENTS.md` and `docs/design/agent-instructions.md`.

---

## 8. Data and Privacy Rule

Do not commit any of the following:

- secrets
- API keys
- private keys
- tokens
- credentials
- `.env` files other than explicit examples such as `.env.example`
- private raw field recordings unless explicitly approved
- exact protected-species coordinates in public sample data
- sensitive timestamp/location combinations that create disclosure risk

Prefer:

- synthetic fixtures
- masked sample data
- approved public demo assets
- generated test datasets

---

## 9. Protected Species and Sensitive Observation Data

This project may involve biologically sensitive data.

Be especially careful with:

- exact nest, roost, breeding, or habitat coordinates
- exact timestamps that may expose location patterns
- data exports that bypass masking logic
- screenshots or demo assets that reveal sensitive locations

When in doubt, use masked or synthetic data.

---

## 10. Database and Migration Rule

When changing schema:

- describe the migration intent
- note rollback considerations
- update related DB design docs if needed
- avoid unsafe destructive changes without explicit review
- consider geospatial and time-series query impact
- consider indexing implications
- consider data retention and auditability implications

---

## 11. Testing Rule

When changing behavior, add or update relevant tests where practical.

Examples include:

- API tests
- service tests
- worker tests
- geospatial query validation
- datetime and timezone normalization checks
- masking and access-control checks
- accessibility checks for UI changes

Do not treat manual testing alone as sufficient for critical logic if automated coverage is practical.

---

## 12. Output Expectations for Agent-Assisted Work

Agent-assisted work in this repository should be:

- implementation-oriented
- assumption-aware
- scoped
- reviewable

Minimum expected sections in proposals:

- Summary
- Assumptions
- Proposed Changes
- Acceptance Criteria
- Risks
- Next Steps

For UI work, also follow the required UI-specific headings defined in the design guidance.

---

## 13. Reporting Ambiguity

When requirements are ambiguous:

- state assumptions clearly
- do not hide interpretation changes
- propose concrete acceptance criteria
- identify the smallest safe next step

Avoid silently expanding scope.

---

## 14. Code Style and Repository Hygiene

Please aim to:

- keep modules cohesive
- avoid unnecessary dependencies
- keep naming consistent with existing repository conventions
- avoid dead files and abandoned scaffolding
- keep public-facing files clean and understandable
- prefer explicitness over cleverness in critical logic

---

## 15. Contributor Conduct

Please keep collaboration professional, respectful, and technically constructive.

Good contributions are:

- precise
- transparent
- testable
- documented
- easy to review

---

## 16. Questions

If something is unclear:

- open an issue
- document assumptions in your pull request
- ask for review before making broad structural changes

Thank you for helping build EcoAudio Mapper carefully and responsibly.