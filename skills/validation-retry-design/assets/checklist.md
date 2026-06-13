# Acceptance Checklist — validation-retry-design

Run before declaring a retry-loop design done. Each item maps to an `expected_check`.

- [ ] Validator returns `{ok, code, message, path, recoverable}` — not a boolean. (`quality_criteria`)
- [ ] Retry prompt reinjects the **specific prior error** + previous output + fix-only instruction. (`error_feedback`, `specific_error`)
- [ ] Original prompt is never resent unchanged after a failure — blind retry impossible by construction. (`blind_retry_blocker`)
- [ ] Each failure classified `recoverable` (retry) vs `not_recoverable` (escalate now). (`recoverability`)
- [ ] `1 <= max_retries <= 3`, with counter and accumulated error chain. (`retry_budget`, `budget_limit`)
- [ ] `>= 2` identical errors break into a structural `fix_hint`. (`systematic_detection`)
- [ ] Exactly two terminal states; exhaustion -> escalation packet with full chain, never last failed output as success. (`silent_failure_blocker`)
- [ ] Validator-throws -> not-recoverable escalate, never loop on a broken validator.
- [ ] Validation runs offline + deterministic against `assets/retry-loop-contract.json`. (`assets`, `deterministic_scripts`)
- [ ] Changes confined to this skill; kata skills untouched. (`upgrade_safety`)

_Single-brand: JM Labs. No invented prices. Never green-as-success._
