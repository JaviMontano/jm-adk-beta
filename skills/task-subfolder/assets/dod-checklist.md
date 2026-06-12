# Deterministic DoD checklist — task-subfolder

Binary gate the guardian runs before declaring "done". Each item is a yes/no
check against the produced `T-NNN-<slug>/` folder. Any `no` blocks completion.

## Existence & structure
- [ ] `CLAUDE.md`, `task.md`, `log.md` all exist under `T-NNN-<slug>/`.
- [ ] All three parse as valid Markdown (no truncated code fences).

## Identity
- [ ] `T-NNN` id is unique in the parent `tasks/` dir (no collision).
- [ ] Folder name matches `T-NNN-<slug>` with an ASCII, hyphenated slug.
- [ ] No existing `T-NNN` was renamed or renumbered.

## Specification
- [ ] `task.md` contains ≥1 acceptance-criteria checkbox (`- [ ]`).
- [ ] Drafted (un-confirmed) criteria are tagged `{POR_CONFIRMAR}`.
- [ ] Empty goal was NOT fabricated past (`{VACIO_CRITICO}` honored).

## Journal
- [ ] `log.md` has exactly one creation/resume entry for this run.
- [ ] On resume, prior entries were appended-to, not rewritten or reordered.

## Idempotency
- [ ] No pre-existing file was overwritten without `--force`.
- [ ] `--force` overwrites were diffed and listed in the summary.

## Evidence & governance
- [ ] Every non-obvious line carries exactly one Jarvis tag.
- [ ] No Alfa `[…]` tag leaked into any artifact.
- [ ] No prices emitted; single brand (JM Labs); no failing check shown as pass.
