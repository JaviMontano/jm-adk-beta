---
name: ux-design
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

Router skill. Resolve `topic` from the request, then Read EXACTLY ONE playbook
from `routes:`. Never load the whole cluster. `depth=deep` → apply the playbook
exhaustively with verification at each step; `quick` → essentials only.

Spine: Discover → Analyze → Execute → Validate.
Quality gates: constitution v6.0.0 (enforcement), evidence tags, script-first rule.
