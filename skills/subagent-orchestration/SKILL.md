---
name: subagent-orchestration
version: 1.2.0
description: "Design deterministic hub-and-spoke subagent orchestration plans with AgentDefinition plus Task dispatch, fresh-session context isolation, typed spoke errors, local recovery, coverage-gap aggregation, and bounded partial-failure behavior."
owner: "JM Labs"
triggers:
  - subagent orchestration
  - hub and spoke
  - coordinator agents
  - error propagation
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Subagent Orchestration

## Purpose

Design deterministic hub-and-spoke coordinators that dispatch isolated subagents via `AgentDefinition` + `Task`, then aggregate typed spoke results without hiding partial failures. Output is an architecture plan, code skeleton, or review packet where context isolation, model/tool assignment, and error propagation are verifiable offline. [DOC]

## When to use vs. skip

- USE when work decomposes into 2+ independent subtasks that benefit from isolated context, distinct tool/model assignment, or parallel fan-out. [DOC]
- SKIP and recommend a single pass (or `prompt-chaining-design`) when subtasks are sequential, share state, or a lone summary/SQL count would do — forcing fan-out onto one task is an anti-pattern the validator rejects as a false positive. [INFERENCIA]
- This is a design/review skill, not a runtime: it produces and validates plans offline; it does not execute spokes. [INFERENCIA]

## Inputs / Outputs

- IN: task description, candidate subtasks, available tools/models, failure tolerance (fail-fast vs. degraded). [DOC]
- OUT: a plan JSON conforming to `assets/orchestration-contract.json`, passing `scripts/validate_orchestration_plan.py`, plus a prose rationale stating whether fan-out is justified. [CONFIG]

## Deterministic Contract

Validate every plan with `scripts/validate_orchestration_plan.py` against `assets/orchestration-contract.json`. A valid plan MUST include: [CONFIG]

- A coordinator that consumes only the final spoke message (`last_message_only`). [CONFIG]
- 2+ spoke definitions, each with `AgentDefinition` fields, minimal tools, an explicit model role, and `Task` dispatch. [CONFIG]
- `fresh_session` context isolation for every spoke. [CONFIG]
- Typed spoke failures: `failure_type`, `attempted_query`, `partial_results`, `suggested_alternatives`. [CONFIG]
- Local recovery (retry / propose alternative) attempted before propagation. [CONFIG]
- Aggregation that continues on partial failure and records explicit `coverage_gaps`. [CONFIG]
- A `valid_empty` result type distinct from `access_failure`. [CONFIG]
- Validation flags: `offline=true`, `network_required=false`, `deterministic=true`. [CONFIG]

## Workflow

1. Confirm independent decomposition; else recommend single pass or `prompt-chaining-design`. [DOC]
2. Define the hub contract: input queue, spoke templates, aggregation shape, coverage-gap shape. [DOC]
3. Define each spoke `AgentDefinition(description, prompt, tools, model)` and its `Task` dispatch; assign the cheapest model that meets the spoke's bar. [INFERENCIA]
4. Enforce `fresh_session` isolation and `last_message_only` consumption. [CONFIG]
5. Define the spoke error contract and local-recovery policy. [DOC]
6. Separate `valid_empty` from `access_failure` explicitly. [CONFIG]
7. Validate offline before presenting the plan as ready. [DOC]

## Output Rules

- Reference `assets/isolation-policy.json`, `assets/error-propagation-policy.json`, `assets/aggregation-policy.json`, `assets/anti-pattern-policy.json`. [CONFIG]
- Gate the plan with the certification bundle `assets/quality-rubric.json` (mirrored by `assets/checklist.md`); see `assets/README.md`. [CONFIG]
- State whether fan-out is justified; never force subagents onto one sequential task. [DOC]
- Never return success with an empty result for an access failure. [DOC]
- Never let one spoke failure abort unrelated spokes unless the user explicitly requires fail-fast. [DOC]
- Never claim parallel execution occurred unless tool results prove it. [DOC]

## Anti-patterns (validator blockers)

- Shared coordinator transcript or mutable scratch object across spokes — breaks isolation. [CONFIG]
- Swallowed errors: catching every exception and returning `success` + `[]`. [CONFIG]
- Fail-fast aggregation aborting all spokes on one failure (unless requested). [CONFIG]
- Missing `Task` dispatch, typed-error fields, local recovery, or `coverage_gaps`. [CONFIG]
- False-positive fan-out on an inherently single-pass task. [CONFIG]

## Edge cases

- 1-of-N spoke failure (e.g. 1 of 50 extractors): hub continues, records the affected unit in `coverage_gaps`, returns partial success. [DOC]
- Spoke returns `[]`: classify as `valid_empty` only if access succeeded; otherwise `access_failure`. [CONFIG]
- All spokes fail: aggregate to a typed failure, not silent empty success. [INFERENCIA]
- User demands fail-fast: honor it, but record which unstarted spokes were skipped. [INFERENCIA]

## Self-correction triggers

Re-open the design if you catch yourself: sharing context to "save tokens"; returning `[]` for an error; aborting siblings on one failure; assigning a tool/model a spoke never uses; or claiming parallelism without proof. Each maps to a named blocker above — fix and re-validate. [INFERENCIA]

## Acceptance gate (done = all true)

- [ ] `validate_orchestration_plan.py` exits 0 on the plan. [CONFIG]
- [ ] `check.sh` passes; flags show `offline/deterministic=true`. [CONFIG]
- [ ] Every spoke: fresh session, minimal tools, explicit model, `Task` dispatch. [CONFIG]
- [ ] Typed errors + local recovery + `coverage_gaps` present. [CONFIG]
- [ ] `valid_empty` ≠ `access_failure`; no swallowed errors; no unjustified fan-out. [CONFIG]

## Example (minimal)

Company enrichment, 3 spokes — `finder`→`extractor`→`ranker`, each `AgentDefinition`+`Task`, fresh session, Haiku for finder/extractor, Sonnet coordinator. One failed `extractor` records `coverage_gaps:[{unit, failure_type:"access_failure", attempted_query, suggested_alternatives}]`; hub still ranks the rest and returns partial success. [INFERENCIA]

## Scripts

```bash
python3 skills/subagent-orchestration/scripts/validate_orchestration_plan.py --input <plan.json>
bash skills/subagent-orchestration/scripts/check.sh
```

The validator is offline and rejects shared context, missing `Task` dispatch, missing typed error fields, missing local recovery, missing coverage gaps, fail-fast aggregation, swallowed errors, and false-positive single-pass plans. [CONFIG]

## Related Skills

- `katas-hub-and-spoke-isolation`
- `katas-multiagent-error-propagation`
- `structured-output-design`
- `prompt-chaining-design`
- `human-escalation-design`
