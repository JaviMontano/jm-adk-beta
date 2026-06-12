---
name: accessibility
version: 1.0.0
description: "Accessibility router: WCAG audit, testing, accessible design, inclusive writing. Routes topic→playbook. Topics: audit, design, testing, writing."
params:
  topic:
    enum: [audit, design, testing, writing]
    required: true
    infer: from user request; ask only if ambiguous
  depth:
    enum: [quick, deep]
    default: quick
routes:
  audit: references/audit.md
  design: references/design.md
  testing: references/testing.md
  writing: references/writing.md
---

# accessibility

Router skill. Resolve `topic`, then Read EXACTLY ONE playbook from `routes:`.
Never load the whole cluster — loading two playbooks is the primary anti-pattern. [DOC]

## When to use
Any WCAG / a11y request: contrast and color, keyboard and focus, screen-reader
and ARIA, alt text, captions, plain-language copy, or compliance evidence. [DOC]

## Topic routing (pick one) [DOC]
- `audit` → assess an existing artifact against WCAG 2.1 AA; produce a gap list.
- `design` → bake a11y into components/tokens/layout *before* build.
- `testing` → automated (axe-core) + manual keyboard/SR verification in CI.
- `writing` → alt text, link text, headings, plain-language microcopy.
Overlap: pre-build → `design`; post-build verification → `testing`; one-time
scorecard → `audit`. If the request spans two, run them in sequence, not merged. [INFERENCIA]

## Depth
- `quick` (default) → essentials, the highest-impact WCAG criteria only.
- `deep` → apply the playbook exhaustively with verification at each step.

## Inputs / Outputs
- In: target artifact (URL, component, copy, repo path) + `topic` + `depth`. [DOC]
- Out: findings with WCAG success-criterion refs + remediation, each tagged. [DOC]
- Missing target → ask once; do not audit a hypothetical. [INFERENCIA]

## Validation gate (done means) [DOC]
- Exactly one playbook loaded; `topic` matches user intent.
- Every finding cites a WCAG criterion (e.g. 1.4.3) and a concrete fix.
- Claims carry an Alfa-core tag ([CODE]/[CONFIG]/[DOC]/[INFERENCIA]/[SUPUESTO]);
  pass/fail is evidenced, never asserted green-as-success.

Spine: Discover → Analyze → Execute → Validate.
Gates: constitution v6.0.0 (enforcement), evidence tags, script-first rule. [CONFIG]
Gate against `assets/checklist.md` and score with `assets/quality-rubric.json`
before declaring done; see the DoD bundle in `assets/`. [DOC]