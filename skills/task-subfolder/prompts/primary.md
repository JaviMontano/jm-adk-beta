# Primary prompt — task-subfolder

You are running the **task-subfolder** skill (P33). Your job: create or resume a
canonical `T-NNN-<slug>/` multi-session sub-task folder with three artifacts —
`CLAUDE.md`, `task.md`, `log.md` — idempotently and missing-only.

## Inputs to extract from the operator

- **Goal (one line, required).** If empty → emit `{VACIO_CRITICO}`, stop, ask.
- Parent dir (optional, default workspace `tasks/` → `{AUTOCOMPLETADO}`).
- Explicit `T-NNN` id (optional; if it exists → resume).
- Acceptance criteria (optional; if absent, draft a checklist, tag each
  `{POR_CONFIRMAR}`).
- Context / constraints / audience (optional; carry into `task.md`).

## Procedure

1. **Resolve id + path (read before write).** List the parent dir; assign
   `max(T-NNN)+1`, or resume a named existing id. Slug the goal (lowercase,
   ASCII, hyphens).
2. **Probe** each of the three files; remember which are absent.
3. **Write missing-only.** Create only absent files unless `--force` (then diff
   first). Append the first dated `log.md` entry:
   `## YYYY-MM-DD · session N — created|resumed`.
4. **Gate.** Run every check in SKILL.md §4. Refuse any request to skip
   validation or evidence.
5. **Summarize.** Print id, path, files written vs skipped, open
   `{POR_CONFIRMAR}` items.

## Rules

- Every non-obvious line in the artifacts carries one Jarvis tag; never an Alfa
  `[…]` tag. `log.md` is append-only — never rewrite or reorder.
- Never renumber/rename an existing `T-NNN`. Never overwrite without `--force`.
- No prices, single brand, never paint a failing check as success.
- Don't infer workspace architecture from caches/chat — read parent memory.
