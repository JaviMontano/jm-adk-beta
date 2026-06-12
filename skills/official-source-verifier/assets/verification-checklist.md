# Verification Pre-Delivery Checklist

Run every item before delivering an official-source verification report. Any unchecked
blocking item forces status `fail` or `blocked` — not `pass`.

## Sources

- [ ] Every source has `url`, `publisher`, `accessed_date` (ISO `YYYY-MM-DD`), `source_type`. [CONFIG]
- [ ] Every `accessed_date` is real and not in the future. [CONFIG]
- [ ] Secondary sources are tagged `official=false`, `role=lead`. [DOC]
- [ ] Each official source's cited URL is the text actually fetched (not a snippet). [DOC]

## Claims

- [ ] Every claim has non-empty `official_source_ids`, or is explicitly `unverified`. [DOC]
- [ ] No `official=false` source is the sole evidence of a `verified` claim. [DOC]
- [ ] No claim is `verified` without a fetched official passage behind it. [INFERENCIA]
- [ ] Cross-major / wrong-version docs are marked `unverified` with a version-conflict note. [INFERENCIA]

## Priority & conflict

- [ ] Priority order official > vendor > spec > repo > secondary applied. [DOC]
- [ ] Any official-vs-official contradiction recorded in `blocking_gaps`, not resolved silently. [INFERENCIA]

## Decision

- [ ] `change_authorized=true` only if all supporting claims are `verified`. [DOC]
- [ ] `justified_change` names the exact change the finding authorizes (or why none). [DOC]
- [ ] Non-empty `blocking_gaps` forces status ≠ `pass`. [DOC]

## Governance

- [ ] Every source, claim, and verdict carries a provenance tag. [DOC]
- [ ] Single brand (JM Labs); no invented prices; no client PII. [SUPUESTO]
- [ ] Green is earned by evidence, not assumed. [SUPUESTO]
