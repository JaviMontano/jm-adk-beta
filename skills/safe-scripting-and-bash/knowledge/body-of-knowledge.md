# Body of Knowledge — safe-scripting-and-bash

Domain knowledge for designing and reviewing safe, portable, dry-run-first Bash
scripts for local agentic workflows. [DOC]

## Key concepts

### Dry-run-first
A script that can write must default to printing intended actions, not
performing them. `--apply` performs writes; `--force` permits overwrites and is
valid only after a dry-run has been shown. This makes the write surface
inspectable before any change. [DOC]

### Write surface
The set of files and directories a script can create, modify, move, or delete,
including the breadth of any glob. The write surface must be declared and
bounded before the script is written. A `**/*` or whole-repo pattern is a
"broad write" and demands dry-run + `--apply` + `--force` + rollback notes. [DOC]

### Repo-root detection
Scripts must locate the repository root dynamically with
`git rev-parse --show-toplevel` rather than embedding an absolute,
machine-specific path. Hard-coded paths break portability and can cause a sync
to escape its intended root. [CODE]

### Destructive command isolation
`rm -rf`, `git reset --hard`, force push, and broad overwrite are destructive.
They require explicit approval AND path isolation (a bounded, validated target)
before they may appear in a script. [DOC]

### Secret hygiene
Env vars, tokens, and credentials are never read, printed, or persisted — not
even for debugging. A leak fails the gate even if behavior is otherwise correct;
the remedy is a redacted diagnostic, never an echo. [DOC]

### Offline validation
Safety of a local script must be decidable without a network call. No `curl` or
remote endpoint inside the validator or as a safety precondition; CI must reach
the same verdict offline. [DOC]

## Standards and safe constructs

- `set -euo pipefail` at the top: fail on error, undefined var, and pipe
  failure. [CODE]
- Quote every expansion: `"$var"`, `"${arr[@]}"`. Word-splitting is a
  write-surface hazard. [CODE]
- Tempdirs via `mktemp -d` with `trap 'rm -rf "$tmp"' EXIT`; never a static
  `/tmp/foo`. [CODE]
- `bash -n script.sh` for syntax; a non-destructive smoke test for behavior. [DOC]
- Prefer POSIX/stdlib; justify any Bashism or external dependency inline. [DOC]

## Decision rules

| Situation | Rule | Tag |
|-----------|------|-----|
| Write possible, no dry-run | Block; add dry-run-first | [INFERENCE] |
| Overwrite requested | Require `--force` after a dry-run | [DOC] |
| Broad write (`**/*`) | dry-run + `--apply` + `--force` + rollback | [DOC] |
| Destructive command | Approval + path isolation, or refuse | [DOC] |
| Secret read/print | Refuse; offer redacted diagnostic | [DOC] |
| Static tempdir | Replace with `mktemp -d` + trap | [CODE] |
| Absolute repo path | Replace with `git rev-parse --show-toplevel` | [CODE] |
| Validator needs network | Reject; checks stay offline | [DOC] |

## Anti-patterns

- Writing the script before the write surface is known. [DOC]
- Defaulting to apply/destroy instead of dry-run. [DOC]
- `sudo`, `chmod 777`, `curl | bash` "make it work" shortcuts. [DOC]
- Reporting green-as-success when an individual check failed. [DOC]

## Evidence taxonomy

Alfa-core tags, one per claim, consistent spelling: `[DOC]` documented behavior,
`[CONFIG]` policy-asset/config, `[CODE]` shell construct, `[INFERENCE]` reasoned
conclusion, `[ASSUMPTION]` stated assumption. [DOC]
