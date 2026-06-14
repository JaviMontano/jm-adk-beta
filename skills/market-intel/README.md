# market-intel — Overview

`market-intel` is a **router skill** for market and competitive intelligence. One
invocation resolves exactly one `topic`, Reads exactly one playbook from
`routes.json`, and runs that playbook's spine: **Discover → Analyze → Execute →
Validate**. It never loads the whole cluster — one topic per call. [CONFIG]

## What it does

Covers eight intelligence topics over the *external market* — positioning,
pricing structure, sector context, peer benchmarks, and partnerships. It does
**not** do product specs, GTM execution, or financial modeling (DCF / unit
economics) — those route elsewhere. [INFERENCIA]

| `topic` (enum) | Job-to-be-done | Playbook |
|---|---|---|
| `competitive-intelligence` | Competitor matrix, tech stack, SWOT, differentiation | `references/competitive-intelligence.md` |
| `competitive-positioning` | Buyer-criteria matrix, battle card, positioning statement | `references/competitive-positioning.md` |
| `benchmarking-analysis` | Subject vs peer/industry gap, prioritized closure | `references/benchmarking-analysis.md` |
| `market-intelligence` | Entity OSINT (company/person/territory/sector), TAM/trends | `references/market-intelligence.md` |
| `sector-intelligence` | Vertical regulation, glossary, value chains, integration rails | `references/sector-intelligence.md` |
| `marketing-context` | Positioning, value props, message hierarchy | `references/marketing-context.md` |
| `partnership-strategy` | Partner fit score, program design, kill criteria | `references/partnership-strategy.md` |
| `pricing-strategy` | Tier architecture, anchoring, decoys, WTP method | `references/pricing-strategy.md` |

## When to use

- You need an evidence-tagged intelligence deliverable on the external market.
- The ask maps cleanly to one of the eight topics above.

Do **not** use for: a one-line fact (`WebSearch` directly), internal-data
analysis (`input-analysis`), DCF / unit economics (`cost-estimation`), or
implementation/architecture (route to a build skill). [INFERENCIA]

## How it routes

1. Infer `topic` from the request using the cue table in `SKILL.md`. Ask only
   when two readings would change the playbook loaded. [CONFIG]
2. Read **only** that topic's file from `routes.json`. [DOC]
3. Set `depth`: `quick` (essentials) or `deep` (apply exhaustively, run the
   playbook's Validate step before output). [CONFIG]
4. Run the playbook's spine and emit its deliverable with evidence tags.

## Evidence taxonomy (per-playbook — do not mix families)

Most playbooks use the **Alfa core** set: `[CÓDIGO]` `[CONFIG]` `[DOC]`
`[INFERENCIA]` `[SUPUESTO]`. Two playbooks carry their own local sets that are
**intentionally not interchangeable**: `market-intelligence` uses
`[EXPLICIT]/[INFERRED]/[OPEN]` (OSINT confidence; wired to HTML chip CSS), and
`competitive-intelligence` / `benchmarking-analysis` use `[EXPLICIT]/[CODE]/
[CONFIG]/[DOC]/[INFERENCE]/[ASSUMPTION]`. Honor whichever family the loaded
playbook declares; never blend two families in one artifact. [DOC]

## References

- `routes.json` — topic → playbook map (source of truth for routing).
- `references/*.md` — the eight playbooks (one loaded per invocation).
- `agents/` — role contracts (lead, specialist, support, guardian).
- `knowledge/` — body of knowledge + concept graph.
- `prompts/` — primary, meta, and quick/deep variations.
- `templates/output.md` — deliverable scaffold.
- `assets/` — quality rubric + routing checklist used by the guardian gate.
- `evals/evals.json` — routing and quality test cases.

Governance: no invented prices (FTE-months + disclaimers only); single brand per
artifact; never green-as-success; no client PII. [CONFIG]
