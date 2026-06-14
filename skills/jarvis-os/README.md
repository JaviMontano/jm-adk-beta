# jarvis-os — README

Pack paraguas del **Personal Jarvis OS**. Materializa el método *Trabajar Amplificado / MetodologIA* sobre alfa bajo la filosofía **"Method First, (Gen)AI Next. Soberanía digital."**

## Qué hace

Es el **punto de entrada y enrutador** del pack. No produce el artefacto de dominio: aplica el ciclo **COOL** (Clarify · Organize · Optimize · Liberate), detecta el **sector/estación/proyecto** donde vive el trabajo y deriva a la skill, cadencia o scaffolder correcto, marcando *verification tags* inline.

## Cuándo usarlo

- El input es **ambiguo** sobre dónde vive el trabajo (qué sector N0–N4 / estación / proyecto).
- Hay que **enrutar** a un scaffolder (`station-create`, `project-create`…) o a una cadencia (`dbr-daily-plan`…).
- Se quiere el método como **punto de entrada** sin haber nombrado una skill concreta.

## Cuándo NO usarlo

- El usuario ya invocó una skill concreta → delega directo, no re-enrutes.
- Se necesita generar el **artefacto final de dominio** → este pack orquesta, no produce.
- Tocar `user-context/` salvo lectura del routing-map → lo íntimo nunca entra a `skills/` tracked.

## Cómo enruta / ejecuta

1. **Clarify** — absorbe el input externo (email, reunión, decisión, dato) con timestamp + intención.
2. **Organize** — coloca la captura en la ubicación correcta usando la taxonomía estable de 5 sectores.
3. **Optimize** — valida antes de actuar; carga el contexto/modelo/skill correcto.
4. **Liberate** — entrega o deriva al scaffolder/cadencia con precisión.

**Cascada de ruteo** (primer match gana): prefijo explícito → working dir → presencia de `02_Proyectos/`|`01_Estaciones/` → keywords → preguntar al usuario.

## Lectura de estado (obligatoria antes de inferir)

`docs/jarvis-os/` (playbook + runbook) y `user-context/context/routing-map.md` — nunca inferir arquitectura desde caché/historial.

## Estructura del bundle

| Recurso | Para qué |
|---|---|
| `SKILL.md` | Contrato operativo, sectores, cadencias, reglas, gate de validación. |
| `agents/` | `lead` (orquesta COOL), `specialist` (taxonomía/ruteo), `support` (ejecución scaffolders), `guardian` (gates de validación). |
| `knowledge/body-of-knowledge.md` | Conceptos, estándares y reglas de decisión del método. |
| `knowledge/knowledge-graph.json` | Grafo de conceptos clave (COOL, sectores, cadencias, tags…). |
| `prompts/` | `primary`, `meta`, `variations/quick`, `variations/deep`. |
| `templates/output.md` | Scaffold del entregable de ruteo COOL. |
| `evals/evals.json` | Casos de evaluación específicos de ruteo y guardrails. |
| `examples/` | Ejemplo worked de ruteo (input → salida). |
| `assets/` | Rúbrica de calidad y checklist del gate (ver `assets/README.md`). |

## Reglas operativas (resumen)

- **NOW ≤ 3** tareas simultáneas por `TAREAS.md`.
- **Rule-9**: root ≤200, sector ≤60, estación ≤50, proyecto ≤70 líneas de CLAUDE.md.
- **Rule stacking**: root → estación → proyecto, sin repetir.
- **Verification tags** de **una sola familia** por documento (kit `[DOC]`/`[INFERENCIA]`/`[SUPUESTO]` en repo; familia operador en output de usuario).
- **Regla de 3** + **14 días** supervisados antes de codificar/automatizar.

## Skills relacionadas

`input-analysis` · `revisor-veracidad` · `workspace-setup`
