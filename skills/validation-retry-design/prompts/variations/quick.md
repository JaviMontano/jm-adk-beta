# Quick Variation — validation-retry-design

Fast path for a single structured-output contract that needs a bounded informed-retry loop.

## Ask

"Design a retry loop for `<contract>`: validator returns `{ok,code,message,path,recoverable}`, reinject the exact error on retry, `max_retries=<2 or 3>`, break on 2 identical errors, escalate on exhaustion or not-recoverable. No blind retry, no silent failure."

## Minimum deliverable

- Validator error shape + 3-row recoverability table (recoverable / not_recoverable examples).
- One feedback-builder snippet that reinjects the specific error.
- Terminal states: `{status:ok,...}` and `{status:escalated, reason ∈ {not_recoverable, systematic, budget_exhausted}, error_chain, last_output}`.

## Skip when

One-shot task, no validator, transport/infra retry, or boolean-only gate -> not this skill.

Tag claims `[DOC] [INFERENCE]`. Single-brand: JM Labs.
