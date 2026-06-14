# Official Source Verification Report

- **Question**: <the concrete decision that depends on external authority>
- **Status**: `pass` | `fail` | `blocked`
- **Repo version under decision**: <e.g. gh 2.x / ADK vX / n/a>
- **Output mode**: JSON contract | human-readable
- **Date of verification**: <YYYY-MM-DD>

## Source registry

| source_id | source_type | publisher | url | accessed_date | official | role |
|-----------|-------------|-----------|-----|---------------|----------|------|
| <id>      | spec/doc/manual/blog/issue | <publisher> | <url> | <YYYY-MM-DD> | true/false | authority/lead |

## Claims

| claim_id | statement | source_ids | official_source_ids | status | tag |
|----------|-----------|-----------|---------------------|--------|-----|
| <id>     | <verifiable statement> | <ids> | <official ids> | verified/unverified | [DOC]/[INFERENCIA] |

For each claim, include a short extract or paraphrase of the official passage that
supports or contradicts it.

## Priority & conflicts

- Priority order applied: official > vendor > spec > repo > secondary.
- Conflicts between official sources (if any): <description → recorded in blocking_gaps>.
- Version-currency findings: <doc version vs repo version>.

## Decision

- **change_authorized**: true | false
- **justified_change**: <the exact change this verified finding authorizes, or why none>
- **scope**: <files/criteria the change touches>
- **blocking_gaps**: <non-empty list forces status ≠ pass; empty if none>

## Self-correction log

- <any claim degraded to unverified, missing date demanded, conflict opened, etc.>

## Acceptance gate

- [ ] Every source has url, publisher, accessed_date (ISO), source_type.
- [ ] Every claim has non-empty official_source_ids or is marked unverified.
- [ ] No `official=false` source is sole evidence of a `verified` claim.
- [ ] `change_authorized=true` only if all supporting claims are `verified`.
- [ ] Non-empty `blocking_gaps` forces status ≠ pass.
- [ ] When required, report passes `scripts/check.sh`.

Single brand (JM Labs); no invented prices; green is not success by default; no client PII.
