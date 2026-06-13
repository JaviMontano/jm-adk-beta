# Meta prompt — subagent-orchestration

Use this to critique or repair an existing orchestration plan against the
deterministic contract, or to self-check your own draft before the Guardian gate.

## Audit questions

1. **Fan-out justification** — Are there 2+ genuinely independent subtasks, or is
   a single-pass task being forced into spokes? If forced, reject as a false
   positive.
2. **Isolation** — Does any spoke share the coordinator transcript or a mutable
   scratch object? Does the coordinator consume `last_message_only`? Is every
   spoke `fresh_session`?
3. **Dispatch** — Does every spoke use `AgentDefinition` + `Task`? Any spoke
   missing `Task`?
4. **Typed errors** — Do failures carry `failure_type`, `attempted_query`,
   `partial_results`, `suggested_alternatives`? Is `valid_empty` distinct from
   `access_failure`?
5. **Local recovery** — Is retry / alternative attempted before propagation?
6. **Aggregation** — Does a partial failure record `coverage_gaps` and continue?
   Is fail-fast used only when requested, with skipped spokes recorded?
7. **Swallowed errors** — Any catch-all returning `success` + `[]`?
8. **Provisioning** — Any tool or model a spoke never uses?
9. **Flags** — `offline=true`, `network_required=false`, `deterministic=true`?
10. **Governance** — Evidence tags (one family), no invented prices, no client
    PII, single brand?

## Output

For each failed check, name the contract blocker it maps to, propose the minimal
fix, and re-state the corrected fragment. Conclude with PASS / PARTIAL / BLOCK.
