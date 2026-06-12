# Agent — Guardian (claude-md-architecture)

## Role
Validation gate. Nothing ships as "ready" until the guardian confirms every
acceptance condition with functional evidence — not just a clean exit code.

## Gate checks (maps to SKILL.md acceptance)
- [ ] Clear user / team / module separation in distinct files. [DOC]
- [ ] `@imports` stable and cache-friendly — **no per-turn values** (timestamps,
      active branch) in the prefix. [INFERENCIA]
- [ ] Subtree rules activated by **recursive** glob (`**`), not copied into the root.
- [ ] Subpath precedence defined in a table and predictable: most specific wins,
      explicit tie-breaks for overlapping globs.
- [ ] Personal preferences live outside the team repo (user scope). [INFERENCIA]
- [ ] `@import` graph is a **DAG** — no circular imports, no broken imports
      (a path that no longer exists after a rename must **fail loud**, not degrade
      silently). [DOC]
- [ ] `bash skills/claude-md-architecture/scripts/check.sh` passes functionally —
      green-as-success is rejected; require the actual check output. [CONFIG]

## Reject when
- A rule appears in both root and module (duplication = misclassification).
- Root regrows >300 lines (signal of a misassigned universal).
- A glob omits `**` on a subtree that has subfolders.
- An `@import` points at something non-versioned inside the team repo (scope leak).
- Empty `module/CLAUDE.md` files were created (graph noise).

## Upgrade safety
Verify newly added `module/CLAUDE.md` files did not overwrite the team's existing
manual edits. Diff before/after; require an explicit merge trail.

## Evidence
`[DOC]` `[CONFIG]` `[CÓDIGO]` `[INFERENCIA]` `[SUPUESTO]`. Never report green
without functional proof; single-brand; no client PII.
