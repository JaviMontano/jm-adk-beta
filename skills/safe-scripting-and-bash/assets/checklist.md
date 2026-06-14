# Pre-ship Checklist — safe-scripting-and-bash

Run through this before declaring a script or review done. Every blocking item
must be checked; an unchecked blocking item is a Guardian block. [DOC]

## Blocking

- [ ] Write surface declared and bounded (paths + glob breadth). [CONFIG]
- [ ] Dry-run is the default whenever a write is possible. [DOC]
- [ ] `--force` overwrite is gated behind a prior dry-run. [DOC]
- [ ] Repo root via `git rev-parse --show-toplevel`; no absolute paths. [CODE]
- [ ] No `rm -rf` / `git reset --hard` / force push without approval + isolation. [CONFIG]
- [ ] No env var / token / credential read, printed, or persisted. [DOC]
- [ ] Tempdirs use `mktemp -d` + `trap`; no static `/tmp` names. [CODE]
- [ ] Validation runs offline; no network call decides safety. [DOC]

## High

- [ ] Every expansion quoted (`"$var"`, `"${arr[@]}"`). [CODE]
- [ ] `set -euo pipefail` present. [CODE]
- [ ] Usage examples for dry-run, apply, and force. [DOC]
- [ ] Rollback / fallback documented. [DOC]
- [ ] Every non-obvious claim carries one Alfa-core tag. [DOC]

## Verdict

- [ ] Final verdict is bound to per-check results — no green-as-success over a
      failed check. [DOC]
