---
name: ux-design
version: 1.0.0
description: "UI/UX design patterns: design systems, interaction and motion, onboarding, microcopy, and component-level UX (forms, tables, search, notifications). Topics: component-designer, dashboard-design, design-critique, design-system, empty-states, error-messaging, first-use-onboarding, form-ux-advanced, iconography, micro-interactions, microcopy-writing, mobile-patterns, motion-design, notification-ux, onboarding-ux, search-ux, table-ux, typography-advanced."
params:
  topic:
    enum: [component-designer, dashboard-design, design-critique, design-system, empty-states, error-messaging, first-use-onboarding, form-ux-advanced, iconography, micro-interactions, microcopy-writing, mobile-patterns, motion-design, notification-ux, onboarding-ux, search-ux, table-ux, typography-advanced]
    required: true
    infer: from user request; ask only if ambiguous
  depth:
    enum: [quick, deep]
    default: quick
routes:
  component-designer: references/component-designer.md
  dashboard-design: references/dashboard-design.md
  design-critique: references/design-critique.md
  design-system: references/design-system.md
  empty-states: references/empty-states.md
  error-messaging: references/error-messaging.md
  first-use-onboarding: references/first-use-onboarding.md
  form-ux-advanced: references/form-ux-advanced.md
  iconography: references/iconography.md
  micro-interactions: references/micro-interactions.md
  microcopy-writing: references/microcopy-writing.md
  mobile-patterns: references/mobile-patterns.md
  motion-design: references/motion-design.md
  notification-ux: references/notification-ux.md
  onboarding-ux: references/onboarding-ux.md
  search-ux: references/search-ux.md
  table-ux: references/table-ux.md
  typography-advanced: references/typography-advanced.md
---

# ux-design

Router skill. Resolve `topic` from the request, Read EXACTLY ONE playbook from
`routes:`, then execute it. Never load the whole cluster. [EXPLICIT]

## When to use

UI/UX design work: design systems, components, interaction/motion, onboarding,
microcopy, and component-level UX (forms, tables, search, notifications). Not
for brand/visual identity, frontend code-gen, or product strategy — sibling
skills, not here. [INFERENCIA]

**In**: the request (resolves `topic`); optional artifact to critique/improve
(screen, component, copy, flow); `depth`. **Out**: the playbook's deliverable
(audit, spec, pattern, or copy), evidence-tagged. [INFERENCIA]

## Routing — resolve `topic`

Map the request to exactly one enum (infer silently; ask only if two fit
equally), Read its `routes:` playbook — one file, nothing else — then:
`depth=deep` → apply exhaustively, verify each step; `quick` → essentials.
Spine: Discover → Analyze → Execute → Validate. [EXPLICIT]

Disambiguation (common collisions): [INFERENCIA]
- Reusable UI block → `component-designer`; tokens/scale/foundations → `design-system`.
- Error copy → `error-messaging`; copy elsewhere → `microcopy-writing`.
- New-user flow → `onboarding-ux`; post-clone/cold-start JM-ADK → `first-use-onboarding`.
- "No data yet" → `empty-states`; "review my design" → `design-critique`.
- Animation/transition → `motion-design`; interaction feedback → `micro-interactions`.
- Data grid → `table-ux`; metric layout → `dashboard-design`; query/filter → `search-ux`.

## Validation gate (acceptance criteria)

Done only when: exactly one playbook was Read; output follows that playbook's
shape; every non-obvious claim carries a verification tag (Alfa core set); no
`{VACIO_CRITICO}` unresolved. [EXPLICIT] Quality gates: constitution v6.0.0
(enforcement), evidence tags, script-first rule. [CONFIG] Run-time machinery in
`assets/` — `assets/routing-checklist.md` (routing gate) and
`assets/quality-rubric.json` (guardian scoring). [CONFIG]

## Anti-patterns

- Reading 2+ playbooks or skimming the cluster "for context". [EXPLICIT]
- Answering from general UX knowledge instead of the routed playbook. [INFERENCIA]
- Guessing `topic` when ambiguous — ask one crisp question. [INFERENCIA]
- Green-as-success or invented metrics in critiques. [EXPLICIT]

**Self-correct**: routed playbook doesn't fit → re-resolve `topic` once, never
force-fit. No enum fits → say so, propose the nearest sibling skill; never
fabricate a route. [INFERENCIA]