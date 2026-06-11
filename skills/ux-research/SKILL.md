---
name: ux-research
description: "User research and validation: interviews, surveys, usability testing, and prototyping. Topics: prototyping, survey-design, user-research, user-testing."
params:
  topic:
    enum: [prototyping, survey-design, user-research, user-testing]
    required: true
    infer: from user request; ask only if ambiguous
  depth:
    enum: [quick, deep]
    default: quick
routes:
  prototyping: references/prototyping.md
  survey-design: references/survey-design.md
  user-research: references/user-research.md
  user-testing: references/user-testing.md
---

# ux-research

Router skill. Resolve `topic` from the request, then Read EXACTLY ONE playbook
from `routes:`. Never load the whole cluster. `depth=deep` → apply the playbook
exhaustively with verification at each step; `quick` → essentials only.

Spine: Discover → Analyze → Execute → Validate.
Quality gates: constitution v6.0.0 (enforcement), evidence tags, script-first rule.
