<!-- distilled from alfa skills/pre-tool-use-guard -->
<!-- Block dangerous commands before execution using the exit-code-2 deny pattern, deterministic write-scope policy, private path protection, and offline report validation. [EXPLICIT] -->
# Pre Tool Use Guard

Blocks unsafe tool calls before execution. The contract is intentionally narrow: a report either allows the call, requires explicit approval, or blocks it with the exit-code-2 pattern. Fail closed on ambiguity — an undecidable call is `block`, never `allow`. [EXPLICIT]

## Deterministic Contract

- `assets/guard-decision-contract.json` defines the JSON report shape. [EXPLICIT]
- `assets/dangerous-command-policy.json` lists command patterns that must fail closed. [EXPLICIT]
- `assets/write-boundary-policy.json` defines protected and allowed write surfaces. [EXPLICIT]
- `assets/private-path-policy.json` defines private path markers. [EXPLICIT]
- `scripts/validate_pre_tool_use_guard.py` validates reports offline. [EXPLICIT]
- `scripts/check.sh` runs positive and negative fixtures. [EXPLICIT]

Required `decision` keys: `action` (`allow|approve|block`), `exit_code` (`0` allow, `1` approve, `2` block), `reason`, `evidence`. A `block` MUST carry `exit_code: 2`; an `allow` MUST carry `exit_code: 0` and non-empty `evidence`. [INFERENCE]

## Procedure

1. Parse the proposed tool call, command, cwd, and write scope.
2. Detect destructive commands, private path touches, secret exposure risk, and writes outside declared scope.
3. Set `decision.action` to `block` and `decision.exit_code` to `2` for any hard blocker.
4. Allow only read-only or explicitly scoped safe writes.
5. Validate the report before presenting the decision.

## Fail-Closed Conditions

- `git reset --hard`, `git clean -fd`, broad deletion (`rm -rf`), or equivalent destructive shell. [EXPLICIT]
- Writes outside declared `allowed_write_roots`. [EXPLICIT]
- Any action touching `user-context/jarvis-os`, `.env`, credentials, or secret-like paths. [EXPLICIT]
- Missing evidence for an allow decision. [EXPLICIT]
- Any blocker with `decision.action: allow`. [EXPLICIT]
- Unparseable command, obfuscation (base64/`eval`/`curl … | sh`), or scope that cannot be resolved — fail closed. [INFERENCE]

## Edge Cases

- Path normalization first: `../` traversal, symlinks, and `~` expansion resolve to a real target before scope check; `./sub/../../.env` is a private-path block. [INFERENCE]
- Allow read-only inspection (`git status`, `ls`, `cat`) even inside protected roots; block only writes/deletes there. [INFERENCE]
- Compound commands (`&&`, `;`, `|`, command substitution) are blocked if ANY segment is a blocker. [INFERENCE]
- Pure reads of a secret file are still blocked when output would surface unmasked secret content. [INFERENCE]

## Anti-Scope

Does not validate tool OUTPUT after execution — that is `post-tool-use-validator`. Does not sanitize prompts (`user-prompt-filter`) or rewrite commands; it only decides allow/approve/block. [INFERENCE]

## Acceptance Criteria

- Every dangerous-policy fixture yields `block` + `exit_code: 2`; every safe fixture yields `allow` + `exit_code: 0`. [EXPLICIT]
- `validate_pre_tool_use_guard.py` passes on the emitted report; `check.sh` exits `0`. [EXPLICIT]
- No `allow` lacks `evidence`; no `block` lacks a `reason`. [INFERENCE]

## Worked Example

Proposed: `rm -rf build/ && cat .env`, cwd repo root, `allowed_write_roots: ["build/"]`.
Decision: `block`, `exit_code: 2`, reason "`.env` secret read + `rm -rf` destructive", evidence = matched `dangerous-command-policy` + `private-path-policy` entries. The `build/` write being in scope does NOT rescue the call — the worst segment governs. [INFERENCE]

## Usage

Run the fixture gate:

```bash
bash skills/pre-tool-use-guard/scripts/check.sh
```
