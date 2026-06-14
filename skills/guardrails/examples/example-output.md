# Example output — guardrails (pre-tool-use-guard verdict)

# Guard Verdict — pre-tool-use-guard

verdict: block
exit_code: 2
topic: pre-tool-use-guard
depth: quick
target: `rm -rf build/ && cat .env` (cwd /repo, allowed_write_roots ["build/"])
triggering_rule: worst-segment-governs + private-path-policy + dangerous-command-policy

## Decision summary

Blocked. The command is compound and at least one segment is a hard blocker, so
the worst segment governs the whole call. `cat .env` surfaces unmasked credentials
(private-path policy) and `rm -rf build/` is a destructive deletion
(dangerous-command policy). The in-scope `build/` write does NOT rescue the call.
[EXPLICIT]

## Checks

| Check | Status | Expected | Observed | Repair |
|---|---|---|---|---|
| inputs_parsed | pass | command, cwd, write scope resolvable | two segments parsed | — |
| destructive_command | fail | no `rm -rf` / `git reset --hard` | `rm -rf build/` matched | run a scoped delete or move to trash; do not recurse-force |
| private_path | fail | no `.env` / credential read | `cat .env` matched | read masked config via the secrets-aware reader, not raw `.env` |
| write_scope | pass | writes within ["build/"] | delete target in scope | — |

## Violations (aggregated)

- segment 1 — `rm -rf build/` matched dangerous-command-policy → replace with a
  non-recursive scoped removal of named files.
- segment 2 — `cat .env` matched private-path-policy → never echo raw `.env`;
  route through the masked reader.

## Evidence

- [CODE] `scripts/validate_pre_tool_use_guard.py` returns action=block,
  exit_code=2 on this report; `scripts/check.sh` exits 0 (pos + neg fixtures).
- [CONFIG] dangerous-command-policy entry `rm -rf` and private-path-policy marker
  `.env` both matched.
- [DOC] pre-tool-use-guard playbook: "Compound commands are blocked if ANY segment
  is a blocker"; "the worst segment governs."

## Secrets (masked only)

- `.env` would surface live credentials if read — content NOT reproduced here;
  the block prevents exposure. severity Critical → owner platform-team.

## Out-of-scope / not verified

- Post-execution output validation (would route to post-tool-use-validator).
- Git-history secret scanning (out of working-tree scope).

## Determinism note

Same proposed call ⇒ byte-identical packet; no clock/network/model/random entered
the verdict. [EXPLICIT]
