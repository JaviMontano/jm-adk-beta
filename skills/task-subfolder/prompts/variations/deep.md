# Deep variation — task-subfolder

Thorough path for ambiguous goals, resumptions, conflicts, or `--force`.

## 1. Context recovery (read before write)

- Read parent memory (`MEMORY.md`, Golden Reference order) — never infer
  architecture from caches/chat. Tag recalled facts `{MEMORIA}`.
- List the parent `tasks/` dir; build the full `T-NNN` map to detect collisions.

## 2. Create vs resume

- Named existing id or matching folder → **resume**: read its `log.md`,
  summarize prior state `{MEMORIA}`, plan the new append entry.
- Otherwise create with `max(T-NNN)+1`.

## 3. Specification with explicit uncertainty

- Draft `task.md` acceptance criteria even if none were given; tag each drafted
  item `{POR_CONFIRMAR}` with a concrete verification step.
- Conflicting requirements → record the conflict in `task.md`, pick the safer
  reading, mark `{SUPUESTO}` + next step.
- Default parent dir → `{AUTOCOMPLETADO}`; pure inferences → `{INFERENCIA}`.

## 4. Idempotent write

- Probe all three files. Missing-only by default.
- `--force` → produce a per-file diff, get confirmation, then overwrite; record
  forced overwrites explicitly in the summary.
- Append (never rewrite/reorder) the `log.md` entry.

## 5. Full gate + summary

- Run every SKILL.md §4 check against `assets/dod-checklist.md`; score with
  `assets/quality-rubric.json`. Refuse any skip-validation request.
- Summary: id, path, written/skipped/forced, open `{POR_CONFIRMAR}`, and any
  unresolved `{SUPUESTO}` with their next steps.
