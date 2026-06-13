# Example output — ux-research

> Route: `user-research` · Depth: `deep` · Date: 2026-06-12

## 1. Decision & objective
- **Decision this informs:** whether the invoicing redesign prioritizes the
  `payment-submit` experience and which friction to target first. [DOC]
- **Objective / question:** "Why do AP clerks abandon at payment-submit?" [EXPLICIT]
- **In scope:** generative interviews, personas, journey map. **Out of scope:**
  A/B test design, the build itself, requirement specs (hand to requirements). [DOC]

## 2. Scope & method
- **Segment:** AP clerks at mid-market B2B customers; recruited across 3 accounts. [DOC]
- **Method:** 6 moderated interviews + funnel analytics review. New themes stopped
  appearing by interview 5 (saturation). [INFERENCIA]
- **Sources:** interviews INT-01…INT-06; analytics export `payment-submit` 90-day.
  No client names or invoice data carried into this report (PII redacted). [CONFIG]

## 3. Synthesis (persona + empathy + journey)
**Persona — "Marta, AP clerk" (provisional → confirmed by INT-02/04/05).**
Goal: close month-end fast. Frustration: re-keying rejected invoices. [DOC]

**Empathy quadrants:**
- Say: "I trust the system." Do: exports to a spreadsheet to double-check totals.
  → **Say-vs-Do gap** is itself the finding: the trust claim is not behavioral. [INFERENCIA]

**Journey — moment of truth = `payment-submit`.** Sentiment dips +2 → −3 at
submit, driven by unclear fee breakdown and no save-draft on rejection. [DOC]

## 4. Findings & opportunities
| # | Finding | Evidence | Severity | Opportunity | Owner |
|---|---------|----------|----------|-------------|-------|
| 1 | Fees unclear at submit; clerks distrust the total | INT-02, INT-05 quotes + spreadsheet workaround | Major | Inline fee preview before submit | Design lead |
| 2 | Rejected invoice loses entered data | INT-04; analytics 38% drop | Blocker | Autosave draft on rejection | Eng lead |
| 3 | "Trust" is stated, not behavioral | Say-vs-Do gap, 4/6 interviews | Minor | Verify with post-launch CES | Research |

## 5. Open assumptions (`[SUPUESTO]` register)
| Assumption | Why uncertain | Verification step |
|------------|---------------|-------------------|
| Inline fee preview will lift completion | not yet tested with users | prototype + usability test (route: prototyping → user-testing) |
| Marta generalizes beyond these 3 accounts | only 3 accounts sampled | widen recruitment or run a confirmatory survey |

## 6. Validation gate
- [x] Exactly one playbook read (`user-research`)
- [x] Personas research-backed, source per attribute; all four empathy quadrants
- [x] Journey includes a negative-sentiment stage; opportunities owned
- [x] Each `[SUPUESTO]` paired with a verification step
- [x] One tag family (Alfa-core); no green-as-success; no PII; single brand

**Status:** `conditional` — findings are solid but desirability of fixes is
unverified until the prototype + test sub-pass runs. [SUPUESTO]
**Next step:** Design lead builds a clickable mockup of inline-fee-preview;
hand to the `prototyping` then `user-testing` routes before committing the
redesign sprint. [DOC]
