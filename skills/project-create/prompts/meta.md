# Meta prompt — project-create

Guidance for the orchestrator on how to invoke and constrain project-create.

## Routing

- Activate when an intent asks to start/create a **project** that does not yet
  exist under `02_Proyectos/<slug>/`. [INFERENCE]
- Do NOT activate for: an existing project (route to its cadence), a sector or
  station (`station-create`), or a one-off task inside a project
  (`task-subfolder`). [DOC]

## Pre-flight checks

- Is the intent non-empty? If not, the skill will `{VACIO_CRITICO}`-stop. [DOC]
- Is there an active workspace? If a placement guard would deny the write, run
  `workspace-manager.sh ensure` first. [CONFIG]

## Self-correction triggers

- About to write a file that already exists → switch to missing-only, re-read it. [DOC]
- `CLAUDE.md` draft > 70 lines → refactor into `MEMORY.md`/links before writing. [INFERENCE]
- Slug or id collision → surface and ask; do not silently rename or reuse. [INFERENCE]

## Quality bar

The run is acceptable only if the guardian's acceptance gate passes in full.
Never report a failing gate as success. [DOC]

## Governance

Single-brand (JM Labs), no prices, no client PII in seeds, Alfa-core evidence
tags throughout. [DOC]
