# pm-delivery

Router skill for project and delivery management. It resolves a single `topic`,
loads **exactly one** playbook from `routes.json`, and executes it under the
shared Discover → Analyze → Execute → Validate spine. [EXPLICIT]

## What it does
Covers 11 PM/delivery topics, each backed by a distilled playbook:

| Topic | Deliverable | Playbook |
|-------|-------------|----------|
| budget-management | Budget baseline in FTE-months | `references/budget-management.md` |
| capacity-planning | Capacity model (supply vs. demand) | `references/capacity-planning.md` |
| cost-estimation | FTE-month estimate, opt/exp/pess bands | `references/cost-estimation.md` |
| okr-design | Objective + 2–5 measurable KRs | `references/okr-design.md` |
| product-roadmapping | Now/Next/Later outcome roadmap | `references/product-roadmapping.md` |
| retrospective-facilitation | Retro notes + action items | `references/retrospective-facilitation.md` |
| risk-assessment | Scored risk register (7 categories) | `references/risk-assessment.md` |
| sla-definition | SLA/SLO/SLI targets + error budget | `references/sla-definition.md` |
| stakeholder-mapping | Power/interest grid + RACI | `references/stakeholder-mapping.md` |
| team-topology | Team types + interaction modes | `references/team-topology.md` |
| vendor-evaluation | Weighted vendor scorecard | `references/vendor-evaluation.md` |

## When to use
PM/delivery questions on budgets, estimation, capacity, roadmaps, OKRs, risk,
stakeholders, SLAs, team design, vendors, or retrospectives. **Not** for
discovery, architecture, or coding — route those to their own skills. [INFERENCE]

## How it routes and executes
1. Infer `topic` from the request; if two topics fit, ask one disambiguating
   question — never guess. [EXPLICIT]
2. Read the single matching playbook from `routes.json`. Stop if the path is
   missing. [EXPLICIT]
3. Pick `depth`: `quick` → essentials; `deep` → exhaustive with verification at
   each step. [EXPLICIT]
4. Run the spine and emit the playbook's deliverable, every non-trivial claim
   tagged `[EXPLICIT]` / `[INFERENCE]` / `[ASSUMPTION]`. [EXPLICIT]

## Governance invariants
- No raw prices anywhere — all cost/budget/vendor work uses FTE-months plus a
  disclaimer (Law of No Prices). [EXPLICIT]
- Constitution v6.0.0 enforcement + script-first rule. [EXPLICIT]
- Never report a gate passed without evidence (no green-as-success theater).
  [EXPLICIT]

## References
See `references/*.md` for the 11 playbooks and `SKILL.md` for the routing
contract. Reusable validation artifacts live in `assets/` (see
`assets/README.md`).

## Companion files
- `agents/` — lead, specialist, support, guardian role contracts.
- `knowledge/` — body of knowledge + concept graph.
- `prompts/` — primary, meta, and quick/deep variations.
- `templates/output.md` — deliverable scaffold.
- `evals/evals.json` — acceptance cases.
- `examples/` — a worked risk-assessment run.
