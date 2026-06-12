<!-- distilled from alfa skills/post-tool-use-validator -->
<!-- Validate tool outputs against exit codes, evidence tags, quality gates, secret exposure policy, scope compliance, and offline post-tool report fixtures. [EXPLICIT] -->
# Post Tool Use Validator

Validates tool outputs after execution and blocks unsupported success claims. Checks command status, evidence, quality gates, secret exposure, and scope compliance before the assistant says work is done. Runs once per tool result; it gates the claim, not the tool call (that is `pre-tool-use-guard`). [EXPLICIT]

**Scope.** Post-execution claim validation only. NOT: pre-execution blocking, prompt filtering, or final-turn checks — those are sibling guardrails. [INFERENCIA]

## Deterministic Contract

- `assets/post-tool-validation-contract.json` defines the JSON report shape.
- `assets/evidence-policy.json` defines evidence requirements.
- `assets/secret-output-policy.json` defines unmasked secret blockers.
- `assets/scope-validation-policy.json` defines write-scope blockers.
- `scripts/validate_post_tool_use_report.py` validates reports offline.
- `scripts/check.sh` runs positive and negative fixtures.

## Procedure

1. Read the tool result: tool name, command, exit code, stdout/stderr excerpts, and touched paths.
2. Verify that declared status matches the actual result.
3. Require evidence for every pass claim.
4. Block unmasked secrets, private data exposure, and writes outside scope.
5. Return `pass`, `warn`, `fail`, or `blocked` with next action.

## Decision States

Most-restrictive state wins on conflict: `blocked` > `fail` > `warn` > `pass`. Never upgrade a state to satisfy a claim. [INFERENCIA]

- `pass` — status matches result, evidence present, no blocker. Proceed.
- `warn` — non-blocking gap (e.g. thin evidence, recoverable stderr noise). Proceed only after the gap is named in output. [SUPUESTO]
- `fail` — status/result mismatch or missing evidence. Retract the success claim; retry or report.
- `blocked` — secret exposure or out-of-scope write. Terminal: stop, do not present output, escalate. [INFERENCIA]

## Fail-Closed Conditions

- Tool exit code is non-zero but decision says `pass`.
- Evidence tags or command evidence are missing.
- Output includes unmasked token-like secrets.
- Writes occurred outside declared scope.
- A quality gate is failed while the report claims pass.

## Edge Cases

- Exit `0` but stderr shows a real error (silent-failure tools) → `fail`, not `pass`; the exit code is necessary, not sufficient. [INFERENCIA]
- Secret already masked (`sk-***`) → not a blocker; only unmasked token-like strings block. [CONFIG]
- Write to a declared-scope path that did not exist before → allowed; scope is about boundary, not novelty. [SUPUESTO]
- Tool result absent or unparseable → `fail` (cannot confirm success), never `pass`. [INFERENCIA]

## Worked Example (fail-closed)

Result: `pytest` exit `1`, stderr `2 failed`; report claims `pass`. → emit `fail`,
retract the "tests pass" claim, next action = surface the 2 failures. Asserting
pass here is the exact failure mode this validator exists to catch. [EXPLICIT]

## Acceptance Criteria

- Every `pass` claim is backed by exit code plus evidence; unbacked pass → `fail`. [DOC]
- No success claim survives a non-zero exit or a failed quality gate.
- No unmasked secret or out-of-scope write ever ships under any state but `blocked`.
- Report validates against `post-tool-validation-contract.json` before it is presented.

## Usage

Run the fixture gate:

```bash
bash skills/post-tool-use-validator/scripts/check.sh
```
