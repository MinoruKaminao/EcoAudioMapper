# Multi-Agent Prompt Structure for EcoAudio Mapper

## 1. Goal
This document defines how to structure prompts for multiple agents working in the same public GitHub repository.

The design goal is:
- consistent outputs
- low drift between agents
- strong UI consistency
- safe public-repo behavior
- implementation-ready results

---

## 2. Directory Structure

```text
docs/
  design/
    ui-design-policy.md
    ui-review-checklist.md
    apple-hig-short.md
    agent-instructions.md

  agents/
    common/
      project-context.md
      repository-rules.md
      output-contract.md
    roles/
      product-agent.md
      architecture-agent.md
      backend-agent.md
      database-agent.md
      ml-audio-agent.md
      gis-analytics-agent.md
      ui-ux-agent.md
      qa-agent.md
      documentation-agent.md
      security-privacy-agent.md

  requirements/
  plan/
  design/
  test/
  operation/
```

---

## 3. Common Prompt Layers

Every agent prompt should be assembled from four layers.

### Layer 1: Project Context
Contains:
- mission
- domain scope
- public GitHub constraints
- system overview
- current architecture summary
- protected data handling principles

### Layer 2: Repository Rules
Contains:
- coding rules
- documentation rules
- branch / PR expectations
- test expectations
- security / privacy restrictions
- sample data rules

### Layer 3: Design Rules
Contains:
- Apple HIG short standard
- UI design policy
- UI review checklist
- agent instructions for UI work

### Layer 4: Role Prompt
Contains:
- role responsibilities
- expected artifacts
- constraints
- decision priorities
- required output format

---

## 4. Standard Agent Prompt Template

Use this template for each role file.

```md
# <Role Name>

## Role
Describe the agent's responsibility in one paragraph.

## Objectives
- objective 1
- objective 2
- objective 3

## Inputs
- project context
- repository rules
- design references
- issue text / task brief
- existing related docs and code

## Required Process
1. restate task and assumptions
2. identify impacted files/modules/screens
3. propose or implement changes
4. define acceptance criteria or validation
5. identify risks and follow-up items

## Output Requirements
- concrete
- implementation-oriented
- structured
- aligned with repository conventions

## Mandatory Sections
- Summary
- Assumptions
- Proposed Changes
- Acceptance Criteria
- Risks
- Next Steps
```

---

## 5. UI-Specific Prompt Contract

All UI-related role prompts must add the following mandatory headings:

- Purpose
- Apple HIG Basis
- NeXT / OPENSTEP / GNUstep Influence
- Layout Description
- Interaction Behavior
- Visual Styling Notes
- Accessibility Notes
- Implementation Considerations
- Self-Check Result

This ensures consistent output across design, frontend, review, and documentation agents.

---

## 6. Role Prompt Summaries

## 6.1 Product Agent
Focus:
- requirement refinement
- feature boundaries
- acceptance criteria
- release slicing

Success criteria:
- clear user-facing scope
- unambiguous functional definition
- traceable acceptance conditions

## 6.2 Architecture Agent
Focus:
- system decomposition
- API and async boundaries
- operational constraints
- deployment fit

Success criteria:
- clear boundaries
- scalable pipeline decisions
- documented tradeoffs

## 6.3 Backend Agent
Focus:
- domain services
- API behavior
- validation
- authz/authn
- background jobs

Success criteria:
- stable contracts
- testable logic
- migration-aware changes

## 6.4 Database Agent
Focus:
- relational design
- PostGIS strategy
- indexing
- masking data model
- auditability

Success criteria:
- queryable schema
- safe migrations
- analytical support

## 6.5 ML / Audio Agent
Focus:
- preprocessing
- segmentation
- inference orchestration
- reproducibility
- evaluation

Success criteria:
- versioned pipeline
- measurable performance
- documented assumptions

## 6.6 GIS / Analytics Agent
Focus:
- spatial filtering
- clustering
- heatmaps
- time aggregation
- export support

Success criteria:
- efficient geo queries
- correct time-zone-aware aggregation
- map-ready outputs

## 6.7 UI / UX Agent
Focus:
- desktop information architecture
- pane layout
- inspector patterns
- HIG compliance
- accessibility

Success criteria:
- OpenStep-inspired composition
- Apple-native behavior
- production-ready screen specs

## 6.8 QA Agent
Focus:
- functional validation
- regression safety
- accessibility verification
- performance smoke tests

Success criteria:
- release confidence
- reproducible checks
- issue isolation

## 6.9 Documentation Agent
Focus:
- README
- setup docs
- architecture docs
- developer workflows
- contributor guidance

Success criteria:
- easy onboarding
- low ambiguity
- docs aligned with implementation

## 6.10 Security / Privacy Agent
Focus:
- public repo hygiene
- secret prevention
- masking policy
- protected-species disclosure controls

Success criteria:
- lower exposure risk
- explicit mitigation guidance
- secure defaults

---

## 7. Example Common Prompt Files

## 7.1 `docs/agents/common/project-context.md`
Recommended sections:
- project summary
- user groups
- core workflows
- architecture snapshot
- data sensitivity notes
- current milestone

## 7.2 `docs/agents/common/repository-rules.md`
Recommended sections:
- public repo rules
- commit and PR expectations
- no secrets rule
- raw data restrictions
- docs sync rule
- testing rule

## 7.3 `docs/agents/common/output-contract.md`
Recommended sections:
- always be concrete
- expose assumptions
- mention impacted files
- define acceptance criteria
- avoid vague style commentary
- keep outputs reviewable

---

## 8. OpenStep-Inspired UI Spec Rule

When any agent discusses UI, the output must follow these principles:
- Apple HIG first
- OpenStep influence through composition, not imitation
- desktop-first productivity layout when appropriate
- sidebar + main workspace + inspector structure
- restrained neutral palette
- minimal decoration
- strong hierarchy
- discoverable controls
- accessibility preserved

---

## 9. GitHub Public Development Rule

Because the repository is public, all prompts should remind agents:
- do not include secrets
- do not commit production endpoints with credentials
- do not publish protected species exact coordinates in sample datasets
- do not commit raw private media unless approved
- prefer generated sample data for tests and demos

---

## 10. Recommended Initial Files to Commit

```text
.gitignore
AGENTS.md
README.md
docs/design/ui-design-policy.md
docs/design/ui-review-checklist.md
docs/design/apple-hig-short.md
docs/design/agent-instructions.md
docs/agents/common/project-context.md
docs/agents/common/repository-rules.md
docs/agents/common/output-contract.md
docs/agents/roles/ui-ux-agent.md
docs/agents/roles/backend-agent.md
docs/agents/roles/database-agent.md
docs/agents/roles/ml-audio-agent.md
docs/agents/roles/gis-analytics-agent.md
```

---

## 11. Recommended UI Spec Statement

Use this statement in repository-level prompts:

> This product must behave like a modern Apple-native application while expressing the structural discipline and professional atmosphere of NeXTSTEP / OPENSTEP / GNUstep. Preserve Apple usability and accessibility first. Express the OpenStep influence through pane composition, toolbar discipline, inspector workflows, restrained neutral styling, and desktop productivity density. Do not create a retro replica.

---

## 12. Final Recommendation

For this project, keep:
- one repository-wide `AGENTS.md`
- one shared design policy stack under `docs/design/`
- separate role prompts under `docs/agents/roles/`
- task briefs under `docs/plan/`

This gives multiple agents a stable shared base while allowing role specialization.
