# DataFlux SaaS MSA — Contract Review (pre-signature)

> **Disclaimer (verbatim, mandatory):** This is a technical compliance gap
> assessment, not legal advice. Regulatory interpretations and penalty exposure must
> be validated by qualified legal counsel before action.

**Resolved route:** topic = `contract-review` · depth = `quick`
**Scope:** DataFlux SaaS MSA · governing law Delaware (single jurisdiction)
**Snapshot date:** 2026-06-12 — provisional pending missing Schedule C (DPA)

## Intake stop — missing exhibit
Schedule C (Data Processing Addendum) is referenced in Clause 11 but was not
attached. Findings below are **provisional**; the DPA commonly carries breach-notice
SLAs, sub-processor consent, and audit rights that change exposure. Request Schedule
C before sign-off. [INFERENCIA]

## Findings (ranked by exposure, not clause order)

| Clause | Risk | Plain-language impact | Recommended redline / fallback | Tag |
|--------|------|-----------------------|--------------------------------|-----|
| 8.4 vs 8.2 | **High** | The 8.2 cap (12 months' fees) is voided for any confidentiality breach (8.4). Because Clause 11 folds all processed personal data into "Confidential Information," a single data-handling slip becomes **uncapped** liability. | Cap confidentiality-breach liability at a multiple of annual fees (e.g., 2–3x), excluding only willful misconduct/gross negligence. Fallback: super-cap at 3x fees. | [INFERENCIA] |
| 14.1 | **Med** | 60-day non-renewal notice with up to 7% auto-escalation. Miss the window and you are bound to another 12 months at a higher price. | Add a calendar reminder 90 days out; negotiate notice to 30 days and cap escalation at CPI. Fallback: 5% cap. | [DOC] |
| 11 | **Med** | "As soon as practicable" breach notice is vague and likely insufficient for downstream GDPR/HIPAA notification clocks. 30-day return/destruction is acceptable. | Replace with a fixed SLA (e.g., notice within 48–72 hours of discovery). | [DOC] |
| Schedule C | **High (provisional)** | DPA absent — sub-processor, audit, and breach-SLA obligations unknown. | Obtain and review before signing; do not finalize risk ranking without it. | [SUPUESTO → obtain Schedule C from counterparty] |

## High findings — fallback positions confirmed
- 8.4 uncapped confidentiality exposure → 2–3x annual-fee super-cap. [INFERENCIA]
- Missing DPA → condition signature on receipt and review of Schedule C. [SUPUESTO]

## Open `[SUPUESTO]` items (with verification step)
- [SUPUESTO] Schedule C contents → verify by obtaining the executed DPA and
  re-running the confidentiality/data clause analysis.

## Validation gate
- [x] Scope named (DataFlux MSA, Delaware) · [x] all Step-2 checklist clauses
  addressed or N/A · [x] each finding has risk/impact/action/tag · [x] every High
  finding has a fallback · [x] no invented terms · [x] disclaimer verbatim · [x] no
  "compliant" asserted as fact.

**Not legal sign-off** — route the super-cap and DPA conditions to counsel before
counter-signature.
