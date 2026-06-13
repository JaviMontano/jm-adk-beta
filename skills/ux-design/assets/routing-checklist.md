# Routing Checklist — ux-design

Run top to bottom before producing any deliverable. Stop at the first failing gate.

## 1. Resolve topic

- [ ] Mapped the request to exactly one of the 18 enum values.
- [ ] Applied disambiguations where collisions exist:
  - reusable UI block → `component-designer`; tokens/foundations → `design-system`
  - error copy → `error-messaging`; other copy → `microcopy-writing`
  - new-user flow → `onboarding-ux`; cold-start JM-ADK → `first-use-onboarding`
  - data grid → `table-ux`; metric layout → `dashboard-design`; query/filter → `search-ux`
  - animation/transition → `motion-design`; single-interaction feedback → `micro-interactions`
- [ ] Asked one crisp question ONLY if two topics fit equally.
- [ ] If no enum fits: named the gap, proposed the nearest sibling skill, did not fabricate a route.

## 2. Load exactly one playbook

- [ ] Read the single `routes:` file for the resolved topic.
- [ ] Did NOT read a second reference "for context".

## 3. Discover before executing

- [ ] Captured user goal, primary task, audience, device/context, success metric.
- [ ] For `design-critique`: confirmed a stated user goal exists; if absent, requested it before proceeding.

## 4. Execute + tag

- [ ] Produced the deliverable in the playbook's shape (used `templates/output.md`).
- [ ] Tagged every non-obvious claim `[EXPLICIT]` / `[INFERENCIA]` / `[SUPUESTO]`.

## 5. Deterministic checks (where artifact is concrete)

- [ ] grep `#[0-9A-Fa-f]{3,8}` → no hex literals outside `:root`.
- [ ] Success state uses `#FFD700` (yellow), never green.
- [ ] Black text on light tints (positive / warning / low); WCAG AA contrast verified.

## 6. Gate

- [ ] One playbook Read · shape matches · tags present · no `{VACIO_CRITICO}` · single brand · no invented metrics.
