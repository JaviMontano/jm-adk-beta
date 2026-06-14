# Quick variation — subagent-orchestration

Fast path: produce the **minimal valid plan** against
`assets/orchestration-contract.json`. No exhaustive narrative.

1. One line: is fan-out justified (2+ independent subtasks)? If not, route to
   `prompt-chaining-design` or a single pass and stop.
2. List spokes as `AgentDefinition(description, prompt, tools, model)` + `Task`,
   each `fresh_session`, cheapest model, minimal tools.
3. Coordinator consumes `last_message_only`.
4. Error contract one-liner: typed fields + `valid_empty` ≠ `access_failure`.
5. Aggregation: continue-on-partial-failure with `coverage_gaps`.
6. Set `offline=true`, `network_required=false`, `deterministic=true`.

Skip deep rationale; still never emit `success` + `[]` for an access failure, and
still tag claims with one evidence family.
