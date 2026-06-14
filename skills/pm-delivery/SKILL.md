---
name: pm-delivery
version: 1.0.0
description: "Project and delivery management router: budgets, estimation, capacity, roadmaps, OKRs, risks, stakeholders, vendors, SLAs, team topology, and retrospectives. Topics: budget-management, capacity-planning, cost-estimation, okr-design, product-roadmapping, retrospective-facilitation, risk-assessment, sla-definition, stakeholder-mapping, team-topology, vendor-evaluation."
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

Router skill for project/delivery management. Resolve `topic`, Read EXACTLY ONE
playbook from `routes:`, then execute it. Never load the whole cluster. [EXPLICIT]

## When to use
PM/delivery questions on budgets, estimation, capacity, roadmaps, OKRs, risk,
stakeholders, SLAs, team design, vendors, or retros. NOT for: discovery,
architecture, or coding — route those to their own skills. [INFERENCE]

## Inputs / Outputs
- **In:** `topic` (one of 11 enums) + `depth` (quick|deep). [EXPLICIT]
- **Out:** the playbook's deliverable (matrix, register, estimate, plan), every
  non-trivial claim carrying an evidence tag. [EXPLICIT]

## Procedure
1. Infer `topic` from the request; if two topics fit, ask one disambiguating
   question — do NOT guess. [EXPLICIT]
2. Read the single matching playbook. Stop if the path is missing. [EXPLICIT]
3. `quick` → essentials only; `deep` → apply exhaustively with verification at
   each step. [EXPLICIT]
4. Run the spine: Discover → Analyze → Execute → Validate. [EXPLICIT]

## Acceptance gate (all must hold)
- Exactly one playbook loaded; output matches its template. [EXPLICIT]
- Every claim tagged `[EXPLICIT]` / `[INFERENCE]` / `[ASSUMPTION]`. [EXPLICIT]
- No raw prices anywhere — cost work uses FTE-months + disclaimers. [EXPLICIT]
- Constitution v6.0.0 enforcement + script-first rule satisfied. [EXPLICIT]
- Gate verified against `assets/` (rubric + checklist) — see `assets/README.md`. [EXPLICIT]

## Self-correction triggers
- Loaded >1 playbook, or summarized from memory instead of reading → restart at
  step 1. [EXPLICIT]
- A price slipped into a cost/budget/vendor output → convert to FTE-months. [EXPLICIT]
- Output skips the Discover/Validate ends of the spine → redo those steps. [INFERENCE]

## Anti-patterns
- Pre-reading or merging multiple playbooks "for context." [EXPLICIT]
- Inventing topics outside the enum, or renaming routes. [EXPLICIT]
- Green-as-success theater: never report a gate passed without evidence. [EXPLICIT]
