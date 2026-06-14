# <Deliverable title> — docs-writing output

> Fill this scaffold from the routed playbook. Keep one evidence-tag family. Replace
> every angle-bracket field; do not ship placeholders.

## Routing record

- **Topic:** `<one of the 13 enum values>` [CONFIG]
- **Playbook read:** `references/<topic>.md` (exactly one) [CONFIG]
- **Depth:** `<quick | deep>` [CONFIG]
- **Brand:** `<single brand>` [DOC]

## 1. Discover

- **Sources inventoried:** `<code / PRs / prior docs / transcript / release diff>` [CÓDIGO|CONFIG]
- **Audience:** `<who reads this and why>` [DOC]
- **Gaps:** `<each gap as [SUPUESTO] + the step that confirms it>` [SUPUESTO]

## 2. Analyze

- **Approach chosen:** `<e.g. code-first OpenAPI / category-grouped changelog>` [INFERENCIA]
- **Trade-off accepted:** `<the cost taken, not just the winner>` [INFERENCIA]

## 3. Execute — deliverable body

> Structure this section per the routed playbook. Examples by route:
> - api-documentation → endpoint reference + error-code catalog (≥1 success + ≥1 error example each)
> - changelog-writing → Security→Removed→Changed→Added→Fixed groups + migration notes
> - internal-memo → Subject · BLUF · Context · Options+Recommendation · Action items
> - developer-onboarding → dependency-ordered checklist + buddy/mentor + ramp metrics

`<deliverable content here, every non-obvious claim tagged>`

## 4. Validate — acceptance gate

| Quality criterion (from routed playbook) | Status | Evidence |
|------------------------------------------|--------|----------|
| `<criterion 1>` | PASS / BLOCK | `<how verified>` |
| `<criterion 2>` | PASS / BLOCK | `<how verified>` |
| Evidence tags: one family, all `[SUPUESTO]` paired with a check | PASS / BLOCK | `<...>` |
| Governance: no invented prices, no PII, single brand | PASS / BLOCK | `<...>` |

## Guardian verdict

`<PASS — all gates evidenced | BLOCK — failing gate + defect + fix owner>` [DOC]
