---
name: jarvis-os
version: 0.2.0
last_updated: 2026-06-11
description: "Pack paraguas del Personal Jarvis OS: aplica COOL, detecta sector/estación, enruta a las skills del pack y materializa el método Trabajar Amplificado sobre alfa."
owner: "JM Labs"
triggers:
  - jarvis-os
  - jarvis
  - trabajar-amplificado
  - personal-jarvis
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# Jarvis OS — Pack paraguas

Materializa el método **Trabajar Amplificado / MetodologIA Personal Jarvis OS** sobre alfa. Filosofía: *"Method First, (Gen)AI Next. Soberanía digital."* La guía completa vive en `docs/jarvis-os/` (playbook + runbook). [DOC]

## Cuándo usar (y cuándo NO)

Usa este pack cuando el input sea ambiguo sobre **dónde** vive el trabajo (qué sector/estación/proyecto), cuando haya que **enrutar** a un scaffolder o cadencia, o como punto de entrada al método. [INFERENCIA]

- **NO** lo uses si el usuario ya invocó una skill concreta (`station-create`, `dbr-daily-plan`, etc.): delega directo, no re-enrutes. [INFERENCIA]
- **NO** generes contenido de dominio aquí; este pack orquesta y deriva, no produce el artefacto final. [SUPUESTO]
- **NO** toques `user-context/` salvo lectura del routing-map; lo íntimo nunca entra a `skills/` tracked. [DOC]

## Entradas / Salidas

- **Entrada**: input externo (email, reunión, decisión, dato) o petición de método; opcional sector/estación explícito. [DOC]
- **Salida**: ruteo resuelto (sector + scaffolder/cadencia/foundation skill a invocar) o estructura materializada, con verification tags inline. [INFERENCIA]
- **Estado leído primero**: `docs/jarvis-os/` y `user-context/context/routing-map.md` antes de inferir arquitectura — nunca desde caché/historial. [DOC]

## Principios COOL

- **Clarify** — absorber input externo con timestamp + intención.
- **Organize** — colocar la captura en la ubicación correcta usando taxonomía estable.
- **Optimize** — validar antes de actuar; cargar el contexto/modelo/skill correcto.
- **Liberate** — producir y entregar el artefacto con precisión.

`Organize + Optimize` = motor estable; `Clarify + Liberate` se adaptan por dominio. [DOC]

## Cinco sectores (N0–N4)

| Sector | Capa | Carpeta | Skill scaffolder |
|---|---|---|---|
| I Foundations | N0 | `00_Recursos/` | `jarvis-bootstrap` |
| II Base | N1 | `01_Estaciones/` | `station-create` |
| III Core | N2 | `02_Proyectos/` | `project-create` |
| IV R&D+i | N3 | `03_Lab/` | `lab-session` |
| V Maintenance | N4 | `04_Cadencias/` | cadence skills |

**Decisión de ruteo** (en orden, primer match gana): prefijo explícito → working dir → presencia de `02_Proyectos/`|`01_Estaciones/` → keywords → preguntar al usuario. [INFERENCIA]

## Cadencias (6)

`dbr-daily-plan` (P09) · `daily-close` (P10) · `wbr-weekly-review` (P11) · `weekly-retro` (P12) · `qbr-quarterly` (P13) · `monthly-audit` (P22). MBR/ABR documentadas en runbook. [DOC]

## Foundation skills (4)

`input-analysis` (reuso) · `revisor-veracidad` · `frontload-prompt` · `cierre-conversacion`. [DOC]

## Reglas operativas

- **NOW ≤ 3** tareas simultáneas en cualquier `TAREAS.md`.
- **Rule stacking**: root → estación → proyecto; cada capa especializa sin repetir.
- **Rule-9 (tamaño CLAUDE.md)**: root ≤200, sector ≤60, estación ≤50, proyecto ≤70 líneas.
- **Verification tags** inline: familia kit (`[DOC]`/`[INFERENCIA]`/`[SUPUESTO]`) en repo, familia operador en output de usuario; nunca mezclar (`references/verification-tags.md`). [DOC]
- **Regla de 3**: codificar una skill solo tras ejecutar el patrón 3+ veces.
- **14 días** en modo supervisado antes de automatizar una tarea programada.

## 12 niveles de adopción

Chat → Chat+prompts → Chat Projects → Cowork → Cowork Projects → **Skills** → Plugins → Mini-apps → Plugin engineering → Orchestrator Station → Web mini-apps → **Portabilidad** (soberanía digital). Sube un nivel solo cuando el actual sea estable; bajar es válido si el contexto lo pide. [INFERENCIA]

## 8 capacidades (Anthropic)

Acceso a archivos · memoria persistente · conectores MCP · Skills · Cowork Projects · extensión navegador · tareas programadas · Dispatch móvil. [DOC]

## Orquestación

El agente `jarvis-orchestrator` (en `agents/`) aplica COOL, detecta sector/estación, hace rule-stacking y marca verification tags. El ruteo personal del operador (íntimo) vive en `user-context/context/routing-map.md`. [DOC]

## Scaffolders

`jarvis-bootstrap` · `station-create` · `project-create` · `lab-session` · `task-subfolder`. [DOC]

## Ejemplo

Input: *"jarvis: llegó un email para definir el alcance del proyecto Atlas."* → **Clarify** (captura email + intención) → **Organize** (sector III Core, `02_Proyectos/atlas/`) → si no existe, invocar `project-create`; si existe, derivar a la cadencia/skill del proyecto → tags inline. [INFERENCIA]

## Validación (acceptance gate)

Activos de soporte: `assets/quality-rubric.json` y `assets/checklist.md` (ver `assets/README.md`). [DOC]

Marcar completo solo si TODO se cumple — si no, autocorregir y reintentar:

- [ ] Estructura generada respeta sectores N0–N4 y nombres **kebab-case**. [DOC]
- [ ] **NOW ≤ 3** y **rule-stacking** preservados; ningún CLAUDE.md excede Rule-9. [DOC]
- [ ] Sin secretos; contenido íntimo en `user-context/`, nunca en `skills/` tracked. [DOC]
- [ ] Verification tags presentes y de **una sola familia** por documento. [DOC]
- [ ] Ruteo resuelto a una skill/cadencia concreta, o pregunta explícita al usuario si hubo ambigüedad. [INFERENCIA]

## Triggers de autocorrección

- Sector indeterminado tras la cascada de ruteo → **preguntar**, no autoasignar. [INFERENCIA]
- Se intentó escribir lo íntimo en `skills/` → abortar y redirigir a `user-context/`. [DOC]
- CLAUDE.md sobrepasa Rule-9 → dividir/especializar antes de continuar. [INFERENCIA]
- Mezcla de familias de tags detectada → normalizar a la familia correcta por audiencia. [DOC]

## Anti-patrones

- Producir el artefacto de dominio dentro del pack en vez de derivar. [SUPUESTO]
- Inferir arquitectura desde caché/historial en lugar de leer `docs/jarvis-os/` y el routing-map. [DOC]
- Automatizar una tarea antes de los 14 días supervisados o codificar una skill con < 3 ejecuciones del patrón. [DOC]
- Re-enrutar cuando el usuario ya nombró la skill concreta. [INFERENCIA]

## Related Skills

- `input-analysis`
- `revisor-veracidad`
- `workspace-setup`
