<!-- distilled from alfa skills/error-recovery-automation -->
<!-- > -->
# Error Recovery Automation

> "Method over hacks."

## TL;DR

Use this skill when an automation, CI job, agent workflow, script, API call, or
deployment failed and the next action must be safe, repeatable, and auditable.
[EXPLICIT]

The output is a recovery plan, not a blind rerun: classify the failure, decide
whether retry is allowed, define bounded backoff, require rollback when state can
be corrupted, and attach validation evidence before marking recovery complete.
[EXPLICIT]

**Default-deny posture.** When evidence is insufficient, treat the failure as
non-retryable and escalate. A safe stop always beats an unsafe rerun. [INFERENCIA]

## Anti-scope (do NOT use this for)

- Designing the failing system or fixing its root-cause bug — this produces a
  recovery decision, not a code fix. [SUPUESTO]
- Greenfield workflows that have not failed yet (use a normal run, not recovery).
- Executing destructive remediation; this skill *plans* it and gates on approval.
- Replacing the on-call owner's judgment for live production incidents. [EXPLICIT]

## Procedure

### Step 1: Capture Failure Evidence

- Record the failed command/workflow, exit code or error class, scope, affected
  state, last safe checkpoint, and available logs.
- Do not invent logs, timestamps, service status, or root cause. If a required
  field is unknown, mark it as a gap — never auto-fill it. [INFERENCIA]
- **Minimum viable evidence** to proceed: (1) what ran, (2) how it failed (exit
  code/error class), (3) whether external state was mutated. Missing any of these
  forces Step 2 → `missing-evidence`. [SUPUESTO]

### Step 2: Classify Recoverability

- Use `assets/classification-policy.json` to classify the error as retryable,
  non-retryable, human-required, or blocked by missing evidence.
- Treat authentication, authorization, schema, data corruption, missing config,
  destructive side effects, and unknown state as non-retryable until evidence
  proves otherwise.
- **Idempotency gate:** retry is only safe if re-execution is idempotent OR the
  prior attempt provably made no partial write. If neither holds, route to
  rollback before any retry. [INFERENCIA]

### Step 3: Design The Recovery Plan

- If retry is allowed, use `assets/retry-policy.json` for bounded attempts,
  deterministic backoff, idempotency checks, and stop conditions.
- If state may have changed, use `assets/rollback-policy.json` *before* any retry.
- If the issue requires an owner decision, use `assets/escalation-policy.json`
  and prepare a handoff with evidence.
- **Order is load-bearing:** rollback precedes retry; escalation overrides both.
  Never retry into a state you have not first made safe. [INFERENCIA]

### Step 4: Validate And Handoff

- Produce the required sections from `assets/error-recovery-contract.json`.
- Validate structured JSON recovery plans with
  `scripts/validate_error_recovery.py`, or `scripts/check.sh` for an offline gate.
- Mark recovery complete only when post-recovery checks pass AND evidence is
  attached. Passing checks alone, without attached evidence, is not "complete".
  [EXPLICIT]

## Decision table (failure class → action)

| Failure class | Default action | Why |
|---|---|---|
| Transient network / 5xx / rate limit | Bounded retry + backoff | Self-healing if idempotent [DOC] |
| Auth / authz (401/403) | Escalate; fix credential/scope | Retry cannot fix expired/insufficient grant [INFERENCIA] |
| Schema / validation (4xx) | Stop; fix input or contract | Identical input reproduces the failure [INFERENCIA] |
| Data corruption / partial write | Rollback first, then reassess | State is untrustworthy [EXPLICIT] |
| Missing config / secret | Escalate to owner | Cannot be inferred safely [SUPUESTO] |
| Unknown / partial state | Rollback or checkpoint-validate | Recovery on unknown state is unsafe [INFERENCIA] |
| Destructive action requested | Require approval + rollback plan | Irreversible by definition [EXPLICIT] |

## Worked example (rate-limited deploy step)

1. **Evidence:** `deploy.sh` step 4/7 exited 1; error `429 Too Many Requests`;
   step is a PUT to an idempotent config endpoint; checkpoint = step 3 succeeded.
2. **Classify:** transient + idempotent → retryable per
   `assets/classification-policy.json`. [DOC]
3. **Plan:** `assets/retry-policy.json` → 3 attempts, backoff 2s/8s/32s, stop on
   any non-429. No rollback needed (no partial write). [INFERENCIA]
4. **Validate:** rerun step 4, then `scripts/check.sh`; confirm steps 5–7 reach
   green and attach the post-deploy health output as evidence.

**Counter-example:** same 429 but the endpoint is a non-idempotent POST that
created a half-written record → rollback first (`assets/rollback-policy.json`),
then retry from a clean checkpoint, not from the failed step. [INFERENCIA]

## Failure modes of this skill (and the guard)

- **Blind rerun** — retrying without classification. Guard: Step 2 is mandatory
  before any retry decision. [EXPLICIT]
- **Optimistic idempotency** — assuming a step is safe to repeat. Guard: require
  explicit evidence of idempotency or no-partial-write. [INFERENCIA]
- **Fabricated evidence** — inventing logs/status to clear a gap. Guard: a gap is
  terminal; stop and request the minimum evidence instead. [INFERENCIA]
- **Premature "complete"** — green checks, no attached evidence. Guard: Step 4
  requires both. [EXPLICIT]

## Quality Criteria

- [ ] Failure evidence is explicit and traceable.
- [ ] Error category and recoverability are justified against the decision table.
- [ ] Retry is bounded, deterministic, idempotent, and stopped on policy breach.
- [ ] Rollback is defined when state, data, deployment, or config may change.
- [ ] Escalation is explicit when retry is unsafe or evidence is insufficient.
- [ ] Validation commands, expected outcomes, and residual risks are recorded.
- [ ] Evidence tags are applied to user-facing factual claims.

## Usage

Example invocations:

- "/error-recovery-automation" - Build a recovery plan for a failed workflow.
- "Classify this CI failure and decide if retry is safe."
- "Create a rollback and escalation plan before rerunning this deployment."
- "Validate this recovery JSON against the deterministic contract."

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs). [EXPLICIT]
- Requires English-language output unless otherwise specified. [EXPLICIT]
- Does not execute destructive remediation without explicit approval. [EXPLICIT]
- Does not replace domain owner judgment for production incidents. [EXPLICIT]
- Recovery quality is bounded by evidence quality: garbage-in yields a gap
  report, not a plan. [INFERENCIA]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Produce an evidence-gap report; request the minimum failure evidence |
| Conflicting retry and safety requirements | Block retry, preserve state, and escalate |
| Unknown state after partial execution | Require rollback or checkpoint validation before recovery |
| Rate limits or transient network failures | Allow bounded retry only with idempotency and stop conditions |
| Authentication, schema, or configuration failures | Do not retry blindly; escalate or fix root cause first |
| Destructive action requested | Require approval, rollback plan, and post-action validation |
| Retry budget exhausted, still failing | Stop; escalate with full attempt log — do not loosen stop conditions |
| Checkpoint itself is unverifiable | Treat as unknown state; rollback or human validation, never resume from it |
