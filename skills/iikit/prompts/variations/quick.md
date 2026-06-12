# Quick Variation — iikit (depth=quick)

Single-pass routing for an unambiguous stage request.

1. Map the named stage or `00`–`08` number to `topic` (enum is authoritative).
2. Confirm the predecessor artifact exists; if not, stop and name what to run.
3. Read the one matching `references/*.md` playbook.
4. Execute its essential steps in one pass — run the prescribed `iikit-core`
   scripts, skip the exhaustive per-gate verification (that is `deep`).
5. Emit the single stage artifact, IIK-tagged, with the next-step suggestion.

Skip clarifying questions when the stage and predecessor are clear. Still enforce:
one playbook, one tag family, zero placeholders, script-first.

Example: `topic=00-constitution depth=quick` on a project with a valid
`PREMISE.md` → draft `CONSTITUTION.md`, ≥3 principles, persist
`tdd_determination`, commit, suggest `/iikit-01-specify`.
