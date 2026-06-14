<!-- distilled from alfa skills/health-check-automation -->
<!-- > -->
# Health Check Automation

> "Method over hacks."

## TL;DR

Use this skill when a project needs a deterministic health-check plan, status
snapshot, dependency monitor, resource threshold policy, or alert handoff.
[EXPLICIT]

The output must separate observed health from inferred risk, name every check,
bind each check to an offline-verifiable threshold where possible, and define
alert routing plus degradation behavior before claiming the system is healthy.
[EXPLICIT]

Deterministic means: re-running the classifier over the same captured evidence
yields the same status, with no network, wall-clock, or random dependency. Live
probing is out of scope; this skill plans and grades checks, it does not run
them. [EXPLICIT]

## Procedure

### Step 1: Inventory Health Surface

- Identify services, dependencies, jobs, storage, queues, credentials,
  scheduled tasks, and resource limits that belong in the health surface.
- Record which signals are observed, synthetic, or unavailable.
- Anti-scope: do not invent signals the caller cannot supply evidence for; list
  them as `unknown` gaps instead of fabricating values. [EXPLICIT]

### Step 2: Define Deterministic Checks

- Use `assets/health-check-contract.json` for required output fields.
- Use `assets/service-policy.json`, `assets/dependency-policy.json`, and
  `assets/resource-policy.json` to define status, severity, threshold, and
  evidence requirements.
- Avoid live network assumptions unless the caller supplies captured evidence.
- State threshold direction explicitly (e.g. `>=` for latency/usage, `<=` for
  free disk) so `warn`/`fail` boundaries are unambiguous and reproducible.
- Each check carries: `id`, `target`, `observed_value`, `threshold`, `severity`,
  `evidence` (source + capture time), and `status`. Missing any required field
  forces `unknown`, never `pass`. [EXPLICIT]

### Step 3: Classify Status And Alerts

- Classify each check as `pass`, `warn`, `fail`, or `unknown`.
- Use `assets/alert-policy.json` to map severity, owner, trigger, and handoff.
- Use `assets/degradation-policy.json` when any required check is unavailable,
  stale, or failing.
- Overall rollup precedence (strictest wins): any required `fail` -> `unhealthy`;
  any required `unknown`/stale -> `degraded` (not healthy); any `warn` ->
  `degraded`; all required `pass` with evidence -> `healthy`. An optional check
  rolls up only if its policy marks the failure service-affecting. [EXPLICIT]

### Step 4: Validate And Handoff

- Validate structured JSON health reports with
  `scripts/validate_health_check.py` or `scripts/check.sh`.
- Mark overall status `healthy` only when all required checks pass and evidence
  is present.
- Record residual risk for skipped optional checks or stale snapshots.
- Handoff is ready only when: schema validates, every check has dated evidence,
  every alert has an owner + route, and the rollup decision is reproducible from
  the artifact alone. Block handoff otherwise. [EXPLICIT]

## Quality Criteria

- [ ] Health surface is explicit and scoped.
- [ ] Required checks have deterministic thresholds (value, direction, units).
- [ ] Dependencies include owner, expected status, and failure behavior.
- [ ] Resource checks include units, warning thresholds, critical thresholds,
  and observed values.
- [ ] Alerts include severity, owner, trigger, and handoff evidence.
- [ ] Unknown or stale evidence cannot produce an overall healthy decision.
- [ ] Rollup precedence is applied and the overall status is reproducible.
- [ ] Evidence tags are applied to user-facing factual claims.

## Worked Example

Input evidence: API `p95_latency_ms=420` captured `2026-06-11T09:00Z`; Postgres
dependency `status=up`; disk `free_pct=8`; cache check has no snapshot.

- `api-latency`: threshold `warn >= 300`, `fail >= 800` -> observed 420 ->
  `warn`. [EXPLICIT]
- `db-postgres` (required): up, owner present -> `pass`. [EXPLICIT]
- `disk-free`: threshold `warn <= 15`, `fail <= 10` -> observed 8 -> `fail`,
  severity critical, routed to on-call owner. [EXPLICIT]
- `cache-hit`: no evidence -> `unknown`. [EXPLICIT]
- Rollup: a required `fail` (disk) exists -> overall `unhealthy`; handoff blocked
  until disk is remediated and cache evidence supplied. [EXPLICIT]

## Usage

Example invocations:

- "/health-check-automation" - Build a deterministic health-check plan.
- "Create health checks for this service and its dependencies."
- "Validate this health report JSON before marking the release healthy."
- "Design alerts for resource usage and degraded dependency status."

## Assumptions & Limits

- Assumes access to project artifacts, supplied telemetry, or captured health
  snapshots. [EXPLICIT]
- Requires English-language output unless otherwise specified. [EXPLICIT]
- Does not perform live monitoring by itself. [EXPLICIT]
- Does not claim production health without provided evidence. [EXPLICIT]
- Thresholds are caller- or policy-supplied; this skill does not infer "safe"
  limits from defaults without evidence. [EXPLICIT]
- "Stale" is defined by the caller's freshness window; absent a window, treat
  any snapshot older than the stated capture horizon as stale. [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Produce a required evidence list and block healthy status |
| Live system unavailable | Mark unavailable checks `unknown` or `fail` based on evidence |
| Stale snapshot | Block healthy status and request fresh evidence |
| Optional dependency missing | Mark degraded only if policy says optional failure affects service |
| Alert owner missing | Block alert readiness until owner and handoff are defined |
| Conflicting thresholds | Use the stricter threshold and flag the conflict |
| Threshold without direction/units | Treat check as undefined -> `unknown`, request the missing spec |
| Evidence present but undated | Cannot prove freshness -> `unknown`, request capture timestamp |
| All checks pass but one required check missing | Block `healthy`; absence is not a pass |
| Flapping signal across snapshots | Report worst observed status and flag instability for review |
| Duplicate alerts for one root cause | Group by trigger/owner; dedupe before handoff to avoid fatigue |
