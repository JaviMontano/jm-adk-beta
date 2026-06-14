# Meta Prompt — validation-retry-design

Use this to decide whether the skill applies, and to self-audit a designed loop before the guardian gate.

## Activation test (all three must hold)

1. Does the target emit a **structured contract** (JSON/schema/fixed format) that is sometimes invalid?
2. Can a retry be **informed** — would telling the model exactly what failed plausibly fix it?
3. Must cost/latency be **bounded** with a legible escalation path?

If any is false -> decline. Explicitly reject: one-shot tasks with no validator, failures no retry can fix (missing source data), flaky-infra/transport retries (network, 5xx, rate-limit), and boolean pass/fail gates with no error payload.

## Self-audit before shipping

- Is the validator actionable (`code/message/path/recoverable`) rather than boolean?
- Is each failure mode classified recoverable vs not-recoverable?
- Does the feedback reinject the *specific* prior error, not the original prompt?
- Is `max_retries` in `1..3` with a counter and error chain?
- Does >= 2 identical errors break into a structural fix hint?
- Are there exactly two terminal states, with escalation carrying the full chain?
- Did I avoid touching related kata skills (`upgrade_safety`)?

## Self-correction triggers

Catch yourself if you: resend an unchanged prompt; return a non-`ok` output without an escalation packet; set `max_retries > 3` "so it eventually fixes itself" (that is the systematic signal, not a budget problem); or validate with a boolean. [INFERENCE]

## Governance

`[DOC] [INFERENCE] [SUPUESTO]` tags on claims. Single-brand: JM Labs. Never green-as-success.
