# Deep Variation — validation-retry-design

Full design for a production loop where wrong escalation reasons or context blowup are costly.

## Expand each dimension

- **Validator depth.** Enumerate every `code`; separate schema-shape from semantic failures; define behavior when the validator itself throws (treat not-recoverable, escalate with the exception in the chain — never loop on a broken validator).
- **Recoverability matrix.** For each `code`: recoverable/not_recoverable, the fix-only instruction it implies, and whether it can plausibly converge.
- **Context budgeting.** Justify reinjecting last output + last error only (not the whole transcript); show where cross-attempt trend lives (the error chain) so systematic-detection still works.
- **Systematic vs oscillation.** Distinguish >= 2 identical errors (systematic break + structural fix_hint) from alternating A,B,A,B (non-converging oscillation -> budget_exhausted; tighten the fix-instruction).
- **Budget rationale.** Defend `max_retries` in `1..3`; explain why >3 masks a systematic defect. Note that `max_retries=1` disables systematic-detection and relies on budget-exhausted escalation.
- **Escalation packet.** Full `{reason, error_chain, last_output, fix_hint?}` for human or supervisor-agent review; map each `reason` to its exit condition.

## Determinism & gate

Validate the plan offline/deterministic against `assets/retry-loop-contract.json` (`offline=true`, `network_required=false`, `deterministic=true`). Walk every acceptance-gate item in `agents/guardian.md`.

Tag claims `[DOC] [INFERENCE] [SUPUESTO]`. Single-brand: JM Labs. Never green-as-success.
