# UX Design Deliverable — {topic}

> Fill the section that matches the routed topic; delete the others. Tag every
> non-obvious claim `[EXPLICIT]` / `[INFERENCIA]` / `[SUPUESTO]`.

## Header

- **Topic (route):** {one of the 18 enum values}
- **Depth:** {quick | deep}
- **Artifact:** {screen / component / copy / flow / token set}
- **User goal:** {primary task the user is trying to complete}
- **Audience / device / context:** {who, what device, where}
- **Success metric:** {how success is measured}

---

## A. Critique deliverable (design-critique / design-review)

**Strengths worth keeping**
- {at least one concrete strength}

**Issues — ordered by severity (not reading order)**

| # | Location | Heuristic | Observation → Impact → Suggestion | Severity |
|---|----------|-----------|-----------------------------------|----------|
| 1 | {where} | {Nielsen heuristic} | {neutral what} → {cost to user/task} → {one direction} | Blocker / Major / Minor / Nit |

> Heuristic Blockers stay `[SUPUESTO]` until confirmed by usability testing/analytics.

---

## B. Design-system deliverable (design-system / typography / iconography)

**Brand tokens (`:root`)** — sourced from `brand-config.json`, no hex literals elsewhere.

| Token | Value | Usage |
|-------|-------|-------|
| `--brand-primary` | {hex} | accents, borders, active |

**Semantic tokens** — universal; success = `#FFD700` (yellow, not green).

| Token | Value | Text color | Usage |
|-------|-------|-----------|-------|
| `--semantic-positive` | #FFD700 | black | success |

**Accessibility check** — WCAG AA pairs verified: {list contrast ratios}.

---

## C. Component deliverable (component-designer / form / table / search / notification / empty-state / error-messaging)

- **Atomic level:** {atom | molecule | organism}
- **Props contract**

| Prop | Type | Required | Default | Notes |
|------|------|----------|---------|-------|
| {name} | {type} | {y/n} | {default} | {a11y / behavior} |

- **States:** {default, hover, focus, active, disabled, loading, error, empty}
- **Copy (if applicable):** {microcopy / error text — clear, blameless, actionable}
- **Accessibility:** {keyboard path, focus order, ARIA, contrast}

---

## D. Interaction / flow deliverable (motion / micro-interactions / onboarding / mobile / dashboard)

- **Trigger → response:** {what fires, what the user sees}
- **Timing / easing:** {duration, curve} ; respects `prefers-reduced-motion`.
- **Steps / layout:** {flow steps or layout regions}

---

## Validation gate (must pass)

- [ ] Exactly one playbook Read for this deliverable
- [ ] Output matches that playbook's shape
- [ ] Every non-obvious claim carries an evidence tag
- [ ] Success = yellow `#FFD700`, never green; no hex literals outside `:root`
- [ ] WCAG AA contrast met (4.5:1 body, 3:1 large)
- [ ] No unresolved `{VACIO_CRITICO}`; no invented metrics or prices; single brand
