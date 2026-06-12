<!-- distilled from alfa skills/workflow-orchestration -->
<!-- > -->
# Workflow Orchestration
> "Method over hacks."
## TL;DR
Multi-step workflow execution with checkpoint and resume capability. [EXPLICIT]

Use this when work spans multiple stages, must survive a crash mid-run, or must be replayable for audit. For single-shot tasks with no recovery need, the overhead is not justified — use a plain skill instead. [INFERRED]

For deterministic output, prefer the bundled compiler:

```bash
python3 skills/workflow-orchestration/scripts/compile-orchestration-plan.py --input orchestration.json --output orchestration.md
```

Use `assets/orchestration-schema.json`, `assets/checkpoint-policy.json`, `assets/resume-policy.json`, and `assets/orchestration-template.md` as the contract before writing an orchestration plan by hand. [EXPLICIT]

Authoring by hand is allowed but lossy — hand-written plans skip schema validation, so run the Deterministic Gate before shipping. [INFERRED]

## Procedure
### Step 1: Discover
- Gather context and requirements
- Define the completion criteria up front; a workflow with no terminal condition cannot be validated or safely resumed. [INFERRED]
### Step 2: Analyze
- Evaluate options per Constitution XIII/XIV
- Record the chosen option and the trade-off rejected, so resume after a gap does not re-litigate decisions. [INFERRED]
### Step 3: Execute
- Implement with evidence tags
- Write a checkpoint after each stage that produces durable output, not only at the end — a single trailing checkpoint forces full replay on failure. [INFERRED]
### Step 4: Validate
- Verify quality criteria met
### Step 5: Persist Resume State
- Record resume token, state store, idempotency key, retry policy, and resume stage. [EXPLICIT]
- Do not mark complete unless checkpoints, observability, and completion criteria are recorded. [EXPLICIT]

## Decisions & Trade-offs
| Decision | Choice | Trade-off accepted |
|----------|--------|--------------------|
| Plan format | Compiled from JSON via the bundled script | Authoring cost up front, in exchange for schema-validated, deterministic, replayable output [INFERRED] |
| Checkpoint granularity | Per durable-output stage | More state writes, in exchange for bounded replay on failure [INFERRED] |
| Idempotency | Keyed retries on every recoverable action | Caller must supply stable keys, in exchange for safe re-runs without duplicate side effects [INFERRED] |

## Quality Criteria
- [ ] Evidence tags applied
- [ ] Constitution-compliant
- [ ] Actionable output
- [ ] `assets/manifest.json` lists schema, policies, and template used by `scripts/compile-orchestration-plan.py`
- [ ] `scripts/check.sh` passes with normal, incident-recovery, and invalid-resume fixtures
- [ ] Each stage has agent, inputs, actions, outputs, checkpoint, resumeState, failureSignals, and recoveryActions
- [ ] Resume contract names token, stateStore, idempotencyKey, retryPolicy, and resumeFrom
- [ ] Observability includes logs, metrics, and auditTrail

## Failure Modes
| Failure mode | Symptom | Recovery |
|--------------|---------|----------|
| Stale resume token | Resume targets a stage whose inputs no longer exist | Reject via invalid-resume fixture; restart from last valid checkpoint [INFERRED] |
| Non-idempotent retry | Re-run duplicates a side effect (double write, double notify) | Require idempotencyKey on the action; gate the retry on it [EXPLICIT] |
| Missing checkpoint | Crash forces full replay from Step 1 | Treat as gate failure — Step 5 must record checkpoints before complete [EXPLICIT] |
| Silent stage failure | Stage errors but workflow reports success | failureSignals must be declared per stage; absent signal blocks completion [EXPLICIT] |

## Usage

Example invocations:

- "/workflow-orchestration" — Run the full workflow orchestration workflow
- "workflow orchestration on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Anti-scope: not a job scheduler or cron replacement — it orchestrates one workflow's stages, not cross-workflow timing or fan-out fleets. [INFERRED]
- State store durability is the caller's responsibility; this skill defines the resume contract, not the storage backend. [INFERRED]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Resume after partial completion | Restart from `resumeFrom` stage using idempotency key; never replay completed durable stages [INFERRED] |
| Retry budget exhausted | Stop, emit auditTrail entry, surface failureSignals — do not loop silently [INFERRED] |

## Deterministic Gate

Run `bash skills/workflow-orchestration/scripts/check.sh` when structured orchestration data is available or before shipping a reusable plan. The check validates JSON assets, positive fixtures, negative fixtures, Python syntax, and report fragments. [EXPLICIT]

Acceptance: the gate must pass all three fixtures (normal, incident-recovery, invalid-resume) before a plan is considered shippable — a green positive run alone is insufficient. [INFERRED]
