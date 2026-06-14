# Body of Knowledge — pm-delivery

Stable domain knowledge for the project/delivery management router. Scoped to the
11 routed topics and their shared governance. [EXPLICIT]

## 1. Routing model
pm-delivery is a **single-route dispatcher**. The contract is: resolve one
`topic` from the enum, load exactly one playbook, execute its method, validate.
Merging or pre-reading playbooks violates the contract and inflates context.
[EXPLICIT]

Topics (11): budget-management, capacity-planning, cost-estimation, okr-design,
product-roadmapping, retrospective-facilitation, risk-assessment, sla-definition,
stakeholder-mapping, team-topology, vendor-evaluation.

## 2. Shared execution spine
**Discover → Analyze → Execute → Validate.** Discover gathers artifacts and
constraints; Analyze applies the playbook method; Execute produces the formatted
deliverable; Validate runs the acceptance gate. Skipping the Discover or Validate
ends is the most common failure. [EXPLICIT]

## 3. Evidence taxonomy
Every non-trivial claim is tagged:
- `[EXPLICIT]` — stated in an artifact or the request.
- `[INFERENCE]` — derived by reasoning from evidence.
- `[ASSUMPTION]` — no supporting artifact; a guess that must be visible.

If `[ASSUMPTION]` exceeds 30% of claims, the deliverable carries a WARNING banner
— evidence is thin and discovery is recommended before commitment. [EXPLICIT]

## 4. Cost discipline — the Law of No Prices
Cost-bearing topics (cost-estimation, budget-management, vendor-evaluation) emit
**FTE-months**, never currency, rates, or prices. Estimation method:
`FTE-months = effort inductors × scope multipliers`, aggregated per workstream,
always reported as an **optimistic / expected / pessimistic** band — never a
single point. Wide spread (pessimistic − optimistic) signals that more discovery
is needed before commitment. [EXPLICIT]

## 5. Key concepts and decision rules per topic
- **Risk scoring**: Severity (1–5) × Likelihood (1–5) = Score (1–25). Bands:
  1–6 Low, 8–12 Medium, 15–25 High. High requires a named mitigation before
  sign-off. 7 categories: technical, operational, security, scalability, data,
  team, timeline. [EXPLICIT]
- **OKRs**: one qualitative Objective (no embedded metric) + 2–5 outcome KRs,
  each with baseline → target → due date and a single owner. Score =
  `(current − baseline)/(target − baseline)` clamped 0.0–1.0. Healthy stretch
  band 0.6–0.7; consistent 1.0 means targets are too soft. [EXPLICIT]
- **Stakeholders**: power/interest grid (manage closely / keep satisfied / keep
  informed / monitor) plus a RACI matrix and a communication cadence. [EXPLICIT]
- **Team topology**: Conway's Law — system structure mirrors org structure. Team
  types and interaction modes (collaboration, X-as-a-Service, facilitating);
  manage cognitive load per team. [EXPLICIT]
- **Capacity**: model demand (committed work) against supply (available
  FTE-months net of leave, ceremonies, on-call); flag over-allocation. [INFERENCE]
- **SLA/SLO/SLI**: SLI is the measured signal, SLO the internal target, SLA the
  external promise; the gap between 100% and the SLO is the error budget. [EXPLICIT]
- **Vendor evaluation**: weighted scorecard across explicit criteria; selection
  expressed without prices (effort/fit, not cost). [EXPLICIT]

## 6. Standards and references
- Constitution v6.0.0 — evidence law, phase separation (Art. 1.5), output
  standards (R-008), single-brand, no client PII. [EXPLICIT]
- Script-first rule: prefer deterministic scripts for computation over ad-hoc
  hand math. [EXPLICIT]
- Quality rubric shipped in `assets/quality-rubric.json`; gate checklist in
  `assets/checklist.md`. [EXPLICIT]

## 7. Anti-scope
Discovery, architecture, and coding are out of scope — route those to their own
skills. This router never invents topics outside the enum or renames routes.
[EXPLICIT]
