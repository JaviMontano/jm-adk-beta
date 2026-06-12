<!-- distilled from alfa skills/task-automation -->
<!-- > -->
# Task Automation
> "Method over hacks."
## TL;DR
Recurring task scheduling, batch operations, periodic health checks. Use when the same operation repeats on a cadence or fans out over many items; do NOT use for one-shot interactive work. [EXPLICIT]
## Procedure
### Step 1: Discover
- Gather context, requirements, trigger (cron/event/manual), and the item set to operate on
- Record the success signal and the rollback path *before* writing any automation [SUPUESTO]
### Step 2: Analyze
- Evaluate options per Constitution XIII/XIV; choose schedule vs. event-driven vs. batch [EXPLICIT]
- Trade-off [INFERENCIA]: cron = predictable but blind to load; event-driven = reactive but harder to test/replay. Default to cron for health checks, events for state changes.
### Step 3: Execute
- Implement with evidence tags; make every run idempotent (safe to re-run) and bounded (timeout + max retries)
- Emit a structured run record: start, end, items processed, failures, exit reason [EXPLICIT]
### Step 4: Validate
- Verify quality criteria met; dry-run once, then enable the live cadence
## Quality Criteria
- [ ] Evidence tags applied
- [ ] Constitution-compliant
- [ ] Actionable output
- [ ] Idempotent: re-running produces no duplicate side effects [EXPLICIT]
- [ ] Observable: each run emits a pass/fail record with a reason [EXPLICIT]
- [ ] Bounded: explicit timeout, retry cap, and failure escalation path [EXPLICIT]

## Acceptance Criteria
- [ ] Trigger fires on the intended cadence/event and is verifiable from the run log [EXPLICIT]
- [ ] A forced failure surfaces (alert/escalation), not a silent skip [EXPLICIT]
- [ ] Partial batch failure leaves the system in a known, resumable state [INFERENCIA]

## Worked Example
Goal: nightly health check across 40 repos.
- Trigger: cron 02:00; item set: repo list from config.
- Per item: run check, append `{repo, status, reason}` to run record; never abort the batch on one failure (isolate, continue) [INFERENCIA].
- End: if any `status=fail`, escalate one summary alert (not 40); exit non-zero so the scheduler marks the run failed [EXPLICIT].

## Usage

Example invocations:

- "/task-automation" — Run the full task automation workflow
- "task automation on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Anti-scope: not for one-off interactive tasks, ad-hoc refactors, or anything needing human-in-the-loop per item [EXPLICIT]
- Assumes the scheduler/runtime persists run records; ephemeral runners need external log capture [SUPUESTO]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Run overlaps previous run | Skip or lock (single-flight); never run concurrently on shared state [INFERENCIA] |
| Partial batch failure | Isolate failed items, continue, report; mark run failed if any item failed [EXPLICIT] |
| Trigger never fires | Treat missing run as a failure; add a dead-man's-switch / freshness check [SUPUESTO] |
| Transient error (network/rate-limit) | Retry with backoff up to the cap, then escalate [INFERENCIA] |

## Failure Modes
- Silent no-op: automation runs but processes zero items — guard with a min-item assertion [INFERENCIA]
- Alert storm: per-item alerts instead of one run summary — aggregate before escalating [EXPLICIT]
- Non-idempotent retry: re-run duplicates side effects — key writes by item id [EXPLICIT]
