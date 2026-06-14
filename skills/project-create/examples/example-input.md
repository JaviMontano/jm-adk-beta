# Example input — project-create

A real invocation: the user wants to spin up a new project from an intent, with a
partial set of details.

> /project-create
>
> Start a new project: **"Atlas — Fase II"**.
> Objective: consolidate the Atlas data pipelines into one orchestrated DAG.
> Sector: leave default. No P-NNN suggested. No slug suggested.
> The folder does not exist yet under `02_Proyectos/`.

## Context the skill reads

- Project registry (latest free id observed: `P-013`). [CONFIG]
- Parent sector `CLAUDE.md` for `III Core` (default sector). [CONFIG]

## What is intentionally under-specified

- **Slug** — to be derived from the name. [INFERENCE]
- **P-NNN** — to be reserved as the next free id. [INFERENCE]
- **Sector** — defaults to `III Core` (an `[ASSUMPTION]`). [ASSUMPTION]
