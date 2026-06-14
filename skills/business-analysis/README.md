# business-analysis

Router skill for the **business side** of a system: how work flows, what it must do,
whether a path is viable, which option wins, and how people adopt the change. It does
**not** do the work itself — it resolves a `topic`, then loads **exactly one** playbook
from `references/` and runs it. [DOC]

## What it does

Given a request, `business-analysis` selects one of nine business-analysis disciplines
and executes its playbook end-to-end under the **Discover → Analyze → Execute → Validate**
spine, emitting an evidence-tagged deliverable (flows, requirements, matrices, scorecards,
ADKAR diagnoses). It is the single entry point so the caller never has to remember nine
separate skill names. [DOC]

## When to use it

| Signal in the request | topic | Playbook |
|---|---|---|
| "how does process X run", BPMN, swimlanes, value stream | `business-process-modeling` | [references/business-process-modeling.md](references/business-process-modeling.md) |
| "end-to-end flows", DDD contexts, integration map, sequence diagrams | `flow-mapping` | [references/flow-mapping.md](references/flow-mapping.md) |
| "what must it do", user stories, acceptance criteria, INVEST/Gherkin | `requirements-engineering` | [references/requirements-engineering.md](references/requirements-engineering.md) |
| "can we / should we build this", build-vs-buy, 7-dimension go/no-go | `feasibility-validation` | [references/feasibility-validation.md](references/feasibility-validation.md) |
| "compare options A/B/C", weighted trade-off, scenario matrix | `scenario-analysis` | [references/scenario-analysis.md](references/scenario-analysis.md) |
| "design the session", event storming, story mapping, design sprint | `workshop-design` / `workshop-facilitator` | [references/workshop-design.md](references/workshop-design.md) · [references/workshop-facilitator.md](references/workshop-facilitator.md) |
| org rollout, stakeholder buy-in, ADKAR, adoption risk | `change-management-enterprise` / `change-readiness` | [references/change-management-enterprise.md](references/change-management-enterprise.md) · [references/change-readiness.md](references/change-readiness.md) |

## How it routes and executes

1. **Infer `topic`** from the request. Ask only if two topics genuinely tie. [DOC]
2. **Read the single mapped playbook** from `routes.json`. Never load the whole cluster —
   that defeats the router and burns the context budget. [INFERENCE]
3. **Pick `depth`** — `quick` (essentials) or `deep` (apply the playbook exhaustively,
   verify at every step). Default `quick`. [DOC]
4. **Honor the stack constraint** — feasibility and scenario topics are
   Firebase/Google/Hostinger-lensed; off-stack options must justify the exception or be
   marked infeasible. No pricing — express effort as FTE-time only. [CONFIG]

## Evidence taxonomy

Every non-obvious claim carries exactly one tag from a single family and consistent
spelling: `[DOC]` (documented), `[CODE]` (read from source), `[CONFIG]` (from
configuration), `[INFERENCE]` (reasoned), `[ASSUMPTION]` (unverified — must be paired with
a verification step). Alfa-distilled references may also surface `[EXPLICIT]`/`[SUPUESTO]`;
treat them as the same family. [CONFIG]

## Companion files

- `SKILL.md` — the routing contract and acceptance gate (canonical).
- `agents/` — role contracts: lead, specialist, support, guardian.
- `knowledge/` — body of knowledge + concept graph for the cluster.
- `prompts/` — primary, meta, and quick/deep variations.
- `templates/output.md` — the deliverable scaffold.
- `evals/evals.json` — the gate cases.
- `examples/` — a worked requirements-engineering example.
- `assets/` — the quality rubric and routing checklist that gate "done".
