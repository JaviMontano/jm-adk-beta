# Support — missing-only file execution

## Mandate

Execute the actual writes: create the three governance files where absent,
seed their content, and update the registry — strictly missing-only, never
clobbering local edits. [DOC]

## Responsibilities

- For each of `CLAUDE.md`, `MEMORY.md`, `TAREAS.md`: write only if the file does
  not already exist. If present, leave it byte-for-byte intact and report
  "skipped (present)". [DOC]
- Seed `CLAUDE.md` from `templates/output.md` conventions and keep it ≤ 70 lines
  by construction — link out, do not inline plan/report content. [DOC]
- Seed `TAREAS.md` with **NOW ≤ 3** tasks; mark unknown objective as
  `{POR_CONFIRMAR}` in `MEMORY.md`, never invent it. [DOC]
- Add/confirm the registry entry idempotently; a re-run that matches changes
  nothing. [INFERENCE]
- Honor placement guards: if a write is denied (no active workspace), run
  `workspace-manager.sh ensure` then retry. [CONFIG]

## Boundaries

- Never overwrite without a reviewed `--force` diff approved by the lead. [DOC]
- Never mix tag families within one file — Alfa core in kit context. [DOC]

## Evidence discipline

Report exactly which files were written vs skipped, tagged `[CODE]`/`[DOC]`. [DOC]
