---
name: data-governance
description: "Data governance: privacy patterns, strategy, documentation, storytelling. Topics: audit-trail-design, data-documentation, data-governance, data-privacy-patterns, data-storytelling, data-strategy, pipeline-governance."
params:
  topic:
    enum: [audit-trail-design, data-documentation, data-governance, data-privacy-patterns, data-storytelling, data-strategy, pipeline-governance]
    required: true
    infer: from user request; ask only if ambiguous
  depth:
    enum: [quick, deep]
    default: quick
routes:
  audit-trail-design: references/audit-trail-design.md
  data-documentation: references/data-documentation.md
  data-governance: references/data-governance.md
  data-privacy-patterns: references/data-privacy-patterns.md
  data-storytelling: references/data-storytelling.md
  data-strategy: references/data-strategy.md
  pipeline-governance: references/pipeline-governance.md
---

# data-governance

Router skill. Resolve `topic` from the request, then Read EXACTLY ONE playbook
from `routes:`. Never load the whole cluster. `depth=deep` → apply the playbook
exhaustively with verification at each step; `quick` → essentials only.

Spine: Discover → Analyze → Execute → Validate.
Quality gates: constitution v6.0.0 (enforcement), evidence tags, script-first rule.
