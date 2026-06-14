# accessibility — Skill Overview

Router skill for WCAG 2.1 AA accessibility work. It resolves a `topic` and loads
**exactly one** playbook, then runs that playbook's Discover → Analyze → Execute →
Validate spine. Loading two playbooks at once is the primary anti-pattern. [DOC]

## What it does
Turns any a11y request into evidence-backed output: a gap audit, an accessible
design spec, a test plan with pass/fail evidence, or accessible copy — each with
WCAG success-criterion references and Alfa-core evidence tags. [DOC]

## When to use
Any request touching contrast/color, keyboard/focus, screen-reader/ARIA, alt text,
captions, plain-language microcopy, or WCAG compliance evidence. If the deliverable
is *not* accessibility, route elsewhere. [DOC]

## How it routes (pick one)
| topic | Playbook | Use when the deliverable is |
|-------|----------|------------------------------|
| `audit` | `references/audit.md` | A WCAG gap scorecard on existing UI (axe-core + manual). |
| `design` | `references/design.md` | An accessible component/token/keyboard spec *before* build. |
| `testing` | `references/testing.md` | A test plan / regression suite producing pass-fail evidence. |
| `writing` | `references/writing.md` | Alt text, link text, error copy, plain-language rewrites. |

Overlap rule: pre-build → `design`; post-build verification → `testing`; one-time
scorecard → `audit`. A request spanning two topics runs them in sequence, never
merged. [INFERENCIA]

## How it executes
1. Resolve `topic` (infer from request; ask only if ambiguous) and `depth`
   (`quick` default / `deep`).
2. Read the single matching playbook from `routes.json`.
3. Run the playbook; emit findings that each cite a WCAG criterion (e.g. 1.4.3),
   a concrete fix, and exactly one evidence tag.
4. Gate the deliverable against the playbook's Quality Criteria before "done".

## References
- `references/audit.md` — WCAG 2.1 AA audit (automated-first, manual-finality).
- `references/design.md` — native-first accessible design, keyboard contracts.
- `references/testing.md` — evidence-producing test workflow, pass/fail/not-verified.
- `references/writing.md` — alt-text treatment matrix, plain-language, inclusive copy.

## DoD bundle
- `agents/` — lead, specialist, support, guardian role contracts.
- `knowledge/` — body of knowledge + concept knowledge graph.
- `prompts/` — primary, meta, quick, deep prompts.
- `templates/output.md` — deliverable scaffold.
- `evals/evals.json` — scenario suite.
- `examples/` — worked input/output.
- `assets/` — quality rubric and asset manifest.

## Governance
Evidence tags on every claim ([CODE]/[CONFIG]/[DOC]/[INFERENCIA]/[SUPUESTO] or the
playbook's `[EXPLICIT]`/`[INFERENCE]`/`[ASSUMPTION]` family). Never green-as-success:
status is `pass` / `conditional` / `fail` / `not verified`, never asserted. No
invented prices, no client PII, single-brand output. [CONFIG]
