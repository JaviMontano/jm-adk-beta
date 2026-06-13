# Body of Knowledge — ux-design

Domain knowledge for the ux-design router. Grounds routing decisions and the
substantive UX judgment inside each playbook. Tags follow the Alfa core set:
`[EXPLICIT]` `[INFERENCIA]` `[SUPUESTO]`.

## 1. Router model

This skill is a router, not a monolith. A request maps to exactly one of 18
topics; the matching `references/*.md` playbook is the source of truth, and the
whole cluster is never loaded at once. [EXPLICIT] The 18 topics cluster into five
families:

- **Foundations** — design-system, typography-advanced, iconography.
- **Components** — component-designer, form-ux-advanced, table-ux, search-ux,
  notification-ux, empty-states, error-messaging.
- **Layout** — dashboard-design, mobile-patterns.
- **Interaction** — motion-design, micro-interactions.
- **Flow & copy** — onboarding-ux, first-use-onboarding, microcopy-writing,
  design-critique. [INFERENCIA]

## 2. Key concepts and standards

### Heuristic evaluation
Nielsen's 10 usability heuristics drive critique: visibility of system status,
match to real world, user control/undo, consistency/standards, error prevention,
recognition over recall, flexibility/efficiency, minimalist aesthetic, error
recovery, help/documentation. Findings record location, heuristic violated, and
user consequence. [EXPLICIT]

### Severity rubric
Critiques force prioritization with four levels: **Blocker** (task fails),
**Major** (task succeeds but costly/confusing), **Minor** (polish), **Nit**
(preference, optional). Severities are calibrated against each other, not
inflated; bikeshedding (piling Nits while a Blocker hides) is the classic failure.
[EXPLICIT]

### Feedback framing
Every critique item is framed observation (neutral what) → impact (cost to
user/task) → suggestion (one concrete direction). Critique the artifact, never
the author — person-directed phrasing triggers defensiveness. Lead with at least
one strength worth keeping. [EXPLICIT]

### Design tokens
Brand identity lives in `brand-config.json`; templates reference
`var(--brand-primary)`, never a hex literal. Eight brand tokens + ten semantic +
five chart tokens live in `:root`; missing `primary_light`/`primary_dark` are
derived (+/-12% L in HSL) deterministically so the same config yields identical
output. [EXPLICIT]

### Atomic design
Components compose as atoms → molecules → organisms, with explicit props
contracts, composition over configuration, and accessibility built into the
primitive (not bolted on). [EXPLICIT]

### Accessibility baseline
WCAG AA: 4.5:1 contrast for body text, 3:1 for large text; visible focus
(`focus-visible` 2px outline); semantic HTML (header/nav/main/section/footer);
skip-to-content link; alt text on images; keyboard reachability for every
interactive element. [EXPLICIT]

## 3. Decision rules

- **Component vs system**: a reusable UI block → component-designer; tokens/scale/
  foundations → design-system. [EXPLICIT]
- **Error copy vs other copy**: failure/validation copy → error-messaging;
  everything else → microcopy-writing. [EXPLICIT]
- **Onboarding split**: generic new-user flow → onboarding-ux; post-clone/cold-start
  JM-ADK context → first-use-onboarding. [EXPLICIT]
- **Tabular families**: data grid → table-ux; metric layout → dashboard-design;
  query/filter → search-ux. [EXPLICIT]
- **Interaction split**: animation/transition timing → motion-design; feedback on a
  single interaction (hover, tap, toggle) → micro-interactions. [INFERENCIA]
- **Success is yellow, not green**: `#FFD700` distinguishes success from decorative
  green data series and survives red-green color blindness; it requires black text
  for AA. [EXPLICIT]
- **No goal, no critique**: without a stated user goal every critique is opinion —
  request the goal before proceeding. [EXPLICIT]

## 4. Limits

- Heuristic evaluation surfaces *likely* issues, not measured ones — confirm
  Blockers with usability testing or analytics before treating them as proven.
  [SUPUESTO]
- Out of scope: brand/visual identity, frontend code generation, product strategy —
  sibling skills own those. [INFERENCIA]
- Critique informs the owner's decision; it does not approve or block ship. [SUPUESTO]
