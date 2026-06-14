# Quick Variation — safe-scripting-and-bash

Fast review of a single short script when the write surface is small and known.
Use only when one file's scope is obvious; otherwise use the deep variation. [DOC]

## Steps

1. Confirm the write surface fits in one paragraph (paths + glob breadth). If
   not, escalate to the deep variation. [DOC]
2. Scan for the four high-severity hazards, in order:
   - Destructive: `rm -rf`, `git reset --hard`, force push. [CONFIG]
   - Secret: any env var / token / credential read or printed. [DOC]
   - Absolute repo path instead of `git rev-parse --show-toplevel`. [CODE]
   - Static tempdir (`/tmp/foo`) instead of `mktemp -d` + trap. [CODE]
3. Confirm dry-run is the default and `--force` is gated behind a prior dry-run. [DOC]
4. Run `bash -n` and emit a one-screen safety report (template's check table only).

## Stop conditions

- Any high-severity hazard unresolved → return guardian_block, do not pass. [DOC]
- Write surface larger than expected → switch to `prompts/variations/deep.md`. [INFERENCE]

Tag each finding with one Alfa-core tag. [DOC]
