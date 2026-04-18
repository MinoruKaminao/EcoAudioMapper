Contributing to EcoAudio Mapper

Thank you for contributing.

This repository is public and is intended to support disciplined, reviewable development for EcoAudio Mapper.

Basic Principles

* keep changes small and reviewable
* keep documentation aligned with implementation
* preserve public-repository safety
* prefer clarity over novelty
* preserve Apple usability and accessibility for UI work
* express OpenStep influence through structure, not retro imitation

Before You Start

Please read:

* AGENTS.md
* docs/agents/common/project-context.md
* docs/agents/common/repository-rules.md
* docs/agents/common/output-contract.md
* docs/design/ui-design-policy.md
* docs/design/ui-review-checklist.md
* docs/design/apple-hig-short.md
* docs/design/agent-instructions.md

Branching

Recommended:

* create a focused feature branch
* use descriptive names such as:
    * feature/map-filters
    * fix/datetime-normalization
    * docs/ui-spec-update

Commit Guidance

Prefer commits that are:

* focused
* descriptive
* easy to review

Examples:

* Add initial observation API scaffolding
* Define datetime normalization rules
* Refine OpenStep-inspired map workspace layout

Pull Request Expectations

Each pull request should include:

* what changed
* why it changed
* impacted areas
* validation performed
* docs updated or not
* privacy or security implications if relevant

Documentation Rule

If behavior, contracts, workflows, or architecture change, update the related docs in the same change when practical.

UI Contribution Rule

For UI-related proposals and implementations:

* Apple HIG has priority for behavior and usability
* OpenStep influence should appear in composition and atmosphere
* do not create a retro replica
* do not default to generic SaaS card-heavy layouts for desktop workflows
* include accessibility considerations

Data and Privacy Rule

Do not commit:

* secrets
* private keys
* credentials
* private raw field media unless explicitly approved
* exact protected-species coordinates in public sample data
* unmasked sensitive timestamp/location combinations that create disclosure risk

Prefer:

* synthetic fixtures
* masked sample data
* approved public demo assets

Database and Migration Rule

When changing schema:

* describe migration intent
* note rollback considerations
* update related design docs if needed
* avoid unsafe destructive changes without explicit review

Testing Rule

When changing behavior, add or update relevant tests where practical:

* API tests
* service tests
* worker tests
* accessibility checks for UI changes
* validation checks for datetime and geospatial logic

Output Expectations for Agent-Assisted Work

Agent-assisted changes should be:

* implementation-oriented
* assumption-aware
* scoped
* reviewable

Minimum expected sections in proposals:

* Summary
* Assumptions
* Proposed Changes
* Acceptance Criteria
* Risks
* Next Steps

Questions and Issues

When requirements are ambiguous:

* state assumptions clearly
* avoid hidden interpretation changes
* propose concrete acceptance criteria

Thank you for helping build EcoAudio Mapper carefully and responsibly.
EOF

———————––

confirm

———————––

echo “===== generated files =====”
ls -la README.md LICENSE CONTRIBUTING.md
echo
echo “===== README preview =====”
head -40 README.md
echo
echo “===== LICENSE preview =====”
head -20 LICENSE
echo
echo “===== CONTRIBUTING preview =====”
head -40 CONTRIBUTING.md