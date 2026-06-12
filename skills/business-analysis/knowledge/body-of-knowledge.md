# Body of Knowledge — business-analysis

Domain knowledge for the nine-topic business-analysis router. Use it to route correctly
and to apply each discipline with the right standards. [DOC]

## 1. The cluster and its spine

All nine topics run the same spine — **Discover → Analyze → Execute → Validate** — and
share one evidence taxonomy and one acceptance gate. They differ in *technique* and
*output*. The router's job is to map intent to exactly one technique. [DOC]

| topic | Answers the question | Core method | Primary output |
|-------|----------------------|-------------|----------------|
| business-process-modeling | How does work flow today? | BPMN 2.0 + value-stream + 8 wastes | As-is/to-be BPMN, PCE |
| flow-mapping | What happens end-to-end across contexts? | DDD bounded contexts + sequence diagrams | 8–12 flows + integration matrix |
| requirements-engineering | What must it do? | INVEST + Gherkin + traceability | Stories + AC + matrix |
| feasibility-validation | Can this be built as scoped? | 7-dimension 1–5 scorecard | Go/no-go/conditional-go + confidence |
| scenario-analysis | Which option wins? | Weighted criteria matrix | Ranked recommendation |
| change-readiness | Are people ready to adopt? | ADKAR per group | Barrier + interventions |
| change-management-enterprise | How do we roll this out org-wide? | Stakeholder + comms + reinforcement | Adoption plan |
| workshop-design | How do we run the discovery session? | Event storming / story mapping / sprint | Agenda + structure |
| workshop-facilitator | How do we facilitate it live? | Timeboxes, divergence/convergence | Facilitation script |

## 2. Standards and frameworks

- **BPMN 2.0** — pools (orgs), lanes (roles), gateways, events. A flowchart without
  pools/lanes is not BPMN: responsibility becomes unattributable. [EXPLICIT]
- **Lean / value-stream** — 8 wastes (defects, overproduction, waiting, non-utilized
  talent, transport, inventory, motion, extra-processing); **Process Cycle Efficiency =
  value-add time ÷ lead time**. [EXPLICIT]
- **DDD** — bounded contexts grouped by ubiquitous language + ownership seam, *not* by
  database table. A flow is a value path from trigger to terminal outcome crossing ≥1
  context. [EXPLICIT]
- **INVEST** — Independent, Negotiable, Valuable, Estimable, Small, Testable. **Gherkin**
  (Given/When/Then) for executable acceptance criteria. [DOC]
- **ADKAR** — Awareness → Desire → Knowledge → Ability → Reinforcement, sequential. The
  barrier is the *first* dimension ≤3 in order; later dimensions are gated by it. [INFERENCE]
- **Weighted decision matrix** — criteria weights sum to 1.0, fixed before scoring;
  weighted total = Σ(weight × score); run a sensitivity check on close calls (top two
  within ~10%). [INFERENCE]

## 3. Decision rules (load-bearing)

1. **Route to exactly one topic.** Tie → ask one question; dominant signal → proceed. [DOC]
2. **Feasibility decision rule** — any dimension = 1 → no-go or conditional-go gated on it;
   mean ≥4 and no dimension <3 → go; else conditional-go with named conditions. Never
   eyeball the mean; a single 1 can sink the project. [INFERENCE]
3. **ADKAR barrier rule** — target the first ≤3 in order, never the numerically lowest and
   never the average. Defer downstream spend until the barrier clears. [INFERENCE]
4. **Scenario weight lock** — define weights *before* generating scenarios; weights set
   after seeing options bias the result. [INFERENCE]
5. **Flow selection** — rank by criticality × frequency × cross-context reach; <8 means the
   domain is under-explored, >12 means you are mapping features not flows. [INFERENCE]
6. **Phase separation (Art. 1.5)** — this cluster describes/analyzes; it does not design
   target architecture, write code, or price. Those belong to plan/dev phases. [CONFIG]
7. **Stack lens** — feasibility/scenario integration points are scored for
   Firebase/Google/Hostinger feasibility; off-stack must justify or be marked infeasible.
   Cost is FTE-time, never currency. [CONFIG]

## 4. Evidence taxonomy

One tag per non-obvious claim, single family, consistent spelling:
`[CODE]` (read from source) · `[CONFIG]` (from configuration) · `[DOC]` (documented) ·
`[INFERENCE]` (reasoned) · `[ASSUMPTION]` (unverified — must name a verification step).
Alfa-distilled references may show `[EXPLICIT]`/`[SUPUESTO]`; same family. If >30% of
claims are `[ASSUMPTION]`, ship a WARNING banner and list the gaps. [CONFIG]

## 5. Common failure modes across the cluster

- Modeling the ideal process instead of the actual as-is. [EXPLICIT]
- Happy-path-only maps/requirements — exception volume is where cost hides. [INFERENCE]
- Averaging scores (ADKAR, feasibility) so a showstopper disappears. [INFERENCE]
- Weight gaming in scenario analysis (weights chosen after scoring). [INFERENCE]
- Green-as-success: a 5 means low risk on that axis, not a guarantee. [EXPLICIT]
- Loading multiple playbooks "to be safe" — defeats the router. [INFERENCE]
