---
name: validation-retry-design
version: 1.2.0
description: "Design deterministic extract-validate-retry loops with actionable validation errors, recoverable vs not-recoverable classification, bounded retry budgets, systematic-error detection, escalation packets, and offline validation."
owner: "JM Labs"
last_updated: 2026-06-11
triggers:
  - validation retry design
  - error feedback loop
  - recoverable vs not
  - retry budget
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Validation Retry Design

## Purpose

Design deterministic `extract -> validate -> retry-with-error-feedback` loops that never retry blindly. The loop reinjects the exact validation error, classifies recoverable vs not-recoverable failures, enforces a retry budget, detects systematic repeat errors, and escalates with a complete error chain instead of silently accepting a failed output. [DOC]

## When to use

Use when **all three** hold; if any is false, this skill is overkill. [INFERENCE]

- A model/agent/pipeline emits **structured output** (JSON, schema, fixed format) that is sometimes invalid. [DOC]
- A retry can be **informed**: the model can plausibly fix the output if told *what* failed (format, parse, range). [DOC]
- Cost/latency must be **bounded**: a finite budget instead of an infinite loop, with a legible escalation path when the loop gives up. [DOC]

## Anti-scope (do NOT use)

- One-shot tasks with no validator and no structured contract (e.g. marketing copy, a one-off lint summary). [INFERENCE]
- Failures that **no retry can fix** (missing source data, irresolvable ambiguity): classify as not-recoverable and escalate immediately — never loop. [DOC]
- Flaky-infra retries (network, rate-limit, 5xx). Those are transport backoff, not *validation* feedback; out of scope here. [INFERENCE]
- Boolean pass/fail gates with no error payload to reinject — fix the validator first, then apply this skill. [INFERENCE]

## Inputs / Outputs

**Inputs** [DOC]
- A task with a `base_prompt` and the structured contract the output must satisfy (schema/format/range).
- A **validator** that returns `{ok, code, message, path, recoverable}` — not a bare boolean.
- `max_retries` (1–3) and the policy assets below.

**Outputs** (exactly one terminal state) [DOC]
- `{"status":"ok", "output", "attempts"}` — validation passed.
- Escalation packet `{"status":"escalated", "reason", "error_chain", "last_output", "fix_hint?"}` where `reason ∈ {not_recoverable, systematic, budget_exhausted}`.

Never a third state. Returning the last failed output as success is a defect, not an output. [DOC]

## Deterministic Contract

Validate plans against `assets/retry-loop-contract.json` using `scripts/validate_retry_plan.py`. The validation MUST run **offline and deterministic** (`offline=true`, `network_required=false`, `deterministic=true`) so the same plan always yields the same verdict. [DOC] A valid plan includes: [DOC]

- Validator output with actionable `code`, `message`, `path`, and `recoverability`.
- Retry feedback carrying the previous output **and** the exact validation error.
- Failure classification with `recoverable` and `not_recoverable` categories.
- `max_retries` between 1 and 3.
- Systematic repeat-error detection.
- Escalation packet with `reason`, `error_chain`, and `last_output`.

## How to build

1. **Validator first.** Write the function that decides pass/fail and **returns a specific, actionable error** (code + message + path + recoverability), never a bare boolean. The error is the retry's only fuel. [DOC]
2. **Classify the failure mode.** In the validator, mark each error `recoverable` (format, parse, range, schema shape) or `not_recoverable` (missing datum, source contradiction). Only recoverable errors retry. [DOC]
3. **Build informed feedback.** Compose the next attempt's prompt as: previous output + exact error + a *fix-only* instruction ("fix what failed, keep the rest"). Never resend the original prompt unchanged. [DOC]
4. **Cap it.** Fix `max_retries` (2–3). Keep a counter and an accumulated error chain. [DOC]
5. **Detect systematic patterns.** If the *same* error recurs every attempt, it is not noise — it is a structural defect (prompt, schema, or source). Break the loop and report the structural fix instead of burning retries. [DOC]
6. **Escalate on exhaustion.** At the budget cap, or on a not-recoverable failure, return the escalation packet with the full error chain and last output for human or supervisor-agent review. [DOC]

### Decisions & trade-offs

- **`max_retries` capped at 3.** Beyond 3, recoverable errors are almost always already fixed; further attempts mask a systematic defect and burn cost. The cap forces the systematic/escalation path instead of hope. [INFERENCE]
- **Reinject error, not full history.** Send last output + last error, not the whole transcript — bounds context growth and keeps the model focused on the delta. Trade-off: loses cross-attempt trend, which is why systematic-detection runs on the error chain separately. [INFERENCE]
- **Systematic break is eager (2 identical errors).** Stopping early on a repeat is cheaper than exhausting the budget and yields a sharper fix hint. [INFERENCE]

## Acceptance gate (Definition of Done)

