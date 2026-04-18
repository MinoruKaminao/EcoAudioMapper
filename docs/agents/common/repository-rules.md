# Repository Rules

## Public Repository Rules
- This repository is public.
- Never commit secrets, tokens, credentials, certificates, or private keys.
- Never commit `.env` files except explicit examples like `.env.example`.
- Never commit raw private field media unless publication is explicitly approved.
- Do not commit exact protected-species sample coordinates unless they are masked or synthetic.

## Documentation Rules
- Keep docs aligned with behavior.
- Update relevant docs when public-facing behavior or architecture changes.
- Prefer English filenames for stable repository structure.
- Keep long-form design guidance under `docs/design/`.
- Keep role prompts under `docs/agents/roles/`.

## Code Change Rules
- Prefer small, reviewable changes.
- Add tests when changing behavior.
- Avoid silent breaking renames.
- State assumptions when requirements are ambiguous.
- Preserve migration safety when changing schema.

## Data Rules
- Use synthetic, masked, or approved demo data in tests and examples.
- Separate raw data, derived artifacts, exports, and checked-in fixtures.
- Never assume field media is safe to publish.

## UI Rules
- Use Apple HIG as the source of truth for behavior, navigation, accessibility, and control expectations.
- Use NeXT / OPENSTEP / GNUstep only as inspiration for composition and visual discipline.
- Do not create retro replicas.
- Do not default to generic SaaS card layouts for desktop-heavy workflows.

## Review Rules
Before finalizing major work, verify:
- public-repo safety
- privacy and masking implications
- documentation impact
- migration impact if schema changed
- accessibility impact if UI changed

## Pull Request Expectations
- explain intent
- list impacted areas
- mention tests or validation
- mention docs updated
- note privacy/security implications when relevant
