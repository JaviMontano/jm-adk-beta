---
name: business-analysis
version: 1.0.0
description: "Business analysis and change router: process modeling, requirements, feasibility, scenarios, enterprise change management, and workshops. Topics: business-process-modeling, change-management-enterprise, change-readiness, feasibility-validation, flow-mapping, requirements-engineering, scenario-analysis, workshop-design, workshop-facilitator."
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

Router skill. Resolve `topic`, then Read EXACTLY ONE playbook from `routes:`. [DOC]

## When to use
Analyzing the business side of a system: how work flows, what it must do, whether
a path is viable, which option wins, or how people adopt the change. Pick by intent: [INFERENCE]

| Signal in request | topic |
|---|---|
| "how does process X run", BPMN, swimlanes | business-process-modeling |
| "end-to-end flows", DDD contexts, integration map | flow-mapping |
| "what must it do", user stories, acceptance criteria | requirements-engineering |
| "can we / should we", build-vs-buy, constraints | feasibility-validation |
| "compare options A/B/C", weighted trade-off | scenario-analysis |
| "design the session", event storming, story mapping | workshop-design / workshop-facilitator |
| org rollout, stakeholder buy-in, adoption risk | change-management-enterprise / change-readiness |

## Routing contract
1. Infer `topic` from the request; ask ONLY if two topics tie. [DOC]
2. Read the single mapped playbook. NEVER load the whole cluster — defeats the router. [INFERENCE]
3. `depth=deep` → apply the playbook exhaustively, verify at each step; `quick` → essentials only. [DOC]
4. Stack is Firebase/Google-constrained for feasibility/scenario topics — honor it, don't propose off-stack. [CONFIG]

Spine: Discover → Analyze → Execute → Validate.
Quality gates: constitution v6.0.0 (enforcement), evidence tags (Alfa core set,
EN spelling: `[DOC]`/`[INFERENCE]`/`[ASSUMPTION]`/`[CONFIG]`/`[CODE]`), script-first rule. [CONFIG]

## Acceptance (gate before "done")
- Run the gate in `assets/checklist.md`; score against `assets/quality-rubric.json`. [DOC]
- Exactly one playbook loaded; topic matches user intent. [DOC]
- Every non-obvious claim tagged, one family, consistent spelling. [DOC]
- Outputs (flows, matrices, requirements) trace to evidence, not invention. [ASSUMPTION]

## Anti-patterns
- Loading multiple playbooks "to be safe" — pick one. [INFERENCE]
- Guessing `topic` when genuinely ambiguous instead of asking. [ASSUMPTION]
- Pricing or off-stack tooling in feasibility/scenario output. [CONFIG]
