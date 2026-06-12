<!-- distilled from alfa skills/katas-hierarchical-claude-memory -->
<!-- Memoria jerarquica CLAUDE.md user/team/module con at-imports y precedencia por especificidad de subpath. -->
# Katas Hierarchical Claude Memory

## Qué es

`CLAUDE.md` es la memoria persistente del agente, organizada en tres niveles que cargan en cascada y se apilan, no se reemplazan: [DOC]

- `~/.claude/CLAUDE.md` — nivel **usuario** (preferencias personales; viven en el home, nunca en el repo). [DOC]
- `<repo>/CLAUDE.md` — nivel **equipo** (convenciones compartidas, versionadas con el código). [DOC]
- `<repo>/<subpath>/CLAUDE.md` — nivel **módulo** (reglas locales de un paquete o directorio). [DOC]

Cada nivel se compone modularmente con `@imports` para mantener el archivo principal corto y caché-friendly. La regla más específica gana: `repo/src/CLAUDE.md` sobrescribe `repo/CLAUDE.md`, que se apila sobre `~/.claude/CLAUDE.md`. [DOC]

## Por qué importa (falla que evita)

Repetir convenciones en cada prompt cuesta tokens y diverge entre miembros del equipo. [INFERENCIA] Sin una fuente de verdad por nivel, el agente improvisa: cada sesión reinventa estilo, lints y prohibiciones, y el equipo paga el costo en inconsistencia y retrabajo. [INFERENCIA] Un `CLAUDE.md` monolítico de 2000 líneas con todo inline degrada la caché y dispersa la atención del modelo. [INFERENCIA]

## Modelo mental

- **Más específico gana:** precedencia subpath > repo > user para el scope del proyecto; el nivel más profundo sobrescribe en conflicto, los demás siguen activos. [DOC]
- **Frontera de privacidad:** lo personal (preferencias del usuario) NO va en el repo; va en el home. Versionar preferencias contamina a otros y diverge entre máquinas. [INFERENCIA]
- **Modularidad con `@imports`:** el archivo principal queda corto y estable (mejor caché); cada sección importa archivos chicos en `docs/`. [DOC]
- **Anti-monolito:** todo inline degrada caché y dispersa atención. Modularizar y separar por nivel es la cura. [INFERENCIA]

## Supuestos y límites (anti-scope)

- Asume un agente que resuelve y compone los tres niveles + `@imports`; en un runtime que solo lee un único `CLAUDE.md` la cascada es inerte. [SUPUESTO] Confirmar soporte de imports antes de modularizar.
- `@imports` son include estático, NO retrieval semántico: importar `docs/` enormes reinfla el contexto que se buscaba reducir. Importar lo que casi siempre aplica; lo raro va condicional por ruta. [INFERENCIA]
- NO sustituye guardrails determinísticos (hooks, validación de salida): una regla en `CLAUDE.md` es guía atendida probabilísticamente, no un control que bloquea. [INFERENCIA]
- NO resuelve reglas que dependen del archivo en edición — eso es `katas-path-conditional-rules`. Esta kata ubica memoria por *quién es dueño* (usuario/equipo/módulo), no por *qué glob* matchea. [INFERENCIA]
- La precedencia rige conflictos puntuales; reglas no contradictorias de distintos niveles coexisten activas, no se anulan. [SUPUESTO]

## Activos determinísticos

- Lint de privacidad en CI: fallar si `<repo>/CLAUDE.md` contiene patrones de preferencia personal (p.ej. `ruff over black`, `terse commits`). [INFERENCIA]
- Verificar que cada `@import` resuelve a un archivo existente y versionado; un import roto degrada en silencio a "sin regla". [INFERENCIA]
- Medir longitud del `CLAUDE.md` raíz resuelto (post-imports) contra un presupuesto de líneas como señal de monolito. [SUPUESTO]

## Patrón correcto

```text
# <repo>/CLAUDE.md  (nivel equipo, versionado)
## Style
@docs/style-guide.md

## Testing
@docs/testing-conventions.md

## Forbidden
- never run pip install without venv

# ~/.claude/CLAUDE.md  (nivel usuario, NO versionado)
- terse commits
- ruff over black
```

## Anti-patrón

```text
# <repo>/CLAUDE.md  (ANTI: monolítico + mezcla de niveles)
# 2000 líneas con TODO inline (style + testing + forbidden + ...)
# además incluye preferencias personales del autor:
- terse commits        # <- esto es del usuario, contamina el repo del equipo
- ruff over black      # <- diverge entre máquinas, no es convención de equipo
```

## Modos de falla (qué vigilar)

- **Fuga de privacidad:** preferencias personales commiteadas al repo de equipo; otros heredan tu estilo sin consentirlo. [INFERENCIA]
- **Import roto silencioso:** `@docs/x.md` movido/borrado; la regla desaparece sin error y el agente improvisa. [INFERENCIA]
- **Deriva monolítica:** el raíz crece inline porque "era una línea más"; la caché se invalida en cada commit y la atención se diluye. [INFERENCIA]
- **Conflicto mal diagnosticado:** se asume que el módulo ignora al equipo, cuando solo sobrescribe la clave en disputa; el resto sigue vigente. [SUPUESTO]
- **Ciclo de imports:** A importa B que importa A; el resolvedor puede colgarse o duplicar. Mantener el grafo de imports acíclico. [SUPUESTO]

## Casos límite

- **Misma regla en dos niveles, idéntica:** redundante, no dañina; preferir declararla en el nivel más alto que aplica a todos. [INFERENCIA]
- **Monorepo con subpaths heterogéneos:** un `CLAUDE.md` por paquete es correcto; el raíz solo lleva lo universal del repo. [INFERENCIA]
- **Preferencia que el equipo sí quiere estandarizar** (p.ej. `ruff`): deja de ser preferencia personal y sube al repo como convención. [INFERENCIA]

## Argumento de certificación

Separación estricta usuario/equipo/módulo y uso de `@imports` para modularidad y caché-friendliness. El agente certifica cuando: las preferencias personales viven solo en el home, las convenciones de equipo en el repo, las reglas locales en el módulo, y el raíz se mantiene corto vía `@imports` en lugar de inline monolítico. [DOC]

## Criterios de aceptación

- `grep` de patrones de preferencia personal sobre `<repo>/CLAUDE.md` retorna vacío. [INFERENCIA]
- Cada `@import` del raíz resuelve a un archivo versionado existente. [INFERENCIA]
- Dado un conflicto subpath vs repo, el agente aplica la regla del subpath y conserva las no contradictorias del repo. [SUPUESTO]
- El `CLAUDE.md` raíz resuelto se mantiene bajo el presupuesto de líneas acordado. [SUPUESTO]

## Cuándo activar

- Diseñar o auditar la memoria persistente de un proyecto con `CLAUDE.md`. [DOC]
- Decidir dónde colocar una convención (¿usuario, equipo o módulo?). [DOC]
- Refactorizar un `CLAUDE.md` monolítico hacia `@imports` modulares. [DOC]
- Resolver precedencia entre niveles que entran en conflicto. [DOC]

## Skills relacionadas

- `katas-path-conditional-rules`
- `katas-context-cache-discipline`
- `katas-subagent-isolation`
