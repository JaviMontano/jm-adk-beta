---
name: business-analysis
description: "Business analysis and change: process modeling, requirements, feasibility, scenarios, enterprise change management, and workshops. Topics: business-process-modeling, change-management-enterprise, change-readiness, feasibility-validation, flow-mapping, requirements-engineering, scenario-analysis, workshop-design, workshop-facilitator."
params:
  topic:
    enum: [business-process-modeling, change-management-enterprise, change-readiness, feasibility-validation, flow-mapping, requirements-engineering, scenario-analysis, workshop-design, workshop-facilitator]
    required: true
    infer: from user request; ask only if ambiguous
  depth:
    enum: [quick, deep]
    default: quick
routes:
  business-process-modeling: references/business-process-modeling.md
  change-management-enterprise: references/change-management-enterprise.md
  change-readiness: references/change-readiness.md
  feasibility-validation: references/feasibility-validation.md
  flow-mapping: references/flow-mapping.md
  requirements-engineering: references/requirements-engineering.md
  scenario-analysis: references/scenario-analysis.md
  workshop-design: references/workshop-design.md
  workshop-facilitator: references/workshop-facilitator.md
---

# business-analysis

Router skill. Resolve `topic` from the request, then Read EXACTLY ONE playbook
from `routes:`. Never load the whole cluster. `depth=deep` → apply the playbook
exhaustively with verification at each step; `quick` → essentials only.

Spine: Discover → Analyze → Execute → Validate.
Quality gates: constitution v6.0.0 (enforcement), evidence tags, script-first rule.
