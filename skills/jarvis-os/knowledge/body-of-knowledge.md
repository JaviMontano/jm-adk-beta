# Body of Knowledge — jarvis-os

Conocimiento de dominio del pack paraguas **Personal Jarvis OS** (método Trabajar Amplificado / MetodologIA). Filosofía rectora: **"Method First, (Gen)AI Next. Soberanía digital."**

## 1. Conceptos clave

### COOL — el ciclo operativo
- **Clarify**: absorber input externo con timestamp + intención.
- **Organize**: colocar la captura en la ubicación correcta usando taxonomía estable.
- **Optimize**: validar antes de actuar; cargar el contexto/modelo/skill correcto.
- **Liberate**: producir y entregar (o derivar) el artefacto con precisión.

**Invariante**: `Organize + Optimize` = motor estable; `Clarify + Liberate` se adaptan por dominio. [DOC]

### Cinco sectores (capas N0–N4)
| Sector | Capa | Carpeta | Scaffolder | Naturaleza |
|---|---|---|---|---|
| I Foundations | N0 | `00_Recursos/` | `jarvis-bootstrap` | Recursos transversales estables |
| II Base | N1 | `01_Estaciones/` | `station-create` | Áreas de vida/operación continuas |
| III Core | N2 | `02_Proyectos/` | `project-create` | Esfuerzos con inicio/fin |
| IV R&D+i | N3 | `03_Lab/` | `lab-session` | Experimentación, Regla de 3 |
| V Maintenance | N4 | `04_Cadencias/` | cadence skills | Ritmos de revisión |

### Cadencias (6 codificadas)
`dbr-daily-plan` (P09) · `daily-close` (P10) · `wbr-weekly-review` (P11) · `weekly-retro` (P12) · `qbr-quarterly` (P13) · `monthly-audit` (P22). MBR/ABR viven documentadas en el runbook. [DOC]

### Foundation skills (4, reuso transversal)
`input-analysis` · `revisor-veracidad` · `frontload-prompt` · `cierre-conversacion`. [DOC]

### Scaffolders
`jarvis-bootstrap` · `station-create` · `project-create` · `lab-session` · `task-subfolder`. [DOC]

## 2. Estándares y reglas de decisión

### Cascada de ruteo (primer match gana)
1. Prefijo explícito (`/jarvis-os …`, sector nombrado).
2. Working directory actual.
3. Presencia de `02_Proyectos/` o `01_Estaciones/`.
4. Keywords del input.
5. **Preguntar al usuario** (default cuando todo lo anterior falla).

### Reglas operativas
- **NOW ≤ 3**: máximo 3 tareas simultáneas en cualquier `TAREAS.md`.
- **Rule stacking**: reglas se apilan root → estación → proyecto; cada capa especializa sin repetir.
- **Rule-9 (tamaño de CLAUDE.md)**: root ≤200, sector ≤60, estación ≤50, proyecto ≤70 líneas.
- **Regla de 3**: codificar una skill solo tras ejecutar el patrón 3+ veces.
- **14 días** en modo supervisado antes de automatizar una tarea programada.

### Verification tags — dos familias, nunca mezclar
- **Familia kit** (repo): `[DOC]` (leído), `[INFERENCIA]` (deducido), `[SUPUESTO]` (asunción).
- **Familia operador** (output a usuario): convención de audiencia humana.
- Regla: **una sola familia por documento**, elegida por audiencia (`references/verification-tags.md`). [DOC]

### Frontera de soberanía digital
- Lo íntimo vive en `user-context/`; **nunca** en `skills/` tracked.
- `user-context/context/routing-map.md` solo se **lee**.
- Sin secretos en archivos versionados.

## 3. Modelo de madurez

### 12 niveles de adopción
Chat → Chat+prompts → Chat Projects → Cowork → Cowork Projects → **Skills** → Plugins → Mini-apps → Plugin engineering → Orchestrator Station → Web mini-apps → **Portabilidad** (soberanía digital). Regla: subir solo cuando el nivel actual sea estable; bajar es válido si el contexto lo pide. [INFERENCIA]

### 8 capacidades (Anthropic)
Acceso a archivos · memoria persistente · conectores MCP · Skills · Cowork Projects · extensión navegador · tareas programadas · Dispatch móvil. [DOC]

## 4. Reglas de gobernanza del pack

- El pack **orquesta y deriva**, no produce el artefacto de dominio.
- **No re-enrutar** si el usuario ya nombró una skill concreta.
- **Leer estado primero**: `docs/jarvis-os/` + routing-map; nunca inferir desde caché/historial.
- Sector indeterminado → preguntar, no autoasignar.
