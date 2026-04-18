# UI Design Policy
Apple Human Interface Guidelines × NeXTSTEP / OPENSTEP / GNUstep Inspired Visual System

## 1. Purpose
This document defines the mandatory UI design policy for this product.

All agents, designers, and developers must follow this document whenever proposing, generating, reviewing, or implementing UI.

This policy exists to ensure that:
- usability remains consistent with Apple platform expectations
- accessibility is preserved
- the product maintains a disciplined and coherent visual identity
- NeXTSTEP / OPENSTEP / GNUstep inspiration is reflected in a modern and practical way
- design decisions do not drift toward generic SaaS, overly playful consumer styling, or retro imitation

---

## 2. Primary Rule
Use Apple Human Interface Guidelines as the primary authority for:
- interaction design
- information architecture
- navigation
- control behavior
- accessibility
- readability
- platform conventions
- system-native UI expectations
- layout clarity
- feedback and error presentation

Use NeXTSTEP / OPENSTEP / GNUstep only as the visual, structural, and atmospheric inspiration for:
- workspace composition
- pane organization
- inspector-oriented workflows
- tool-focused desktop layout
- professional tone
- grayscale-driven restraint
- workstation-like seriousness
- disciplined visual hierarchy

---

## 3. Priority Rule
If there is any conflict between:
- Apple Human Interface Guidelines
and
- NeXTSTEP / OPENSTEP / GNUstep visual nostalgia or legacy conventions

then Apple Human Interface Guidelines must always take priority.

This rule is absolute.

In practical terms:
- behavior = Apple
- usability = Apple
- accessibility = Apple
- platform fit = Apple
- visual spirit = NeXT / OPENSTEP / GNUstep

Do not sacrifice usability, accessibility, or platform consistency for retro appearance.

---

## 4. Interpretation Rule
Do not reproduce a historical UI literally.

This project does NOT seek:
- a nostalgic replica
- a museum-like recreation
- obsolete visual details copied without reason
- old UI behavior that conflicts with modern expectations

Instead, reinterpret NeXT-like design principles for a modern Apple-native application.

The target outcome is:

> a modern Apple-compliant application with the compositional discipline and atmosphere of NeXTSTEP / OPENSTEP / GNUstep

---

## 5. Desired Product Character
The UI should feel:
- calm
- precise
- technical
- professional
- structured
- minimal
- intentional
- quietly elegant
- engineered
- timeless

It should support prolonged use and serious work.

It should not feel:
- flashy
- toy-like
- trendy for its own sake
- overly soft
- cluttered
- ornamental
- nostalgic in a theatrical way

---

## 6. Visual Direction
### 6.1 General Principles
Prefer:
- restrained composition
- clear grouping
- pane-based structure
- disciplined alignment
- subtle hierarchy
- compact but comfortable density
- low-noise presentation
- functional over decorative decisions

Avoid:
- excessive decoration
- attention-seeking visual effects
- ornamental textures
- over-designed empty space
- heavy card-based layouts on desktop
- overly playful or bubbly styling

### 6.2 Color Policy
Use:
- grayscale or restrained neutral tones as the base
- one controlled accent color
- semantic color only where meaning is needed
- color for focus, selection, status, warning, and destructive actions

Do not:
- use many competing accent colors
- oversaturate the interface
- rely on color alone to communicate meaning
- create rainbow-style visual noise

### 6.3 Depth and Materials
Use depth sparingly and purposefully.

Prefer:
- subtle separators
- light hierarchy cues
- restrained material layering
- depth only when it improves comprehension

Avoid:
- dramatic shadows
- excessive translucency
- gratuitous glass effects
- decorative layering that reduces clarity

---

## 7. Layout Direction
### 7.1 Preferred Screen Composition
Prefer a workstation-style desktop layout when appropriate:
- left sidebar: navigation, hierarchy, object tree, or source list
- center pane: main workspace or primary content
- right pane: inspector, detail editor, properties, metadata, or contextual controls
- top toolbar: essential actions only
- bottom status area: only if it materially improves situational awareness

### 7.2 Layout Priorities
Layouts should optimize for:
- task clarity
- scanning efficiency
- predictable grouping
- editability
- operational precision
- reduced cognitive overhead

### 7.3 Spacing
Spacing should be:
- consistent
- intentional
- readable
- efficient on desktop

Do not create excessive whitespace that lowers information throughput.
Do not compress the UI until it becomes visually stressful.

The target is:
- compact but comfortable
- efficient but not cramped

---

