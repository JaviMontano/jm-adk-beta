# marketing-content — Routing & Delivery Output

## 1. Routing decision
- **Request (verbatim):** <what the user asked> [EXPLICIT]
- **Resolved topic:** <one of the 8 enum values> [INFERENCIA]
- **Runner-up considered / rejected:** <topic + one-line reason, or "none"> [INFERENCIA]
- **Depth:** quick | deep [CONFIG]
- **Brand (single):** MetodologIA [EXPLICIT]
- **Playbook loaded:** references/<topic>.md (exactly one) [CONFIG]

## 2. Discover (inputs gathered)
| Required input (per playbook) | Value | Status |
|-------------------------------|-------|--------|
| <e.g. audience / CTA / baseline metric / spokesperson> | <value> | provided / `[NEEDS APPROVAL]` / `[SUPUESTO]` |

Open gaps / questions asked: <list, or "none">

## 3. Delegated artifact
> Produced strictly by the resolved playbook in its canonical structure.
> Every claim carries a tag ([EXPLICIT]/[DOC]/[INFERENCIA]/[SUPUESTO]).

<artifact body — case study, calendar, copy, PR, shot list, run-of-show, etc.>

## 4. Validation result (guardian gates)
- **Gate 1 Routing:** one playbook loaded ☐ · topic matches output ☐ · depth honored ☐
- **Gate 2 Topic criteria:** <list the resolved playbook's acceptance items, each ✓/✗>
- **Gate 3 Governance:** tags ☐ · no invented prices ☐ · no unsourced superlatives ☐ · single-brand ☐ · no PII ☐ · `[SUPUESTO]`/`[NEEDS APPROVAL]` resolved or disclosed ☐

## 5. Open items before publish
- <placeholders, unverified stats, pending approvals — or "none; cleared">

**Verdict:** dod=pass only if all three gates clear; otherwise list the failing
checks and the exact fix required.
