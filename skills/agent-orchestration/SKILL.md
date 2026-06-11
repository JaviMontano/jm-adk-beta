---
name: agent-orchestration
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

Router skill. Resolve `topic` from the request, then Read EXACTLY ONE playbook
from `routes:`. Never load the whole cluster. `depth=deep` → apply the playbook
exhaustively with verification at each step; `quick` → essentials only.

Spine: Discover → Analyze → Execute → Validate.
Quality gates: constitution v6.0.0 (enforcement), evidence tags, script-first rule.
