# subagent-orchestration

## What it does

Designs and reviews **deterministic hub-and-spoke subagent orchestration plans**.
Given a task that decomposes into independent subtasks, it produces an
architecture plan (or code skeleton / review packet) where a coordinator
dispatches isolated spokes via `AgentDefinition` + `Task`, then aggregates typed
spoke results without hiding partial failures. Every property — context
isolation, model/tool assignment, error propagation — is verifiable **offline**.
[DOC]

## When to use

- USE when work splits into **2+ independent subtasks** that benefit from
  isolated context, distinct tool/model assignment, or parallel fan-out. [DOC]
- SKIP (route to `prompt-chaining-design` or a single pass) when subtasks are
  sequential, share mutable state, or a lone summary / SQL count would do. Forcing
  fan-out onto a single-pass task is a false positive the contract rejects. [INFERENCIA]
- This is a **design/review skill, not a runtime** — it emits and validates plans
  offline; it never executes spokes. [INFERENCIA]

## How it routes / executes

1. **Lead** confirms independent decomposition; else routes away. Defines the hub
   contract (input queue, spoke templates, aggregation shape, coverage-gap shape).
2. **Specialist** sizes each spoke: `AgentDefinition(description, prompt, tools,
   model)` with the cheapest model meeting the bar, and the typed-error / local
   recovery policy.
3. **Support** materializes the plan JSON against
   `assets/orchestration-contract.json` and the four policy assets, plus the prose
   rationale stating whether fan-out is justified.
4. **Guardian** runs the acceptance gate: fresh-session isolation, `Task`
   dispatch, typed errors, local recovery, `coverage_gaps`, `valid_empty` ≠
   `access_failure`, no swallowed errors, no unjustified fan-out, and the offline
   / deterministic flags. [CONFIG]

## Deterministic backbone

A valid plan validates against `assets/orchestration-contract.json` and must
satisfy the four policy assets:

- `assets/isolation-policy.json` — `fresh_session` per spoke, coordinator
  consumes `last_message_only`.
- `assets/error-propagation-policy.json` — typed failures (`failure_type`,
  `attempted_query`, `partial_results`, `suggested_alternatives`),
  `valid_empty` ≠ `access_failure`.
- `assets/aggregation-policy.json` — continue-on-partial-failure with explicit
  `coverage_gaps`; fail-fast only when the user demands it.
- `assets/anti-pattern-policy.json` — shared context, swallowed errors,
  unjustified fan-out, missing `Task` / recovery / gaps.

## References

This skill ships its contract and policies as data assets (see `assets/`) rather
than prose playbooks. The authoritative spec lives in `SKILL.md`; the domain
model lives in `knowledge/body-of-knowledge.md` and
`knowledge/knowledge-graph.json`.

## Related skills

`prompt-chaining-design` · `structured-output-design` · `human-escalation-design`
· `katas-hub-and-spoke-isolation` · `katas-multiagent-error-propagation`
