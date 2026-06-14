# Meta prompt — task-subfolder

Guidance for an orchestrator deciding whether and how to invoke
**task-subfolder**.

## Activate when

- The operator wants a task to persist **across sessions** with its own memory.
- They say "crear subtarea", "task-subfolder", or name a `T-NNN`.
- They ask to *complete missing files* for an existing T-NNN folder
  (missing-only fill).

## Do NOT activate when

- The deliverable is single-turn (no durable folder needed).
- They want to author a *skill* under `skills/` → route to `skill-creator`.
- The request explicitly asks to skip validation/evidence → refuse; the gate is
  non-negotiable (this is a no-activation / refuse case).

## Routing

lead → resolve id + create-vs-resume → specialist (draft tagged bodies) →
support (write missing-only) → guardian (gate) → lead (summary).

## Quality contract

- Three parsing Markdown files, unique `T-NNN`, ≥1 acceptance checkbox, exactly
  one creation/resume log entry, no un-forced overwrite, full Jarvis tagging,
  zero Alfa-tag leakage.
- Deterministic backing: `assets/dod-checklist.md`, `assets/quality-rubric.json`.

## Self-correction

- Conflicting requirements → safer reading + `{SUPUESTO}` + next step.
- Id collision / folder exists → resume, append, never recreate.
- Empty goal → `{VACIO_CRITICO}`, stop and ask.
