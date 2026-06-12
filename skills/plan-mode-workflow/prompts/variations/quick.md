# Prompt — Quick (plan-mode-workflow)

Variación rápida: produce el **núcleo del gate de dos modos** en una pasada, sin
profundizar en taxonomía ni edge cases. Úsala cuando el repo es pequeño y el
aprobador ya está identificado.

## Pide solo lo esencial

- Objetivo del cambio (si falta → detente y pide; no fabriques plan).
- Repo objetivo y aprobador.

## Entrega en 5 puntos

1. Estado: `mode = "plan"`, `signed_plan_hash = null`. [CÓDIGO]
2. Write-blocklist mínima: `Write`, `Edit`, `MultiEdit`, `NotebookEdit` + Bash
   mutante (`rm `, `sed -i`, `>`). Fail-closed. [CONFIG]
3. `plan.md` corto: objetivo, archivos a tocar, criterio de aceptación, riesgos. [DOC]
4. Evento de firma `{ hash, approved_by, plan_signed_at }`; `approve_plan(hash)`
   → `execute`. [CÓDIGO]
5. Hook `PreToolUse`: deny write-tools en `plan`; hash-mismatch revierte a `plan`. [CÓDIGO]

Sin precios. Single-brand (JM Labs). Si la tarea no escribe a repo, no actives el gate.
