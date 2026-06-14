<!-- distilled from alfa skills/negociacion-oferta -->
<!-- Evalua ofertas profesionales con filtros de aceptacion, PIVOTE, evidencia suministrada y contrapropuestas sin presion, numeros inventados ni claims de mercado vivo. -->
# Negociacion Oferta

## Purpose

Use this skill when the user needs to compare job, consulting, advisory, or project offers and decide whether to accept, reject, ask questions, or prepare a counterproposal. The skill is deterministic: it scores only the offer facts the user supplies, applies fixed acceptance filters, and blocks unsupported claims about market rates, competing offers, or guaranteed outcomes. [DOC]

**In scope:** ranking supplied offers, decision packets, evidence-tied questions, calm counterproposals. **Anti-scope (never do):** invent market benchmarks, exchange rates, tax/equity values, competing offers, or hiring guarantees; decide for the user; emit pressure or scarcity language. [DOC] These boundaries are the skill's reason to exist — relaxing them silently is the primary failure mode. [INFERENCIA]

## Inputs Expected

- Offer facts: name, monthly USD amount or normalized USD amount, work mode, exclusivity, relocation compatibility, and relevant notes. [DOC]
- User constraints: `floor_usd`, minimum optionality, relocation goal, parallel-stream requirement, and deal breakers. [CONFIG]
- PIVOTE dimensions: purpose, income, viability, optionality, traction, and energy, each scored 0 to 10 from supplied facts. [DOC]
- Evidence list for non-obvious claims: written offer, recruiter statement, contract clause, user preference, documented competing offer, or known constraint. [DOC]
- Desired output: ranking, decision packet, questions to ask, or counterproposal draft. [DOC]

**Minimum to score one offer:** name, USD amount, work mode, exclusivity, relocation flag, plus `floor_usd`. Anything else absent becomes an open question, not a default. [SUPUESTO] Verify by running the packet through `score_oferta.py`; a missing required field yields a blocked output, not a guess. [CONFIG]

## Outputs Expected

- One deterministic offer table with pass/fail filters and PIVOTE score. [DOC]
- A ranked list of offers that pass every acceptance filter. [DOC]
- A blocked or partial decision when required evidence is missing. [DOC]
- A counterproposal plan only when supported by the supplied offer facts. [DOC]
- Risk notes for pressure language, fabricated leverage, market-data claims, exclusivity, relocation, and hustle culture. [DOC]

## Procedure

### Discover

Identify the decision target, normalize supplied compensation to monthly USD only when the user provides the conversion, and capture constraints before scoring. If conversion, taxes, equity value, or benefits are needed but not supplied, mark them as open questions instead of inventing them. [DOC] **Decision — user-supplied conversion only:** trade off convenience for trust; a hidden FX default could silently flip a pass/fail at the floor, so the skill refuses to convert rather than risk a wrong recommendation. [INFERENCIA]

### Analyze

Apply `assets/acceptance-filters.json`, `assets/pivote-rubric.json`, `assets/evidence-policy.json`, and `assets/counteroffer-policy.json`. Treat live market benchmarks as out of scope unless the user provides a source. [CONFIG] Hard filters (floor, exclusivity vs parallel streams, relocation, deal breakers) gate ranking; PIVOTE is a quality score applied only after hard filters pass. [INFERENCIA]

### Execute

Score every offer with `scripts/score_oferta.py`. Rank only offers that pass all filters. Draft a counterproposal in calm language, anchored to supplied value, scope, constraints, and requested adjustment. Do not create fake competing offers, ultimatums, scarcity pressure, or guaranteed hiring outcomes. [DOC]

### Validate

Run the deterministic fixture suite:

```bash
bash skills/negociacion-oferta/scripts/check.sh
```

For one decision packet:

```bash
python3 skills/negociacion-oferta/scripts/score_oferta.py --input <packet.json>
```

## Worked Example

Input: Offer A `5000` USD/mo, remote, non-exclusive, relocation-compatible; Offer B `6500` USD/mo, hybrid, exclusive, no relocation. Constraints: `floor_usd=4500`, parallel-stream required, relocation goal true. [SUPUESTO]

- Offer A: passes floor (5000 ≥ 4500), passes parallel-stream (non-exclusive), passes relocation. PIVOTE computed from supplied facts. → **rankable**. [INFERENCIA]
- Offer B: passes floor, but exclusivity fails the parallel-stream requirement and relocation fails the goal. → **fail, not ranked**, despite higher pay. [INFERENCIA]

