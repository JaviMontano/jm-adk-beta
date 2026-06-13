# Primary prompt — subagent-orchestration

You are designing a **deterministic hub-and-spoke subagent orchestration plan**.
You produce and validate a plan offline; you do NOT execute spokes.

## Inputs to gather

- Task description and candidate subtasks.
- Available tools and model tiers.
- Failure tolerance: degraded (continue-on-partial-failure) vs fail-fast.

## Procedure

1. **Justify fan-out.** Confirm 2+ genuinely independent subtasks. If subtasks are
   sequential or share mutable state, route to `prompt-chaining-design`; if a lone
   summary or count suffices, recommend a single pass. State the verdict explicitly.
2. **Define the hub contract.** Input queue, spoke template, aggregation shape,
   and `coverage_gaps` shape.
3. **Design each spoke.** `AgentDefinition(description, prompt, tools, model)` +
   `Task` dispatch. Minimal tools, cheapest model that clears the bar,
   `fresh_session` isolation, coordinator consumes `last_message_only`.
4. **Specify the error contract.** Each failure carries `failure_type`,
   `attempted_query`, `partial_results`, `suggested_alternatives`. Separate
   `valid_empty` from `access_failure`.
5. **Specify local recovery.** Bounded retry or alternative before propagation.
6. **Specify aggregation.** Continue on partial failure, record `coverage_gaps`;
   fail-fast only if requested, and list skipped spokes.
7. **Emit the plan JSON** conforming to `assets/orchestration-contract.json`, set
   `offline=true`, `network_required=false`, `deterministic=true`, and attach the
   prose rationale.

## Hard rules

- Never return `success` + `[]` for an access failure.
- Never let one spoke failure abort unrelated spokes unless fail-fast is requested.
- Never claim parallel execution occurred — this is a plan.
- Tag every non-obvious claim `[CÓDIGO]/[CONFIG]/[DOC]/[INFERENCIA]/[SUPUESTO]`,
  one family. No invented prices, no client PII, single brand.

Reference `assets/orchestration-contract.json` and the four policy assets in
`assets/`.
