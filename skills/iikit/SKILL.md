---
name: iikit
version: 1.0.0
description: "Intent Integrity Kit: spec-driven development pipeline (constitution->specify->plan->checklist->testify->tasks->analyze->implement). Consumes upstream intent-integrity-chain/kit conventions. Topics: 00-constitution, 01-specify, 02-plan, 03-checklist, 04-testify, 05-tasks, 06-analyze, 07-implement, 08-taskstoissues, bugfix, clarify, core."
params:
  topic:
    enum: [00-constitution, 01-specify, 02-plan, 03-checklist, 04-testify, 05-tasks, 06-analyze, 07-implement, 08-taskstoissues, bugfix, clarify, core]
    required: true
    infer: from user request; ask only if ambiguous
  depth:
    enum: [quick, deep]
    default: quick
routes:
  00-constitution: references/00-constitution.md
  01-specify: references/01-specify.md
  02-plan: references/02-plan.md
  03-checklist: references/03-checklist.md
  04-testify: references/04-testify.md
  05-tasks: references/05-tasks.md
  06-analyze: references/06-analyze.md
  07-implement: references/07-implement.md
  08-taskstoissues: references/08-taskstoissues.md
  bugfix: references/bugfix.md
  clarify: references/clarify.md
  core: references/core.md
---

# iikit

Router skill for the Intent Integrity Kit: a spec-driven pipeline that turns
intent into shipped code through ordered gates. [DOC]

## When to use
Trigger on any spec-driven request: a constitution, spec, plan, checklist,
tests, task list, or driving implementation/bugfix. Named stage (or its number
`00`–`08`) → that topic; described intent → infer the earliest unmet stage.
Don't use for ad-hoc coding with no spec artifact in play. [INFERENCE]

## Routing
1. Resolve `topic` (enum is authoritative; numbers map 1:1). [CONFIG]
2. Read EXACTLY ONE playbook from `routes:`. Never load the cluster — that
   defeats the router and burns context. [INFERENCE]
3. Apply by `depth`: `deep` → exhaustive, verify each step; `quick` →
   essentials, single pass. [CONFIG]

Pipeline (each output feeds the next): 00-constitution → 01-specify → 02-plan →
03-checklist → 04-testify → 05-tasks → 06-analyze → 07-implement →
08-taskstoissues. `clarify`, `bugfix`, `core` are off-spine helpers. [DOC]

## Inputs / Outputs
- **In:** `topic` (required), `depth` (default `quick`), plus the upstream
  artifact the stage consumes (e.g. 02-plan needs a 01-specify spec). [CONFIG]
- **Out:** the single stage artifact, evidence-tagged with the Alfa core set
  (`[CODE]` `[CONFIG]` `[DOC]` `[INFERENCE]` `[ASSUMPTION]`). [DOC]

## Validation gate (before declaring done)
- Exactly one playbook read; topic ∈ enum; predecessor artifact existed or was
  explicitly created (no stage on a missing predecessor). [INFERENCE]
- Constitution v6.0.0 enforcement honored; script-first rule applied; tags from
  ONE family only. [CONFIG]
- Score against `assets/quality-rubric.json` (QR-01…QR-08); see the `assets/`
  bundle for the routing checklist. [CONFIG]

## Anti-patterns & self-correction
- Loading multiple playbooks "to be safe" — read one, re-route if wrong. [INFERENCE]
- Guessing `topic` when genuinely ambiguous → ask, don't fan out. [ASSUMPTION]
- Skipping a predecessor stage to reach implementation faster. [INFERENCE]
- If the chosen playbook doesn't fit mid-execution: stop, re-resolve `topic`,
  read the correct one — never stack a second on top. [INFERENCE]

Spine: Discover → Analyze → Execute → Validate. [DOC]

## Provenance — tessl tile dependency [DOC]

`iikit` is a thin overlay over the tessl tile `tessl-labs/intent-integrity-kit`. Its
deeper assets — **`iikit-core`** (references like constitution-loading, formatting-guide,
phase-separation-rules, model-recommendations; templates like spec/plan/tasks/checklist)
and the helper scripts under `.tessl/tiles/.../iikit-core/scripts/` — are **provisioned by
tessl at install time**, NOT vendored in this repo. [CONFIG]

- When a playbook names one of those assets in backticks (e.g. `formatting-guide`,
  `spec-template`), read it from the installed tile, not from `skills/iikit/`. [DOC]
- If tessl is not installed (`.tessl/` absent), those assets are unavailable — run the
  spine on the in-repo playbooks (`references/00-08`, `bugfix`, `clarify`, `core`) and
  flag the missing tile. [ASSUMPTION]
- Do NOT fabricate local copies of `iikit-core` content — it is maintained upstream;
  duplicating it would drift. [DOC]