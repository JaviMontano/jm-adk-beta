---
name: legal-compliance
description: "Legal and compliance: contract review, compliance frameworks, and assessments. Topics: compliance-assessment, compliance-framework, contract-review."
params:
  topic:
    enum: [compliance-assessment, compliance-framework, contract-review]
    required: true
    infer: from user request; ask only if ambiguous
  depth:
    enum: [quick, deep]
    default: quick
routes:
  compliance-assessment: references/compliance-assessment.md
  compliance-framework: references/compliance-framework.md
  contract-review: references/contract-review.md
---

# legal-compliance

Router skill. Resolve `topic` from the request, then Read EXACTLY ONE playbook
from `routes:`. Never load the whole cluster. `depth=deep` → apply the playbook
exhaustively with verification at each step; `quick` → essentials only.

Spine: Discover → Analyze → Execute → Validate.
Quality gates: constitution v6.0.0 (enforcement), evidence tags, script-first rule.
