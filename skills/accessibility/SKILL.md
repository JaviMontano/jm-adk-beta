---
name: accessibility
description: "Accessibility: WCAG audit, testing, design, writing. Topics: audit, design, testing, writing."
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

Router skill. Resolve `topic` from the request, then Read EXACTLY ONE playbook
from `routes:`. Never load the whole cluster. `depth=deep` → apply the playbook
exhaustively with verification at each step; `quick` → essentials only.

Spine: Discover → Analyze → Execute → Validate.
Quality gates: constitution v6.0.0 (enforcement), evidence tags, script-first rule.
