# Ejemplo — output (jarvis-os)

Resultado del ruteo para el input del email del proyecto Atlas. Familia de tags: **kit**, única.

## 1. Clarify
- **Input capturado**: email de cliente sobre alcance del proyecto Atlas (próxima fase).
- **Timestamp**: 2026-06-12 09:14
- **Intención declarada**: definir alcance de la siguiente fase de Atlas.

## 2. Estado leído (antes de inferir)
- `docs/jarvis-os/`: playbook confirma sector **III Core → `02_Proyectos/`** vía `project-create`. [DOC]
- `user-context/context/routing-map.md`: sin override personal para "Atlas". [DOC]

## 3. Organize — cascada de ruteo
| Paso | Resultado |
|---|---|
| 1. Prefijo explícito | No (solo `jarvis:`) |
| 2. Working dir | `~/Cosas con IA` (raíz, no resuelve) |
| 3. Presencia `02_Proyectos/atlas/` | **No existe** → proyecto nuevo |
| 4. Keywords | "proyecto", "alcance", "fase" → esfuerzo con inicio/fin |
| 5. Preguntar | No necesario; keywords convergen a N2 |

- **Sector resuelto**: III Core / N2 [INFERENCIA]
- **Ubicación**: `02_Proyectos/atlas/`

## 4. Optimize — acceptance gate
- [x] Sectores N0–N4 + kebab-case (`atlas`) [DOC]
- [x] NOW ≤ 3 (no se añaden tareas aún) [DOC]
- [x] Rule-stacking preservado (root → proyecto) [DOC]
- [x] Rule-9 respetado (proyecto ≤70 líneas en su CLAUDE.md) [DOC]
- [x] Sin secretos; nada íntimo en `skills/` [DOC]
- [x] Una sola familia de tags [DOC]
- [x] Ruteo concreto resuelto [INFERENCIA]

## 5. Liberate — derivación
- **Ruta objetivo**: `project-create`
- **Acción**: invocar `project-create` con `slug=atlas`, sector III Core. El documento de alcance lo producirá la skill del proyecto, no este pack. [DOC]
- **Estructura materializada (a crear por el scaffolder)**:
  ```
  02_Proyectos/atlas/
    CLAUDE.md        # ≤70 líneas (Rule-9)
    TAREAS.md        # NOW ≤ 3
  ```

## 6. Autocorrecciones aplicadas
- Ninguna: la cascada convergió sin ambigüedad residual.

## 7. Próximos pasos
- Ejecutar `project-create slug=atlas`.
- Tras crear el proyecto, derivar la captura del email a la cadencia/skill de definición de alcance del proyecto Atlas.
