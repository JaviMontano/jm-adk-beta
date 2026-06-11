---
name: pm-delivery
description: "Project and delivery management: budgets, estimation, capacity, roadmaps, OKRs, risks, stakeholders, vendors, and retrospectives. Topics: budget-management, capacity-planning, cost-estimation, okr-design, product-roadmapping, retrospective-facilitation, risk-assessment, sla-definition, stakeholder-mapping, team-topology, vendor-evaluation."
params:
  topic:
    enum: [budget-management, capacity-planning, cost-estimation, okr-design, product-roadmapping, retrospective-facilitation, risk-assessment, sla-definition, stakeholder-mapping, team-topology, vendor-evaluation]
    required: true
    infer: from user request; ask only if ambiguous
  depth:
    enum: [quick, deep]
    default: quick
routes:
  budget-management: references/budget-management.md
  capacity-planning: references/capacity-planning.md
  cost-estimation: references/cost-estimation.md
  okr-design: references/okr-design.md
  product-roadmapping: references/product-roadmapping.md
  retrospective-facilitation: references/retrospective-facilitation.md
  risk-assessment: references/risk-assessment.md
  sla-definition: references/sla-definition.md
  stakeholder-mapping: references/stakeholder-mapping.md
  team-topology: references/team-topology.md
  vendor-evaluation: references/vendor-evaluation.md
---

# pm-delivery

Router skill. Resolve `topic` from the request, then Read EXACTLY ONE playbook
from `routes:`. Never load the whole cluster. `depth=deep` → apply the playbook
exhaustively with verification at each step; `quick` → essentials only.

Spine: Discover → Analyze → Execute → Validate.
Quality gates: constitution v6.0.0 (enforcement), evidence tags, script-first rule.
