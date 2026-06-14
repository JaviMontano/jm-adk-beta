# Deep Variation — safe-scripting-and-bash

Full four-agent treatment for broad-write scripts, multi-file syncs, or any
script whose write surface crosses repo boundaries. Use when the quick variation
cannot bound the scope in a single paragraph. [DOC]

## Procedure

1. **Discover (Lead + Support)**
   - Read every existing script the change touches and the repo conventions. [DOC]
   - Enumerate the full write surface: each path, each glob, and breadth
     (`**/*` is broad). Detect nested/sibling repos that a sync could escape. [INFERENCE]

2. **Analyze (Specialist)**
   - Classify against all policy assets: destructive, write-surface,
     dry-run, portability, validation. [CONFIG]
   - For each broad write, require dry-run + `--apply` + `--force` + rollback
     notes before proceeding. [DOC]

3. **Execute (Support)**
   - `set -euo pipefail`; repo-root via `git rev-parse --show-toplevel`. [CODE]
   - Dry-run-first; quote every `"$var"` / `"${arr[@]}"`; `mktemp -d` + trap. [CODE]
   - Produce usage for dry-run, apply, and force; document rollback/fallback. [DOC]

4. **Validate (Guardian)**
   - `bash -n` plus a deterministic, offline smoke test on a fixture. [DOC]
   - Run the offline gate; bind the verdict to per-check results. [CONFIG]
   - No network call decides safety; no green-as-success over a failed check. [DOC]

## Edge cases to force

- Broad write, static tempdir, unquoted expansion, secret-in-output, nested
  repos, CI/offline. Each must be explicitly resolved or refused. [DOC]

## Output

Full safety report via `templates/output.md`, including the rollback section and
the per-check table. One Alfa-core tag per non-obvious claim. [DOC]
