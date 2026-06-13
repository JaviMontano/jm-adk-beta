---
name: sales-bizdev
version: 1.0.0
description: "Router for sales and business development in an ES/EN consulting context — prospecting, outreach, dossiers, proposals, pitches, and collateral. Topics: b2b-outreach, client-dossier, client-prospecting, executive-pitch, lead-generation, proposal-writing, sales-collateral."
params:
  topic:
    enum: [b2b-outreach, client-dossier, client-prospecting, executive-pitch, lead-generation, proposal-writing, sales-collateral]
    required: true
    infer: from user request; ask only if ambiguous
  depth:
    enum: [quick, deep]
    default: quick
routes:
  b2b-outreach: references/b2b-outreach.md
  client-dossier: references/client-dossier.md
  client-prospecting: references/client-prospecting.md
  executive-pitch: references/executive-pitch.md
  lead-generation: references/lead-generation.md
  proposal-writing: references/proposal-writing.md
  sales-collateral: references/sales-collateral.md
---

# sales-bizdev

Router skill: resolve ONE `topic`, Read EXACTLY ONE playbook from `routes:`, execute its spine. [DOC]

## When to use
Any sales/bizdev deliverable: cold/warm outreach, account dossiers, prospect/lead lists, executive pitches, proposals, or sales collateral. Not for delivery, billing, or post-sale account management. [INFERENCIA]

## Routing
1. Map the request to one enum `topic` (above). Pick by deliverable, not channel. [INFERENCIA]
2. Tie-break overlaps: list of accounts → `client-prospecting`; scored/qualified pipeline → `lead-generation`; one-account deep brief → `client-dossier`; per-contact message → `b2b-outreach`. [SUPUESTO]
3. If two topics fit equally or none does, ask one disambiguating question — never load two playbooks. [DOC]
4. `depth=deep` → apply the playbook exhaustively, verifying at each step; `quick` → essentials only. [DOC]

## Inputs / Outputs
- **In:** `topic`, `depth`, plus the request's account/ICP/context. Missing target account or ICP for prospecting/dossier work is `[SUPUESTO]` — fill or ask, don't fabricate. [INFERENCIA]
- **Out:** the deliverable defined by the chosen playbook, evidence-tagged. Estimates follow Constitution P8 (computed from decomposition + sources, never guessed). Under a commercial profile that forbids client-facing prices (e.g. MetodologIA), express effort in units (FTE-months) + disclaimer, never an unauthorized quote; a profile that permits pricing may state figures. [DOC]

## Guardrails (Alfa core tags only — kit-facing)
- Tag non-obvious claims with `[CÓDIGO]`/`[CONFIG]`/`[DOC]`/`[INFERENCIA]`/`[SUPUESTO]`; one tag, one spelling, one family per output. See `references/verification-tags.md`. [DOC]
- Script-first: prefer a repo script over ad-hoc steps where one exists. [DOC]
- Single-brand: identify the brand first; never mix brands in one output. [DOC]
- Quality gates: constitution v6.0.0 (enforcement) + evidence tags. [CONFIG]
- Routing, scoring, and gate aids live in `assets/` (`routing-matrix.json`, `quality-rubric.json`, `preflight-checklist.md`). [CONFIG]

## Acceptance criteria
- Exactly one playbook loaded; `topic` ∈ enum; cluster never bulk-loaded. [DOC]
- Output matches the playbook's spine (Discover → Analyze → Execute → Validate) and `depth`. [DOC]
- Every non-obvious claim carries one Alfa-core tag; no invented prices; single brand. [DOC]
- Each `[SUPUESTO]` pairs with a concrete next step that would verify it. [DOC]

## Anti-patterns
- Loading multiple playbooks "to be safe", or answering inline without reading the route. [INFERENCIA]
- Guessing `topic` on a genuine tie instead of asking. [INFERENCIA]
- Emitting a price, mixing brands, or using Jarvis-set `{…}` tags in this kit output. [DOC]

## Self-correction
Two routes feel right → re-read tie-break rules; still tied → ask. About to state a number → tag and check it's not a price. Mid-task you find the wrong topic was chosen → stop, re-route, restart the spine. [INFERENCIA]
