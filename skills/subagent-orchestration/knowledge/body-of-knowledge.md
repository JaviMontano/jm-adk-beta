# Body of Knowledge — subagent-orchestration

Domain knowledge for designing deterministic hub-and-spoke subagent
orchestration plans. Evidence taxonomy: `[CÓDIGO] [CONFIG] [DOC] [INFERENCIA]
[SUPUESTO]`. [DOC]

## Key concepts

- **Hub (coordinator).** The single agent that dispatches spokes and aggregates
  their results. It consumes only each spoke's final message
  (`last_message_only`) — never the spoke's full transcript — so coordinator
  context stays bounded regardless of spoke chatter. [CONFIG]
- **Spoke.** An isolated subagent defined by `AgentDefinition(description,
  prompt, tools, model)` and dispatched via `Task`. Each spoke owns one
  independent subtask. [CONFIG]
- **Fresh-session isolation.** Every spoke runs in its own `fresh_session` with
  no shared transcript and no mutable scratch object. Isolation is the property
  that makes spokes independently reasoned-about and safely parallelizable. [CONFIG]
- **Typed spoke failure.** A failure object carrying `failure_type`,
  `attempted_query`, `partial_results`, and `suggested_alternatives` — replacing
  a bare exception or an empty list. [CONFIG]
- **Coverage gaps.** The explicit record of which units a degraded run could not
  cover, attached to a partial-success aggregation. [CONFIG]
- **`valid_empty` vs `access_failure`.** Two distinct result types: a query that
  reached its source and legitimately found nothing (`valid_empty`) versus a
  query that could not reach its source (`access_failure`). Collapsing both to
  `[]` is the canonical bug this skill prevents. [CONFIG]

## Standards and contracts

- A plan is valid only against `assets/orchestration-contract.json`, checked by
  `scripts/validate_orchestration_plan.py` offline. [CONFIG]
- Four policy assets bind the design: `isolation-policy`,
  `error-propagation-policy`, `aggregation-policy`, `anti-pattern-policy`. [CONFIG]
- Validation flags must read `offline=true`, `network_required=false`,
  `deterministic=true`. A plan that needs the network to validate is not a
  deterministic plan. [CONFIG]

## Decision rules

1. **Fan-out gate.** Design spokes only when 2+ subtasks are genuinely
   independent. Sequential or shared-state work → `prompt-chaining-design`; a lone
   summary / count → single pass. [INFERENCIA]
2. **Model floor.** Assign the cheapest model tier that clears the spoke's bar;
   never provision a model (or tool) a spoke does not use. [INFERENCIA]
3. **Recovery-before-propagation.** A spoke retries or proposes an alternative
   locally before surfacing a typed failure to the hub. [DOC]
4. **Continue-on-partial-failure by default.** One spoke failing records a
   `coverage_gaps` entry and lets siblings finish. Fail-fast is opt-in and must
   record skipped spokes. [CONFIG]
5. **No false success.** Never return `success` with `[]` for an access failure;
   aggregate all-spokes-failed to a typed failure, not a silent empty. [CONFIG]

## Anti-patterns (contract blockers)

- Shared coordinator transcript or mutable scratch object across spokes. [CONFIG]
- Swallowed errors: catch-all returning `success` + `[]`. [CONFIG]
- Fail-fast aggregation aborting unrelated spokes without an explicit request. [CONFIG]
- Missing `Task` dispatch, typed-error fields, local recovery, or
  `coverage_gaps`. [CONFIG]
- False-positive fan-out on an inherently single-pass task. [INFERENCIA]
- Claiming parallel execution occurred when only a plan exists. [DOC]

## Worked edge cases

- **1-of-50 extractor fails:** hub continues, records the affected document in
  `coverage_gaps`, returns partial success. [DOC]
- **Spoke returns `[]`:** classify `valid_empty` only if access succeeded; else
  `access_failure`. [CONFIG]
- **All spokes fail:** typed aggregate failure, not silent empty. [INFERENCIA]
- **User demands fail-fast:** honor it, but list the unstarted/skipped spokes. [SUPUESTO]