Ship only when every item holds; each maps to an `expected_check`. [DOC]

- [ ] Retry feedback is the **specific error** of the prior attempt, not the unchanged original prompt. (`error_feedback`, `specific_error`) [DOC]
- [ ] Validator returns an actionable cause, not just `true/false`. (`quality_criteria`) [DOC]
- [ ] Recoverable (retry) is distinguished from not-recoverable (escalate now). (`recoverability`) [DOC]
- [ ] Retry budget exists, `1 <= max_retries <= 3`, with counter and error chain. (`retry_budget`, `budget_limit`) [DOC]
- [ ] Systematic repeat-error detection triggers a structural fix hint instead of more retries. (`systematic_detection`) [DOC]
- [ ] On exhaustion: escalation with the full error chain; a failed output is **never** returned as success. (`silent_failure_blocker`) [DOC]
- [ ] Blind retry of the original prompt is impossible by construction. (`blind_retry_blocker`) [DOC]
- [ ] `assets/*` policies referenced and `scripts/*` checks pass. (`assets`, `deterministic_scripts`) [DOC]
- [ ] Changes stay inside this skill; related kata skills untouched. (`upgrade_safety`) [DOC]

## Output Rules

Reference `assets/error-feedback-policy.json`, `assets/recoverability-policy.json`, `assets/retry-budget-policy.json`, `assets/systematic-error-policy.json`, `assets/escalation-policy.json`, and `assets/anti-pattern-policy.json`. [DOC] Hard rules: [DOC]

- Never retry the original prompt unchanged after a validation failure.
- Never use boolean-only validation.
- Never retry not-recoverable missing-source or irresolvable-ambiguity errors.
- Never return the last failed output as success.

## Pattern

```python
# GOOD: informed retry, classified failure mode, bounded budget, escalation
def run_with_retry(task, max_retries=3):
    errors, prev_output = [], None
    for attempt in range(max_retries):
        prompt = build_prompt(task, prev_output, errors[-1] if errors else None)
        output = model.run(prompt)
        verdict = validate(output)  # -> {"ok", "error", "recoverable"}
        if verdict["ok"]:
            return {"status": "ok", "output": output, "attempts": attempt + 1}
        if not verdict["recoverable"]:
            return escalate(reason="not_recoverable", errors=errors + [verdict["error"]])
        errors.append(verdict["error"])
        prev_output = output
        if is_systematic(errors):  # same error repeating -> structural defect
            return escalate(reason="systematic", errors=errors, fix_hint="schema/prompt")
    return escalate(reason="budget_exhausted", errors=errors, last_output=prev_output)


def build_prompt(task, prev_output, last_error):
    if prev_output is None:
        return task.base_prompt
    # reinject the SPECIFIC error, not the original prompt unchanged
    return (
        f"{task.base_prompt}\n\n"
        f"Your previous output failed validation: {last_error}\n"
        f"Previous output:\n{prev_output}\n"
        f"Fix only what failed; keep everything else."
    )
```

## Anti-Pattern

```python
# ANTI: blind retry + silent failure
def run_bad(task, max_retries=3):
    for _ in range(max_retries):
        output = model.run(task.base_prompt)   # same prompt every time, no feedback
        if validate_bool(output):              # boolean only, no error reason
            return output
    return output  # accept the last failed output silently, no escalation
```

Why it fails: resending the original prompt without the error makes the model repeat the same failure; a boolean validator has nothing to feed the retry; and returning the last failed output without escalating hides the defect downstream. [INFERENCE]

## Edge cases & self-correction triggers

- **Validator itself throws** (not a clean fail): treat as not-recoverable, escalate with the exception in the chain — do not loop on a broken validator. [INFERENCE]
- **Output passes schema but fails semantics:** the validator's `code/message` must distinguish these so feedback is targeted; a generic "invalid" wastes the retry. [INFERENCE]
- **Two distinct recoverable errors alternate** (A, B, A, B): not systematic by identity, but a non-converging oscillation — cap still fires `budget_exhausted`; consider tightening the fix-instruction. [INFERENCE]
- **`max_retries=1`** is valid (single corrective attempt) but means systematic-detection cannot fire; rely on the budget-exhausted escalation. [INFERENCE]

Self-correct if you catch yourself: resending an unchanged prompt; returning a non-`ok` output without an escalation packet; setting `max_retries > 3` "so the model eventually fixes itself" (that is the systematic-defect signal, not a budget problem); or validating with a boolean. [INFERENCE]

## Scripts

```bash
python3 skills/validation-retry-design/scripts/validate_retry_plan.py --input <plan.json>
bash skills/validation-retry-design/scripts/check.sh
```

## Katas y skills relacionadas

- Kata: `katas-26`
- Relacionada: `katas-validation-retry-feedback`
- Vecinas de diseño: `independent-review-design`, `workflow-forge`
