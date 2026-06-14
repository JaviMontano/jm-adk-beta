# Guard Verdict — {topic}

verdict: allow | approve | block | pass | fail | blocked | not_verified
exit_code: 0 | 1 | 2 | n/a
topic: <one of the 12 enum values>
depth: quick | deep
target: <proposed tool call + cwd, or artifact path + declared contract>
triggering_rule: <policy/gate rule that decided the verdict>

## Decision summary

<One or two sentences. State the verdict and the single rule that governs it.
Worst-segment / worst-row governs compound inputs.> [EXPLICIT]

## Checks

| Check | Status | Expected | Observed | Repair |
|---|---|---|---|---|
| contract_loaded / inputs_parsed | pass/fail/blocked | <expectation> | <observed> | <exact edit> |
| <content/gate check> | pass/fail/blocked | <expectation> | <observed> | <exact edit> |

## Violations (aggregated — never stop at first)

- `<path:line or check id>` — <what failed> → <deterministic repair: exact target + exact edit>
- None.

## Evidence

- [CODE] <script run + result, e.g. `scripts/check.sh` exit 0 on pos/neg fixtures>
- [CONFIG] <policy asset and matched entry>
- [DOC] <playbook clause applied>

## Secrets (masked only)

- `<path:line>` `<MASKED token, ≤4 prefix chars>` — severity Critical/High/Medium → owner + action
- None found in scope.

## Out-of-scope / not verified

- <vectors not covered (e.g. git history, binaries) listed, never silently passed>

## Determinism note

Same input ⇒ byte-identical packet; no clock/network/model/random entered the
verdict. [EXPLICIT]
