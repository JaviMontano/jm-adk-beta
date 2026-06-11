---
name: iikit
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

Router skill. Resolve `topic` from the request, then Read EXACTLY ONE playbook
from `routes:`. Never load the whole cluster. `depth=deep` → apply the playbook
exhaustively with verification at each step; `quick` → essentials only.

Spine: Discover → Analyze → Execute → Validate.
Quality gates: constitution v6.0.0 (enforcement), evidence tags, script-first rule.