## 8. Components
### 8.1 Native Controls First
Use standard Apple platform controls and patterns whenever possible.

Do not invent custom controls when native controls already satisfy the need.

Custom controls are allowed only when:
- they materially improve task performance
- native controls cannot represent the interaction clearly
- accessibility and consistency are preserved

### 8.2 Expected Feel of Components
Buttons, lists, tables, forms, sidebars, toolbars, inspectors, menus, dialogs, and settings should feel:
- modern
- native
- clear
- compact
- professional
- utility-oriented

They should not feel:
- decorative
- oversized
- playful
- arbitrary
- visually loud

### 8.3 Tables and Lists
For information-heavy workflows:
- prefer clear tables and structured lists
- support efficient scanning
- preserve alignment
- expose sorting, filtering, and selection states clearly

### 8.4 Inspectors
Inspector panels should be:
- concise
- structured
- contextual
- subordinate to the main task
- clearly separated from the main workspace

---

## 9. Typography
Use Apple-appropriate typography conventions.

Prefer:
- clean system typography
- hierarchy through size, weight, spacing, and placement
- readable labels
- concise copy
- consistent terminology

Avoid:
- retro imitation fonts
- decorative typography
- excessive font variation
- ornamental text styling

Typography should support:
- fast scanning
- long-session readability
- dense desktop workflows
- semantic clarity

---

## 10. Interaction Principles
### 10.1 Interaction Model
All interactions must feel Apple-native in behavior.

This includes:
- navigation
- selection
- search
- dialog presentation
- sheets
- context menus
- settings organization
- keyboard support
- focus handling
- state changes
- destructive action confirmation
- feedback and recovery

### 10.2 Productivity Orientation
Optimize for:
- prolonged desktop use
- keyboard efficiency
- repeatable workflows
- precise manipulation
- low-friction editing
- discoverable but disciplined controls

### 10.3 Error Handling
Errors, warnings, and confirmations should:
- be concise
- be actionable
- use clear semantics
- avoid alarmist tone
- follow platform expectations

---

## 11. Accessibility
Accessibility is mandatory, not optional.

All designs must:
- preserve sufficient contrast
- avoid relying on color alone
- provide clear focus states
- maintain readable text sizes
- use meaningful labels
- support assistive interpretation where applicable
- maintain clear hit targets
- keep interaction states understandable

Any design that improves appearance but weakens accessibility must be rejected.

---

## 12. Anti-Patterns
The following outcomes are not acceptable:
- retro imitation for its own sake
- literal reproduction of legacy UI details
- generic modern SaaS card grids used without justification
- excessive rounded corners everywhere
- visually loud gradients
- glossy or ornamental effects without purpose
- oversized empty spacing on desktop
- mobile-style sparse layouts applied blindly to desktop
- custom controls replacing standard controls without strong reason
- style decisions that reduce scanning efficiency
- decorative complexity that weakens operational clarity

---

## 13. Mandatory Output Format for Agents
Whenever proposing, generating, or revising a screen, component, or workflow, the agent must provide the following sections:

1. Purpose  
2. Apple HIG Basis  
3. NeXT / OPENSTEP / GNUstep Influence  
4. Layout Description  
5. Interaction Behavior  
6. Visual Styling Notes  
7. Accessibility Notes  
8. Implementation Considerations  

The agent must not provide only vague aesthetic impressions.
The output must be implementation-oriented.

---

## 14. Mandatory Self-Check Before Finalizing Any UI Proposal
Before finalizing any proposal, the agent must explicitly verify:

- Does this preserve Apple usability conventions?
- Does this preserve accessibility?
- Does this avoid retro imitation?
- Does this reflect NeXT-like structure through composition rather than obsolete behavior?
- Is the layout efficient for desktop work?
- Is the interface visually restrained?
- Are native patterns used where possible?
- Is the design coherent with the rest of the product?

If any answer is “no”, revise before finalizing.

---

## 15. Platform Assumption
Unless explicitly stated otherwise, assume:
- primary target = desktop productivity application
- prolonged usage is expected
- keyboard usage matters
- information density matters
- precision matters
- inspector/pane-based workflows are preferred when appropriate

Do not default to mobile-first visual decisions for desktop UI.

---

## 16. Relationship to Apple Human Interface Guidelines
The official Apple Human Interface Guidelines provided in this repository remain the source of truth for platform behavior and usability interpretation.

This document does not replace Apple HIG.
This document defines how to combine Apple HIG with the intended visual and compositional character of this product.
