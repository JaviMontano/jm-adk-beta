# Example output — agent-orchestration

Worked dispatch packet for the failed `sync-ledger.sh` request.

## Request Classification
- Resolved `topic`: `error-recovery-automation` — an automation that already ran
  and failed; the next action must be safe and auditable. [CONFIG]
- Runner-up: `workflow-orchestration` — rejected because the user is not building
  a new workflow, they are recovering one that failed; the narrowest match is
  recovery. [INFERENCE]
- `depth`: deep. [CONFIG]

## Playbook Loaded
- Playbook: `references/error-recovery-automation.md` (only this one). [CONFIG]
- Required inputs gathered: failed command, error class (`409 Conflict`),
  state-mutated = yes (3 entries written), checkpoint = step 4. No `[OPEN]`
  gaps — minimum viable evidence is present. [DOC]

## Analysis (policy applied)
- Decision table row: the endpoint is a non-idempotent POST and a partial write
  occurred → **not** the transient/idempotent path. Retry is unsafe until state
  is made safe. [DOC]
- Idempotency gate fails: re-running step 5 would risk duplicate journal
  entries. Order is load-bearing — rollback precedes retry. [INFERENCE]
- Option chosen: rollback the 3 written entries (or reconcile to a clean
  checkpoint), then retry from step 5. Trade-off rejected: blind rerun, which
  would double-write. [INFERENCE]

## Execution / Deliverable
- Recovery plan:
  1. Capture evidence (done above).
  2. Classify: non-idempotent + partial write → rollback-first. [DOC]
  3. Roll back the 3 entries using `assets/rollback-policy.json`; verify the
     ledger matches the step-4 checkpoint. [CONFIG]
  4. Retry from step 5 with bounded backoff per `assets/retry-policy.json`;
     stop on any non-409. [CONFIG]
  5. Validate: rerun, then `scripts/check.sh`; attach post-recovery ledger
     reconciliation as evidence (script-first). [CONFIG]
- Resume state: idempotencyKey on the journal POST; resumeFrom = step 5 after
  rollback verification. [DOC]

## Validation Gate (Guardian)
- [x] One playbook loaded
- [x] Topic in enum
- [x] Spine completed
- [x] Constitution v6.0.0 enforced
- [x] Evidence tags present, single family
- [x] Script-first honored (rollback/retry policies + `check.sh`)
- [x] No false "passed" before this gate
- Verdict: **PASS** (plan only — destructive rollback still requires owner
  approval before execution). [DOC]

## Risks & Assumptions
- [ASSUMPTION] The accounting API exposes a reversible delete for the 3 entries;
  if not, escalate to the ledger owner instead of auto-rollback.
- Residual risk: a fourth entry may have been written between failure and
  inspection — reconcile against the step-4 checkpoint before retry. [INFERENCE]
