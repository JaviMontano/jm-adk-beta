---
name: agent-orchestration
version: 1.0.0
description: "Multi-agent orchestration: workflow execution, triad composition, routing, parallelism, subagent monitoring, error recovery, and learning loops. Topics: continuous-learning, error-recovery-automation, intelligent-routing, multi-model-routing, parallel-workflow, socratic-debate, subagent-monitor, task-automation, triad-composition, workflow-orchestration."
params:
  topic:
    enum: [continuous-learning, error-recovery-automation, intelligent-routing, multi-model-routing, parallel-workflow, socratic-debate, subagent-monitor, task-automation, triad-composition, workflow-orchestration]
    required: true
    infer: from user request; ask only if ambiguous
  depth:
    enum: [quick, deep]
    default: quick
routes:
  continuous-learning: references/continuous-learning.md
  error-recovery-automation: references/error-recovery-automation.md
  intelligent-routing: references/intelligent-routing.md
  multi-model-routing: references/multi-model-routing.md
  parallel-workflow: references/parallel-workflow.md
  socratic-debate: references/socratic-debate.md
  subagent-monitor: references/subagent-monitor.md
  task-automation: references/task-automation.md
  triad-composition: references/triad-composition.md
  workflow-orchestration: references/workflow-orchestration.md
---

# agent-orchestration

Router skill: dispatches multi-agent orchestration work to exactly one playbook. [DOC]

## When to use
Any request to compose/route/run/recover/monitor a multi-agent workflow under PRISTINO. [DOC]
NOT for single-agent tasks, content generation, or domain skills — route those to their own skill. [INFERENCE]

## Contract
- **Input**: `topic` (one of the 10 enum values; infer from request, ask only if two routes tie) + `depth`. [CONFIG]
- **Output**: the resolved playbook applied; every non-obvious claim tagged from the Alfa core set
  (`[CODE]`/`[CONFIG]`/`[DOC]`/`[INFERENCE]`/`[ASSUMPTION]`) — never mix tag families. [DOC]

## Procedure
1. Resolve `topic` from the request. Read EXACTLY ONE playbook from `routes:`. Never load the cluster. [CONFIG]
2. `depth=deep` → apply exhaustively, verify at each step; `quick` → essentials only. Default `quick`. [CONFIG]
3. Run the spine: Discover → Analyze → Execute → Validate. [DOC]
4. Gate before "done": constitution v6.0.0 enforcement, evidence tags present, script-first rule honored. [CONFIG]

## Topic disambiguation (pick the narrowest match)
- Role/Lead-Support-Guardian selection → `triad-composition`; which model per task → `multi-model-routing`. [DOC]
- Which skill/agent handles a request → `intelligent-routing`; end-to-end run → `workflow-orchestration`. [DOC]
- Concurrent fan-out → `parallel-workflow`; live subagent status → `subagent-monitor`. [DOC]
- Multi-perspective reasoning → `socratic-debate`; harvesting its insights → `continuous-learning`. [DOC]
- Recover from a failed step → `error-recovery-automation`; schedule/trigger work → `task-automation`. [DOC]

## Acceptance gate
Done only if: one playbook loaded (not many); spine completed; gates passed; tags single-family + EN/ES consistent. [DOC]
Walk `assets/routing-checklist.md` before emitting; Guardian scores with `assets/quality-rubric.json`. [CONFIG]

## Anti-patterns
- Loading multiple playbooks "to be safe" — defeats the router; pick one or ask. [INFERENCE]
- Guessing `topic` when two routes genuinely tie — ask instead of mis-routing. [ASSUMPTION]
- Marking complete without the constitution/evidence/script-first gate. [DOC]
- Inventing a topic outside the enum — the catalog parser rejects it. [CONFIG]

## Self-correction
If mid-run the request no longer fits the chosen `topic`, stop, re-resolve against the
disambiguation table, and switch playbooks — do not stretch the wrong one. [INFERENCE]
