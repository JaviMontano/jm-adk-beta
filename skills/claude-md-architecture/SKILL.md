---
name: claude-md-architecture
version: 1.1.0
description: "Estructurar memoria jerarquica CLAUDE.md user/team/module con at-imports y reglas condicionales por glob de ruta, optimizada para cache KV y precedencia por subpath."
owner: "JM Labs"
triggers:
  - claude md architecture
  - hierarchical memory
  - path scoped rules
  - memory imports
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Claude Md Architecture

## Capacidad

Diseñar la memoria persistente de un proyecto Claude Code como una jerarquía explícita de archivos `CLAUDE.md` en tres niveles (user, team, module), conectados por `@imports` y complementados con reglas condicionales por glob de ruta. La meta de ingeniería: las reglas universales viven siempre en el **prefijo cacheable** (raíz estable), mientras que las heurísticas de un subárbol se cargan solo cuando el trabajo toca ese subárbol. El resultado en producción es una memoria que no crece sin control, que respeta la precedencia por subpath y que mantiene la economía de contexto (cache KV) en cada turno. [DOC]

## Cuándo usarla (triggers)

- El `CLAUDE.md` del repo superó ~300 líneas y empieza a cargar reglas que solo aplican a un módulo. [SUPUESTO]
- Hay reglas que deben aplicar solo a `frontend/**`, `infra/**` o `tests/**`, y hoy viven en un único archivo global.
- Preferencias personales (tono, atajos individuales) se están filtrando al repo de equipo versionado.
- Se necesita separar política de equipo (versionada) / preferencia de usuario (no versionada) / contrato de módulo.

**No usarla cuando** (anti-scope): el repo es un solo módulo sin subárboles divergentes (jerarquía = sobre-ingeniería); el problema real es *contenido* de reglas, no su *ubicación*; o se pide editar `~/.claude/CLAUDE.md` global del usuario sin su confirmación explícita. [INFERENCIA]

## Inputs / Outputs

- **Input**: ruta del repo; `CLAUDE.md` actual; lista de subárboles con reglas propias; opcional `assets/architecture-policy.json`. [CONFIG]
- **Output**: `CLAUDE.md` raíz lean + un `module/CLAUDE.md` por subárbol + bloque `@imports` + tabla de precedencia documentada + reporte reproducible vía script. [DOC]

## Cómo construir

1. Inventaría las reglas actuales y clasifícalas en tres cubos: **universal** (siempre), **por-módulo** (subárbol concreto), **por-usuario** (preferencia personal no versionada). Una regla mal clasificada es la causa raíz de cache thrashing. [INFERENCIA]
2. Crea el `CLAUDE.md` raíz de equipo solo con universales más un bloque de `@imports` hacia los módulos. Mantén el raíz lean y estable: es el prefijo que se cachea. **Trade-off**: cada línea volátil en el raíz invalida el prefijo KV de *todos* los turnos, no solo del afectado — por eso lo estable vive arriba. [INFERENCIA]
3. Por cada módulo con reglas propias, crea `module/CLAUDE.md` con reglas activadas por glob (p. ej. `apply to: "src/api/**"`), **no** copiadas al raíz.
4. Mueve las preferencias personales a `~/.claude/CLAUDE.md` (user scope) e impórtalas con `@import`; nunca al repo del equipo.
5. Define la precedencia: la regla más específica por subpath gana; documenta el orden de resolución en una tabla para que sea predecible y auditable.
6. Verifica que el prefijo (raíz + imports universales) no contenga valores por-turno ni reglas que solo apliquen a un subárbol.

## Patrón correcto

```markdown
# team CLAUDE.md (versioned, stable prefix)
@import ./CONVENTIONS.md          # universal, always loaded
@import ~/.claude/CLAUDE.md       # user prefs, not in repo

## Rules (universal)
- Conventional commits; never push to main directly.

## Path-scoped rules
- apply to: "frontend/**"  ->  @import ./frontend/CLAUDE.md
- apply to: "infra/**"     ->  @import ./infra/CLAUDE.md
```

```markdown
# frontend/CLAUDE.md (loaded only when work touches frontend/**)
- Use the design-system tokens; no inline styles.
- Co-locate tests as *.test.tsx next to the component.
```

## Anti-patrón

```markdown
# CLAUDE.md (ANTI: monolithic, 2000 lines, always loaded)
- Use design-system tokens.        # only relevant to frontend
- Prefer pnpm over npm.            # personal preference, leaked into repo
- ABAP naming is Z-prefixed.       # only relevant to one legacy module
- ...1990 more lines that load on every single turn, blowing the cache...
```

Otros anti-patrones: glob no recursivo (`frontend/*` en vez de `frontend/**`) que omite subcarpetas; `@import` a una ruta volátil (timestamp, branch activo) que rompe el prefijo cada turno; precedencia ambigua entre dos globs que solapan sin regla de desempate. [INFERENCIA]

## Casos límite

- **Globs que solapan** (`src/**` y `src/api/**` ambos con reglas): el más específico gana; si no se puede ordenar por especificidad, declara el desempate explícito en la tabla de precedencia. [SUPUESTO]
- **Import circular** entre módulos: prohibido; el grafo de `@imports` debe ser un DAG, valídalo antes de escribir. [INFERENCIA]
- **Import roto** (ruta inexistente tras un rename): el script debe fallar, no degradar en silencio. [DOC]
- **Monorepo con N módulos**: no crees `module/CLAUDE.md` vacíos; solo donde haya ≥1 regla propia, o añades ruido al grafo. [INFERENCIA]

## Self-correction triggers

Detente y reclasifica si: una regla aparece copiada en raíz **y** módulo (deduplica al nivel correcto); el raíz vuelve a crecer >300 líneas (señal de universal mal asignado); un `@import` apunta a algo no versionado dentro del repo de equipo (fuga de scope); o un glob no usa `**` cuando el subárbol tiene subcarpetas. [INFERENCIA]

## Gate de aceptación (validación)

Marca la skill como lista **solo si todo** se cumple:

- [ ] Separación clara user / team / module en archivos distintos. [DOC]
- [ ] `@imports` estables y cache-friendly (sin valores por-turno en el prefijo). [INFERENCIA]
- [ ] Reglas de subárbol activadas por glob recursivo (`**`), no copiadas al raíz.
- [ ] Precedencia por subpath definida en tabla y predecible (más específico gana; desempates explícitos).
- [ ] Preferencias personales fuera del repo de equipo (user scope).
- [ ] Grafo de `@imports` es un DAG sin imports rotos ni circulares.
- [ ] `bash skills/claude-md-architecture/scripts/check.sh` pasa en verde funcional (no solo sin error). [CONFIG]

## Paquete deterministico

- Usa `assets/architecture-schema.json` y `assets/architecture-policy.json` para **declarar** la arquitectura antes de escribir archivos (ontology-first: declara, luego compila). [CONFIG]
- Ejecuta `scripts/compile-claude-md-architecture.py <arquitectura.json> --output <reporte.md>` para generar un reporte reproducible con `CLAUDE.md` raíz y módulos.
- Ejecuta `bash skills/claude-md-architecture/scripts/check.sh` antes de marcar la skill como lista.
- Rechaza raíces monolíticas, imports inestables, globs no recursivos, precedencia ambigua y preferencias personales versionadas en el repo.

## Katas y skills relacionadas

- Katas: `katas-08`, `katas-09`.
- Relacionadas: `katas-hierarchical-claude-memory`, `katas-path-conditional-rules`, `context-window-engineering`.
