# Deep variation — subagent-orchestration

Exhaustive path: design AND verify every property, then dry-run the edge cases.

1. **Decomposition proof.** Map each candidate subtask to an independence
   argument. Reject any spoke whose input depends on another spoke's output
   (that is chaining, not fan-out). State the fan-out verdict with evidence tags.
2. **Hub contract.** Fully specify input queue, spoke template, aggregation
   shape, and `coverage_gaps` shape.
3. **Per-spoke design.** For each: `AgentDefinition(description, prompt, tools,
   model)`, `Task` dispatch, model-tier justification (cheapest clearing the bar),
   tool-minimality justification, `fresh_session`.
4. **Error contract.** Specify `failure_type`, `attempted_query`,
   `partial_results`, `suggested_alternatives`; define the `valid_empty` vs
   `access_failure` decision boundary precisely.
5. **Local recovery.** Retry caps and alternative-proposal logic per spoke.
6. **Aggregation.** Continue-on-partial-failure; degraded-vs-fail-fast policy;
   skipped-spoke recording.
7. **Edge-case dry run.** Walk: 1-of-N failure; spoke returns `[]`; all spokes
   fail; user demands fail-fast. Show the expected aggregation outcome for each.
8. **Self-correction sweep.** Check each named contract blocker; fix and
   re-validate.
9. **Validate.** Confirm the plan passes `validate_orchestration_plan.py` and the
   flags read `offline/deterministic=true`. Attach the rationale.

Every non-obvious claim tagged with one evidence family; no invented prices, no
client PII, single brand.
