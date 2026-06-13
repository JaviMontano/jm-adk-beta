# Acceptance checklist — subagent-orchestration

Legible mirror of `assets/quality-rubric.json`. Use it to validate a hub-and-spoke
orchestration plan by hand, or as the validation section of the deliverable
(`templates/output.md`). Every box must be checked for a PASS. [CONFIG]

## Decomposition

- [ ] Fan-out is justified: 2+ genuinely independent subtasks (no single-pass task forced into spokes).

## Isolation

- [ ] Every spoke runs in `fresh_session`.
- [ ] No shared coordinator transcript or mutable scratch object across spokes.
- [ ] Coordinator consumes `last_message_only`.

## Dispatch & provisioning

- [ ] Each spoke declares `AgentDefinition(description, prompt, tools, model)`.
- [ ] Each spoke is dispatched via `Task`.
- [ ] No tool or model a spoke does not use; cheapest model that clears the bar.

## Error contract

- [ ] Failures carry `failure_type`, `attempted_query`, `partial_results`, `suggested_alternatives`.
- [ ] `valid_empty` is distinct from `access_failure`.
- [ ] No `success` + `[]` returned for an access failure.
- [ ] Local recovery (bounded retry / alternative) attempted before propagation.

## Aggregation

- [ ] Continue-on-partial-failure with explicit `coverage_gaps`.
- [ ] Fail-fast used only when requested; skipped spokes recorded.
- [ ] All-spokes-fail aggregates to a typed failure, not a silent empty.

## Flags & governance

- [ ] `offline=true`, `network_required=false`, `deterministic=true`.
- [ ] Evidence tags present (one family); no invented prices; no client PII; single brand.
