<!-- distilled from alfa skills/subagent-monitor -->
<!-- > -->
# Subagent Monitor
> "Method over hacks."
## TL;DR
Track subagent execution with a deterministic timeout policy, typed results, partial-failure aggregation, evidence tags, and offline validation — so a swarm result is reproducible and never reports false success.

## Deterministic Contract

Use `assets/subagent-monitor-report-contract.json` and validate reports with `scripts/validate_subagent_monitor_report.py`. A valid report must include:

- Stable `swarm_id` and task summary.
- Agent registry with deterministic roles and status values.
- Timeout policy that is bounded, monotonic, and not based on wall-clock evidence (wall-clock is non-reproducible across hosts and replays) [EXPLICIT].
- One typed result per agent with `agent_id`, `status`, `result_type`, evidence tag, and optional error.
- Aggregation policy that preserves blockers and partial failures instead of reporting success silently.
- Evidence entries with approved tags and source.
- Validation checks for assets, deterministic scripts, quality criteria, timeout policy, typed results, aggregation policy, partial failure handling, and evidence.

### Status & result_type vocabulary
Fix the enums so aggregation is deterministic [EXPLICIT]:
- `status`: `pending` → `running` → one of `done` | `failed` | `timeout` | `skipped`. No other terminal value.
- `result_type`: `data` | `decision` | `artifact` | `noop`. Drives how aggregation consumes the payload.
- Aggregate rollup precedence (worst-wins): `failed`/`timeout` > `blocked` > `warning` > `done`. A single blocker MUST surface in the swarm status [INFERENCE].

## Procedure
### Step 1: Discover
- Gather agent list, task contract, timeout budget, and expected result types.
### Step 2: Analyze
- Identify timeout and partial-failure policy before dispatch.
### Step 3: Execute
- Track sequence-based start/completion, collect typed results, and record errors.
### Step 4: Validate
- Run the offline report validator before accepting the aggregate result.

## Worked Example (minimal report)
```json
{
  "swarm_id": "swarm-2026-001",
  "task": "extract + verify claims",
  "timeout_policy": {"unit": "steps", "budget": 50, "monotonic": true},
  "results": [
    {"agent_id": "extractor", "status": "done", "result_type": "data", "evidence": "[DOC]"},
    {"agent_id": "verifier", "status": "timeout", "result_type": "noop", "evidence": "[INFERENCE]",
     "error": "budget_exhausted"}
  ],
  "aggregate": {"status": "timeout", "blockers": ["verifier"], "coverage": "1/2"}
}
```
Rollup is `timeout` (not `done`) because worst-wins precedence surfaces the `verifier` blocker [EXPLICIT].

## Quality Criteria
- [ ] Evidence tags applied
- [ ] Timeout policy is bounded and non-silent
- [ ] Every agent has exactly one typed result (no missing, no duplicate)
- [ ] Aggregation status reflects blockers, warnings, and coverage gaps
- [ ] Offline validator passes

## Usage

Example invocations:

- "/subagent-monitor" — Run the full subagent monitor workflow
- "subagent monitor on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Anti-scope: does NOT dispatch, schedule, or kill agents — it tracks and validates their reported state only [EXPLICIT]
- Anti-scope: not a live dashboard; operates on completed/streamed reports, not real-time wall-clock telemetry [EXPLICIT]
- Timeout budget is step/sequence-based, so it cannot detect a hung agent that never emits a step [INFERENCE]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Agent emits two results | Reject report; "exactly one typed result" is violated [EXPLICIT] |
| Agent never reports (silent drop) | Mark `timeout`/`failed`; never count as `done` [EXPLICIT] |
| All agents `skipped` | Aggregate is `blocked` with zero coverage, not `done` [INFERENCE] |
| Evidence tag missing/foreign | Validator fails; only approved tags are accepted [CONFIG] |
| Timeout policy references wall-clock | Validator fails; require bounded monotonic budget [EXPLICIT] |
