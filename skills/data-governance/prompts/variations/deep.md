# Deep variation — data-governance (depth=deep)

Exhaustive path. Resolve one topic, load one playbook, apply it fully and verify
at every step.

1. **Resolve topic** with an explicit confidence score and tie-break note.
2. **Load** the single `references/<topic>.md` — still one, never siblings.
3. **Discover** completely: full inventory from source (DDL, catalog, profiling),
   regulatory drivers (retention horizon, residency, regime), all stakeholders.
   Stop with a `[SUPUESTO]` blocker on any missing required input.
4. **Analyze** with the playbook's decision matrix: record the chosen option AND
   the rejected alternative with its trade-off. Examples:
   - privacy → re-identification risk vs utility across the full ladder; tune k/l/t.
   - audit-trail → sync vs async write path against latency/durability.
   - strategy → ETL/ELT, batch/streaming per source; medallion vs mesh.
5. **Execute** the full design; tag every claim.
6. **Validate exhaustively** against the playbook's own quality criteria:
   - privacy → run a re-identification/linkage test before release.
   - audit-trail → replay a window; confirm tamper detection fires on a mutated row.
   - documentation → reconcile doc vs live schema (drift = 0); no "unknown" sources.
   - pipeline → evaluate all four gates; prove a gate rejects a malformed output.
   - strategy/governance → every role assigned to a named person; rules auto-alert.
7. **Decision log**: each material call with rationale, rejected alternative, and
   confidence. Every `[SUPUESTO]` carries a verification step.
