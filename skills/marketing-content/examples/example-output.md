# Example Output — marketing-content

Routed output for the example input (retailer support case study), following
`templates/output.md`.

## 1. Routing decision
- **Request (verbatim):** "Turn this into something our sales team can send to
  prospects" (9d→2.6d resolution, CSAT 3.2→4.5, with a Head-of-Support quote). [EXPLICIT]
- **Resolved topic:** case-study-writing [INFERENCIA]
- **Runner-up considered / rejected:** press-release — no external news hook. [INFERENCIA]
- **Depth:** quick [CONFIG]
- **Brand (single):** MetodologIA [EXPLICIT]
- **Playbook loaded:** references/case-study-writing.md (only) [CONFIG]

## 2. Discover (inputs gathered)
| Required input | Value | Status |
|----------------|-------|--------|
| Baseline / before metric | 9d resolution; CSAT 3.2 | provided [EXPLICIT] |
| After metric | 2.6d resolution; CSAT 4.5 | provided [EXPLICIT] |
| Verbatim quote | "We finally got ahead of it." — Head of Support | `[NEEDS APPROVAL]` |
| Client identity | Regional retailer | anonymize to role+industry |

## 3. Delegated artifact (case study)
**Headline:** Cut support resolution from 9 days to 2.6 days in one quarter [EXPLICIT]

**Snapshot:** Regional retailer, customer-support operations; hero number —
71% faster ticket resolution. [EXPLICIT]

**Problem:** Tickets aged 9 days on average; CSAT sat at 3.2 and churn risk was
climbing. [EXPLICIT]

**Solution:** Triage automation plus tiered routing. Full rip-and-replace was
rejected as too slow to show quarter-level impact. [INFERENCIA]

**Result:** Resolution 9d → 2.6d; CSAT 3.2 → 4.5 over one quarter. [EXPLICIT]
> "We finally got ahead of it." — Head of Support `[NEEDS APPROVAL]`

**CTA:** Book a 20-minute support-operations assessment. [EXPLICIT]

## 4. Validation result (guardian gates)
- **Gate 1 Routing:** one playbook ✓ · topic matches output ✓ · depth honored ✓
- **Gate 2 Topic criteria:** business-outcome hero metric w/ before/after ✓ ·
  metrics source-traceable ✓ · verbatim quote present ✓ (approval pending) ·
  scannable in <30s ✓
- **Gate 3 Governance:** tags ✓ · no invented prices ✓ · no unsourced
  superlatives ✓ · single-brand ✓ · client anonymized, no PII ✓

## 5. Open items before publish
- Quote approval not on file → held as `[NEEDS APPROVAL]`; do not publish until
  cleared. [DOC]

**Verdict:** dod=hold (publishing blocked on quote approval). Routing and
structure pass; this is a true case study, not a testimonial, because both
before-numbers are sourced. [INFERENCIA]