Result: B's higher number does not override hard filters; the packet returns A as the only acceptable offer plus a question for B ("can exclusivity be scoped to allow one parallel stream?"). Verify by scoring both packets and confirming B is excluded. [CONFIG]

## Assets

- `assets/acceptance-filters.json`
- `assets/pivote-rubric.json`
- `assets/evidence-policy.json`
- `assets/counteroffer-policy.json`
- `assets/output-contract.json`

## Quality Criteria

- Every offer has required numeric and boolean fields before scoring. [DOC]
- PIVOTE is computed from six bounded dimensions, not a free-form vibe. [DOC]
- Each specific claim references supplied evidence or is marked as an open question. [DOC]
- Counterproposal language is respectful and firm; it avoids FOMO, ultimatums, hustle glorification, and fabricated leverage. [DOC]
- Offers that fail any hard filter are not ranked as acceptable. [DOC]
- Missing compensation, exclusivity, relocation, or evidence produces a blocked output instead of a confident recommendation. [DOC]

## Edge Cases

- No offers: block and request at least one offer packet. [DOC]
- Salary exactly equals the floor: pass the compensation filter (`>=`, not `>`). [CONFIG]
- Strong compensation but exclusivity blocks parallel streams: fail unless the user explicitly marks it as an accepted documented exception. [DOC]
- PIVOTE average above 7 but one dimension below 5: fail the PIVOTE gate. [CONFIG]
- User asks to cite market rates without a source: mark as unsupported. [DOC]
- User asks to pretend there is another offer: block fabricated leverage. [DOC]
- User asks for aggressive pressure language: rewrite to calm counterproposal language. [DOC]
- Two offers tie on every filter and PIVOTE: report the tie, do not break it with an invented tiebreaker; surface the deciding question to the user. [SUPUESTO]
- Compensation supplied in non-USD with no conversion: block the compensation filter as an open question, never assume a rate. [INFERENCIA]

## Failure Modes

- **Silent FX/tax default** flips a floor decision: prevented by user-supplied-conversion-only rule; if tempted, emit an open question. [INFERENCIA]
- **PIVOTE laundering a hard fail**: a high average must never resurrect an offer that failed a hard filter; hard filters gate first. [INFERENCIA]
- **Politeness drift into servility or FOMO** in the counterproposal: lint against hustle/ultimatum/scarcity before output. [DOC]
- **Tag inflation**: do not tag restated user input or the output's own structure; over-tagging defeats scannability. [INFERENCIA]

## Assumptions and Limits

- This skill is career and negotiation support, not legal, tax, immigration, or financial advice. [DOC]
- It does not fetch market data, exchange rates, tax tables, or live job-market information. [DOC]
- It does not decide for the user; it produces a traceable decision packet from supplied constraints. [DOC]
- Evidence tags follow the Alfa core set; do not mix in the Jarvis operator family in this document. [CONFIG]

## Scripts

`scripts/score_oferta.py --input <json>` validates and scores offer packets against acceptance filters, PIVOTE dimensions, evidence policy, pressure language, and counteroffer boundaries. `scripts/check.sh` runs valid, blocked, and invalid fixtures offline. [CONFIG] A non-zero exit from `check.sh` means a fixture regressed — treat scoring as untrusted until it passes. [INFERENCIA]

## Related Skills

- `validar-liquidacion-co`
- `gratitud-post-proceso`
- `proceso-seleccion-orchestrator`

## Evidence Requirements

- Tie compensation, work mode, exclusivity, relocation, benefits, competing-offer leverage, and next-step claims to supplied evidence. [DOC]
- Mark live market, tax, equity, or immigration assumptions as open questions unless a source is provided. [DOC]
- Report validation commands and results when a machine-readable packet is used. [DOC]

## Acceptance Criteria

- Every offer scored only after all required fields are present; otherwise blocked. [DOC]
- Hard filters gate ranking; PIVOTE never overrides a hard fail. [INFERENCIA]
- No invented market data, FX, competing offers, or hiring guarantees appear anywhere in the output. [DOC]
- Counterproposal passes the pressure-language lint (no FOMO, ultimatum, scarcity, servility). [DOC]
- Every non-obvious claim carries exactly one Alfa-set tag; spelling is consistent. [DOC]
- Validation commands and their results are reported for machine-readable packets. [DOC]

## Update-Safety Notes

- Keep scoring deterministic and offline. [DOC]
- Do not add network calls, wall-clock market data, randomness, or hidden default conversions. [DOC]
- Preserve user facts and avoid changing other skills during hardening. [DOC]
- Preserve the H2 heading set and the asset/script paths above; routes and the alfa source bind to them. [CONFIG]
