# Quick Variation — devops-deploy

Fast path. Resolve one topic, read one playbook, ship the minimum viable artifact
with its gate.

## Steps
1. Map request → one enum topic (ask only if truly ambiguous).
2. Read `references/<topic>.md` at `depth=quick` (essentials only).
3. Produce the core artifact via `templates/output.md` — skip exhaustive
   edge-case enumeration.
4. Run the playbook's primary validator if cheap; record pass/fail.

## Non-negotiables even in quick mode
- One topic, one playbook — no cluster loading.
- Evidence tags on every claim.
- No secret values in output.
- Green build ≠ done — state the one behavior check still owed.

## Example
"Add a cache step to this Actions workflow" → topic `github-actions-ci`, quick:
emit the lockfile-keyed `cache` config + the one criterion (key includes lockfile
hash) and note SHA-pinning is still owed for release jobs. [DOC]
