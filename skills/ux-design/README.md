# ux-design — README

Router skill for UI/UX design work. It resolves a single `topic`, Reads exactly
one playbook from `routes:`, and executes that playbook's procedure. It never
loads the whole cluster. [EXPLICIT]

## What it does

Covers the practical UX surface: design systems and tokens, component
architecture, interaction and motion, onboarding flows, microcopy, and
component-level UX (forms, tables, search, notifications, empty states,
dashboards). Output is the routed playbook's deliverable — an audit, a spec, a
pattern, or copy — every non-obvious claim carrying an Alfa-core evidence tag
(`[EXPLICIT]` `[INFERENCIA]` `[SUPUESTO]`). [INFERENCIA]

## When to use

- "Apply / build a design system", token scale, foundations → `design-system`.
- "Design / spec this reusable component" → `component-designer`.
- "Review / critique this screen" → `design-critique` (Nielsen heuristics + severity).
- Error copy → `error-messaging`; copy elsewhere → `microcopy-writing`.
- New-user flow → `onboarding-ux`; cold-start JM-ADK → `first-use-onboarding`.
- Data grid → `table-ux`; metric layout → `dashboard-design`; query/filter → `search-ux`.
- "No data yet" → `empty-states`; animation/transition → `motion-design`;
  interaction feedback → `micro-interactions`; mobile → `mobile-patterns`;
  type scale → `typography-advanced`; icons → `iconography`; alerts → `notification-ux`;
  forms → `form-ux-advanced`.

Not for brand/visual identity, frontend code-gen, or product strategy — those
are sibling skills, not this one. [INFERENCIA]

## How it routes and executes

1. Resolve `topic` from the request (infer silently; ask only on a true tie).
2. Read the one file named in `routes:` for that topic — nothing else.
3. Walk the spine: Discover → Analyze → Execute → Validate. `depth=deep` applies
   the playbook exhaustively and verifies each step; `quick` does essentials.
4. Stop at the validation gate: exactly one playbook Read, output matches its
   shape, evidence tags present, no `{VACIO_CRITICO}` left unresolved.

## References

All playbooks live in `references/` and are listed in `SKILL.md` `routes:` and
`routes.json`. Key entries:

- `references/design-system.md` — tokens, semantic colors (success = yellow #FFD700, not green), components, WCAG AA gate.
- `references/design-critique.md` — heuristic evaluation, severity rubric (Blocker/Major/Minor/Nit), observation→impact→suggestion framing.
- `references/component-designer.md` — atomic design, props contracts, composition, accessibility built in.
- `references/form-ux-advanced.md`, `references/table-ux.md`, `references/search-ux.md`,
  `references/notification-ux.md`, `references/empty-states.md`, `references/error-messaging.md`.
- `references/motion-design.md`, `references/micro-interactions.md`, `references/mobile-patterns.md`,
  `references/typography-advanced.md`, `references/iconography.md`, `references/dashboard-design.md`.
- `references/onboarding-ux.md`, `references/first-use-onboarding.md`, `references/microcopy-writing.md`.

## Companion bundle

- `agents/` — lead, specialist, support, guardian role contracts for this skill.
- `knowledge/` — body of knowledge + concept graph for UX foundations.
- `prompts/` — primary, meta, and quick/deep variations.
- `templates/output.md` — deliverable scaffold (audit / spec / pattern / copy).
- `evals/evals.json` — scenario suite with expected checks.
- `examples/` — one worked design-critique example, input and output.
- `assets/` — quality rubric + routing checklist consumed by the gate (see `assets/README.md`).
