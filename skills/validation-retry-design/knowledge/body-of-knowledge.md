# Body of Knowledge — validation-retry-design

Domain knowledge for designing deterministic extract-validate-retry loops with actionable error feedback. Scope is *validation* feedback, not transport backoff. [DOC]

## Key concepts

- **Informed retry.** A retry that carries the exact prior validation error plus the previous output and a fix-only instruction. The opposite — resending the original prompt unchanged — is a **blind retry** and reliably reproduces the same failure. The error is the retry's only fuel. [DOC]
- **Actionable validator.** A validator that returns `{ok, code, message, path, recoverable}`, not a bare boolean. `code` separates schema-shape failures from semantic failures so feedback can target the real cause; a generic "invalid" wastes the attempt. [DOC]
- **Recoverability classification.** Each failure is `recoverable` (format, parse, range, schema shape — fixable by an informed retry) or `not_recoverable` (missing source datum, source contradiction, irresolvable ambiguity — no retry can fix it). Only recoverable errors loop. [DOC]
- **Retry budget.** A finite cap `1 <= max_retries <= 3` with a counter and an accumulated error chain. Beyond 3, recoverable errors are almost always already fixed; more attempts mask a systematic defect and burn cost. [DOC][INFERENCE]
- **Systematic error.** The *same* error recurring across attempts. It is a structural defect (prompt, schema, or source), not noise. Detection is eager — >= 2 identical errors breaks the loop and emits a structural `fix_hint`. [DOC]
- **Escalation packet.** The non-`ok` terminal state: `{status:"escalated", reason, error_chain, last_output, fix_hint?}` with `reason ∈ {not_recoverable, systematic, budget_exhausted}`. Carries the full chain for human or supervisor-agent review. [DOC]
- **Silent failure.** Returning the last failed output as if it passed. A defect, never an output — the loop has exactly two terminal states. [DOC]

## Standards & invariants

1. **Exactly two terminal states:** `ok` or escalation. Never a third. [DOC]
2. **Determinism:** validation runs `offline=true`, `network_required=false`, `deterministic=true` against `assets/retry-loop-contract.json` — same plan, same verdict, every time. [DOC]
3. **Bounded context:** reinject last output + last error only, not the whole transcript. Cross-attempt trend lives in the error chain, consumed separately by systematic-detection. [INFERENCE]
4. **No blind retry by construction:** the feedback builder must make resending the unchanged prompt impossible, not merely discouraged. [DOC]

## Decision rules

- No actionable validator yet -> build it first; do not design the loop. [DOC]
- Not-recoverable failure or thrown validator -> escalate immediately, never loop. [DOC]
- Same error twice -> systematic break with fix_hint, not another retry. [DOC]
- Request for `max_retries > 3` -> treat as a systematic-defect signal; reject the budget increase. [DOC]
- `max_retries = 1` -> valid single corrective attempt, but systematic-detection cannot fire; rely on budget-exhausted escalation. [INFERENCE]
- Alternating distinct recoverable errors (A,B,A,B) -> non-converging oscillation, not systematic-by-identity; budget cap fires `budget_exhausted`; tighten the fix-instruction. [INFERENCE]

## Anti-scope

One-shot tasks with no validator; failures no retry can fix; flaky-infra/transport retries (network, 5xx, rate-limit — those are backoff, not validation feedback); boolean pass/fail gates with no error payload to reinject. [DOC]

## Evidence taxonomy

`[DOC]` stated in SKILL.md or a policy asset · `[INFERENCE]` derived from the contract · `[SUPUESTO]` assumption to confirm. Single-brand: JM Labs.
