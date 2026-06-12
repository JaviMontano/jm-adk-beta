# Example output — carrera (topic: negociacion-oferta)

**Routing trace:** topic=`negociacion-oferta` · depth=`quick` · playbook=`references/negociacion-oferta.md`
**Tag family:** authoring `[DOC][CONFIG][INFERENCIA][SUPUESTO]`
**Status:** `complete`

## 1. Request & scope
- Ask: decide which of two supplied offers is acceptable under fixed constraints.
- In scope: ranking supplied offers + evidence-tied open questions. Out of scope:
  market benchmarks, FX conversion, hiring guarantees. [DOC]

## 2. Evidence inventory
| ID | Source type | Short summary |
|----|-------------|---------------|
| E-001 | written_offer | Offer A: 5000 USD/mo, remote, non-exclusive, relocation-OK |
| E-002 | recruiter_email | Offer B: 6500 USD/mo, hybrid, exclusive, no-relocation |

Constraints: `floor_usd=4500`, parallel-stream required, relocation goal = true. [CONFIG]

## 3. Analysis — offer table

| Offer | Floor (≥4500) | Parallel-stream (non-exclusive) | Relocation goal | Hard filters | PIVOTE | Rankable |
|-------|---------------|----------------------------------|-----------------|--------------|--------|----------|
| A (E-001) | PASS (5000) | PASS (non-exclusive) | PASS | PASS | scored from supplied facts | YES |
| B (E-002) | PASS (6500) | FAIL (exclusive) | FAIL (no relocation) | FAIL | not scored (hard fail) | NO |

- Offer B's higher pay does **not** override the parallel-stream and relocation
  hard fails. PIVOTE is only computed after hard filters pass. [INFERENCIA]
- No FX, market rate, or competing offer was invented; both offers came already
  in USD from supplied evidence. [DOC]

## 4. Open questions & risks
- Open question for B: "¿Puede acotarse la exclusividad para permitir un stream
  paralelo, y hay compatibilidad de reubicación?" — no decision until answered. [SUPUESTO]
- Risk: anchoring on B's higher number → mitigation: hard filters gate first. [INFERENCIA]

## 5. Recommendation / next action
- **Acceptable offer: A only.** B is excluded on hard filters despite higher pay.
- Single next action: send B the scoped-exclusivity question above before any
  further comparison. [INFERENCIA]

## 6. Validation
- Validator run: `python3 skills/negociacion-oferta/scripts/score_oferta.py --input packet.json` → exit `0`
- `bash skills/negociacion-oferta/scripts/check.sh` → exit `0` (valid/blocked/invalid fixtures pass) [CÓDIGO]
- Determinism: filters and PIVEOTE order fixed; identical packet ⇒ identical bytes. [INFERENCIA]
- Guardian gates: single-playbook · contract-shape · one-tag-family ·
  no-invented-numbers · stop-on-empty · no-FOMO counterproposal → **pass**. [DOC]
