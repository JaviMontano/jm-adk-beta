# Deep Variation — Multi-Source Verification with Conflict Resolution

For high-impact decisions resting on several claims, where official sources may disagree
and version currency is contested.

## Use when

- A migration, ADK adapter change, or spec interpretation drives code/architecture edits.
- Multiple official sources (vendor doc + spec, or two doc versions) must be reconciled.
- The decision warrants explicit corroboration and a recorded conflict trail.

## Procedure

1. **Decompose** the decision into every distinct claim it rests on; list them before
   fetching.
2. **Map the authority surface**: identify each producer's canonical doc and the spec that
   governs the contested behavior.
3. **Fetch each official source** (`WebSearch` → `WebFetch`); record `url`,
   `accessed_date`, `publisher`, `official`, `role`, and a passage extract per source.
4. **Anchor version**: pin `repo_version`; mark any doc from a different major as
   `unverified` with a version-conflict note.
5. **Cross-check claims**: each claim needs ≥1 official source; high-impact claims need a
   second official corroboration.
6. **Resolve priority** official > vendor > spec > repo > secondary. Where the spec is more
   correct than a vendor doc on a contested point, prioritize the spec and record why.
7. **Record conflicts**: any genuine official-vs-official contradiction goes to
   `blocking_gaps` unresolved.
8. **Decide and gate**: `change_authorized=true` only with all supporting claims
   `verified` and no open gaps; otherwise `blocked`.

## Output

Full report per `templates/output.md`, JSON when contracted. Validate offline with
`scripts/validate_official_source_verifier.py`; run `scripts/check.sh` for the smoke.

## Discipline

Every claim, source, and conflict carries a provenance tag. Never elevate a secondary
source. Default `unverified` under doubt. Green is never success by default. Single brand;
no invented prices; no client PII.
