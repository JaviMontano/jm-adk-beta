# sales-bizdev — Skill Overview

Router skill for sales and business development in an ES/EN consulting context. It resolves **one** `topic` from a request and loads **exactly one** playbook, then executes that playbook's spine to produce an evidence-tagged deliverable — never a price, never mixed brands.

## What it does

Turns a sales/BD intent into a concrete artifact across seven deliverable families:

| Topic | Deliverable | Route |
|-------|-------------|-------|
| `client-prospecting` | Tiered, BANT+Fit-scored prospect list + per-Tier-1 approach brief | `references/client-prospecting.md` |
| `lead-generation` | Lead-capture system + fit×intent qualification handoff | `references/lead-generation.md` |
| `client-dossier` | Battle-ready intelligence brief (Company DNA, contacts, pain hypotheses, approach) | `references/client-dossier.md` |
| `b2b-outreach` | 5-touch sequence with persona hooks, subject variants, response handlers, CSV tracker | `references/b2b-outreach.md` |
| `executive-pitch` | C-level PAS pitch + business case (NPV/IRR/payback, 3-option comparison) | `references/executive-pitch.md` |
| `proposal-writing` | Win-shaped proposal (problem reframe, scope/anti-scope, FTE-month effort, risks) | `references/proposal-writing.md` |
| `sales-collateral` | One-pager / battle card / ROI calculator / competitive positioning | `references/sales-collateral.md` |

## When to use

Any pre-sale sales/bizdev deliverable: cold/warm outreach, account dossiers, prospect or lead lists, executive pitches, proposals, or collateral. **Not** for delivery, billing, or post-sale account management.

## How it routes and executes

1. Map the request to one enum `topic` by **deliverable**, not channel (see `SKILL.md` → Routing).
2. Tie-break overlaps: list of accounts → `client-prospecting`; scored/qualified pipeline → `lead-generation`; one-account deep brief → `client-dossier`; per-contact message → `b2b-outreach`.
3. Load **only** the matching route; if a genuine tie or no fit, ask one disambiguating question — never load two playbooks.
4. `depth=deep` runs the playbook exhaustively with per-step verification; `quick` runs essentials only.
5. Execute the playbook spine: **Discover → Analyze → Execute → Validate**, then pass the deliverable through the playbook's Validation Gate.

## Evidence taxonomy (kit-facing, Alfa core)

Every non-obvious claim carries exactly one tag, one spelling, one family per output:
`[CÓDIGO]` `[CONFIG]` `[DOC]` `[INFERENCIA]` `[SUPUESTO]`. Some playbooks (b2b-outreach, client-prospecting, client-dossier) use the Alfa-style `[EXPLICIT]`/`[INFERRED]`/`[OPEN]` convention internally — match the loaded playbook, do not cross families.

## Hard rules

- **Estimation per Constitution P8** (computed + sourced). Pricing is profile-scoped: under a commercial profile that forbids client prices (e.g. MetodologIA), express effort in FTE-months + disclaimer and route a price request to a human; a pricing-enabled profile may quote.
- **Single brand.** Identify the brand first; never introduce an off-brand element.
- **Every `[SUPUESTO]` pairs with a verify step.** No hypothesis presented as confirmed fact.
- **No client PII** beyond public professional context.

## Bundle contents

- `SKILL.md` — router contract and routing rules.
- `references/*.md` — the seven playbooks.
- `agents/` — role contracts (lead, specialist, support, guardian).
- `knowledge/` — body of knowledge + concept graph.
- `prompts/` — primary, meta, and quick/deep variations.
- `templates/output.md` — deliverable scaffold.
- `evals/evals.json` — calibration cases.
- `examples/` — a worked input/output pair.
- `assets/` — quality rubric, routing matrix, and pre-flight checklist (see `assets/README.md`).
