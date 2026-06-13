---
name: jarvis
description: "Jarvis OS personal cadences: /jarvis <daily|dbr|wbr|qbr|retro|audit|lab|project|station|task> [args]"
argument-hint: "<cadence> [args]"
---
# /jarvis

Router to jarvis-os pack skills. [DOC] One cadence per invocation.

| `arg` skill | Args |
|-------------|------|
| `daily` daily-close · `dbr` dbr-daily-plan | — |
| `wbr` wbr-weekly-review · `qbr` qbr-quarterly · `retro` weekly-retro · `audit` monthly-audit | period |
| `lab` lab-session · `project` project-create · `station` station-create · `task` task-subfolder | name/slug |

Routing: parse `$1` as cadence; remaining tokens pass to the skill. [INFERENCE]

**Golden Reference first** [DOC]: when the task touches Cosas con IA architecture (memory, sectors, stations, projects, labs, cadences, P-006), read the canonical order (CLAUDE.md → _ESTRUCTURA → _INDICE → MEMORY → memory/_INDICE → TAREAS → active CLAUDE.md) before acting — never infer architecture from caches/history (user CLAUDE.md rule).

Acceptance: cadence resolves to exactly one skill; unknown/empty `$1` → list valid args, do not guess. [ASSUMPTION]
Anti-scope: no multi-cadence batching; no MetodologIA brand work (JM Labs single-brand only); no price output.
