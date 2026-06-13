# Support — subagent-orchestration

## Mandate

Materialize the orchestration design into the concrete deliverable: a plan JSON
conforming to `assets/orchestration-contract.json`, the prose rationale, and (when
requested) the coordinator/spoke code skeleton. Support executes the spine; it
does not decide fan-out (Lead) or certify (Guardian). [DOC]

## Execution steps

1. **Render the hub.** Coordinator that consumes `last_message_only`, an input
   queue, the aggregation block, and the `coverage_gaps` block. [CONFIG]
2. **Render each spoke.** `AgentDefinition(description, prompt, tools, model)` +
   `Task` dispatch, `fresh_session` flag, and the typed-error fields. [CONFIG]
3. **Wire aggregation.** Continue-on-partial-failure by default: on a spoke
   failure, record the unit in `coverage_gaps` and keep processing siblings.
   Fail-fast only if Lead set it, and then list skipped spokes. [CONFIG]
4. **Write the rationale.** State plainly whether fan-out is justified and why,
   mapping each spoke to an independent subtask. [DOC]
5. **Set validation flags.** `offline=true`, `network_required=false`,
   `deterministic=true`. [CONFIG]

## Output rules

- Reference the four policy assets (`isolation`, `error-propagation`,
  `aggregation`, `anti-pattern`). [CONFIG]
- Never emit `success` + `[]` for an access failure. [DOC]
- Never claim parallel execution occurred — this is a plan, not a run. [DOC]
- Keep the plan lean: no tool/model a spoke does not use. [INFERENCIA]

## Handoff

→ **Guardian** with the plan JSON, the rationale, and the policy references
attached, ready for the acceptance gate. Never mark done before the gate. [DOC]

## Evidence

Tag construction choices `[CÓDIGO]`/`[CONFIG]`/`[DOC]`/`[INFERENCIA]`/`[SUPUESTO]`,
one family per output. [DOC]
