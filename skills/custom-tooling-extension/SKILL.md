---
name: custom-tooling-extension
version: 1.1.0
description: "Decidir slash command vs skill y escribir su frontmatter de producción (context fork, allowed-tools whitelist, argument-hint) con el scope correcto, sin contaminar la sesión ni romper la replicabilidad del equipo."
owner: "JM Labs"
last_updated: 2026-06-11
triggers:
  - custom tooling extension
  - slash command authoring
  - skill frontmatter
  - context fork
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Custom Tooling Extension

## Capacidad

Diseñar e implementar extensiones de Claude Code de producción: slash commands (`.claude/commands/X.md`) y skills (`SKILL.md` con `context: fork`, `allowed-tools`, `argument-hint`), eligiendo el artefacto y el scope correctos. La capacidad no es "escribir un `.md`": es **decidir command vs skill** por tipo de disparo y scope, **economizar contexto** con fork, y **acotar el blast radius** de operaciones mutadoras con whitelist de herramientas, sin contaminar la sesión ni romper la replicabilidad del equipo. [DOC]

## Cuándo usarla

- Disparador explícito invocado por nombre (`/comando arg`) → candidato a **slash command**. [DOC]
- Activación por contexto/semántica, con ventana propia y herramientas acotadas → **skill** con `context: fork`. [DOC]
- El artefacto debe **replicarse a todo el equipo** vía repo → scope **project** (`.claude/commands/`, `.claude/skills/`), nunca user. [DOC]
- Una skill ejecuta ops que pueden mutar repo/sistema y hay que restringir el blast radius con `allowed-tools`. [DOC]
- Quieres mover convenciones permanentes (no condicionales) del proyecto fuera de skills, hacia `CLAUDE.md`. [DOC]

**No usarla cuando** (anti-scope): el pedido es de dominio no-tooling (correos, análisis, contenido) [CONFIG: ver evals `negative_*`]; el input está vacío; o piden explícitamente violar las reglas (user scope para artefacto de equipo, sin fork, sin `allowed-tools`) — en ese caso **no actives**: explica el anti-patrón en vez de obedecerlo. [CONFIG: evals `negative_anti_pattern_request`]

## Entradas / Salidas

- **Entrada:** descripción del trigger (¿quién y cómo lo invoca?), si debe replicarse al equipo, qué operaciones ejecuta (lectura vs mutación), y qué argumentos recibe. [INFERENCE]
- **Salida:** (1) decisión command|skill justificada; (2) ruta + scope; (3) frontmatter completo y válido; (4) `allowed-tools` mínimo justificado; (5) checklist de validación resuelto. [INFERENCE]
- **Falta de dato crítico** (no se sabe si es de equipo, o qué muta) → no inventes el scope ni la whitelist: pregunta antes de emitir frontmatter. [SUPUESTO]

## Cómo construir

1. **Clasifica el artefacto.** ¿Disparo explícito y predecible por el usuario? → command. ¿Activación por contexto + economía de ventana + herramientas acotadas? → skill con `context: fork`. [DOC]
2. **Fija el scope.** ¿Se replica al equipo? → `.claude/` versionado (project). User scope **solo** para experimentos personales que NO deben llegar al repo de nadie. [DOC]
3. **Declara la interfaz.** `argument-hint` para que el invocante sepa qué pasar; en skill, `description` como **contrato de routing** (qué la activa, en una línea). [DOC]
4. **Aísla el contexto.** En skills de trabajo no trivial usa `context: fork` para que la sub-tarea no contamine ni infle la sesión principal. [DOC]
5. **Whitelist de herramientas.** `allowed-tools` con el mínimo. Sin mutación → read-only (`Read, Grep, Glob`). Con ejecución → añade `Bash` explícito y **documenta por qué**. [DOC]
6. **Separa convención de capacidad.** Reglas permanentes → `CLAUDE.md`. La skill encapsula solo la capacidad condicional/invocable. [DOC]
7. **Valida con katas y evals** antes de mergear (ver checklist). [DOC]

### Disambiguador command vs skill

| Señal | Command | Skill (`context: fork`) |
|---|---|---|
| Disparo | Explícito por nombre (`/x`) | Por contexto/semántica |
| Argumentos | Posicionales vía `$ARGUMENTS` | `argument-hint` + routing por `description` |
| Contexto | Inline en sesión actual | Ventana aislada (no infla la principal) |
| Mejor para | Acción corta, predecible | Sub-tarea con herramientas acotadas |

[INFERENCE]

## Patrón correcto

```yaml
# .claude/skills/release-notes/SKILL.md  (project scope, versionado)
---
name: release-notes
description: "Genera notas de versión desde git log entre dos tags; se activa al pedir changelog/release notes."
context: fork                 # GOOD: aísla y economiza la ventana principal
argument-hint: "<tag-desde> <tag-hasta>"
allowed-tools:               # GOOD: whitelist mínima; solo lectura + git
  - Read
  - Grep
  - Bash
---
```

```markdown
<!-- .claude/commands/deploy-check.md  (GOOD: disparo explícito, project scope) -->
---
argument-hint: "<env>"
---
Verifica readiness de deploy para $ARGUMENTS. Solo lectura.
```

## Anti-patrón

```yaml
# ANTI: user scope -> no se replica al equipo (cada quien la recrearía)
# ~/.claude/skills/release-notes/SKILL.md
---
name: release-notes
# ANTI: sin context: fork -> la sub-tarea contamina e infla la sesión principal
# ANTI: sin allowed-tools -> ops destructivas sin whitelist (blast radius abierto)
description: "hace cosas con git"   # ANTI: description vaga, no es contrato de routing
---
# ANTI: la skill incrusta convenciones permanentes (van en CLAUDE.md, no aquí)
```

## Edge cases y autocorrección

- **Command con activación contextual** (esperas que se dispare "solo") → mala elección: los commands solo se invocan por nombre. Re-clasifica a skill. [INFERENCE]
- **`description` multilínea o vaga** → el router no activa bien la skill. Reescríbela en una sola línea con el trigger explícito. [INFERENCE]
- **`Bash` en la whitelist sin justificación** → reducir a read-only o añadir la justificación. Whitelist abierta = blast radius abierto. [DOC]
- **Skill que repite convenciones permanentes del repo** → mover a `CLAUDE.md`; la skill solo capacidad condicional. [DOC]
- **Misma capacidad como command y skill duplicados** → consolidar; evita drift de comportamiento entre los dos. [SUPUESTO]

**Disparadores de autocorrección:** si el frontmatter quedó sin `argument-hint`, o `allowed-tools` incluye más de lo necesario, o el scope es user pero el artefacto es de equipo → detente y corrige antes de marcar listo. [INFERENCE]

## Trade-offs (decisiones justificadas)

- **`context: fork` vs inline.** Fork aísla y economiza la ventana pero pierde el contexto vivo de la sesión; úsalo cuando la sub-tarea sea no trivial y autocontenida, no para acciones de una línea. [INFERENCE]
- **Whitelist mínima vs conveniencia.** Acotar `allowed-tools` reduce blast radius a cambio de fricción si luego necesitas otra herramienta; prefiere ampliar deliberadamente sobre abrir por defecto. [DOC]
- **Project vs user scope.** Project replica y versiona (gobernanza) a costa de pasar por revisión; user es ágil pero no llega al equipo. Equipo ⇒ siempre project. [DOC]

## Checklist de validación (gate)

No marques la skill como lista hasta que TODO sea sí (gate operativo en `assets/checklist.md`, rúbrica en `assets/quality-rubric.json`):

- [ ] ¿Elegiste **command vs skill** por trigger (explícito vs contextual) y por scope? [DOC]
- [ ] ¿Scope **project** si el artefacto se replica al equipo? (user no replica) [DOC]
- [ ] ¿`context: fork` en skills de trabajo no trivial (economía de contexto)? [DOC]
- [ ] ¿`allowed-tools` es **whitelist mínima**, read-only salvo justificación explícita para `Bash`/mutaciones? [DOC]
- [ ] ¿`description`/`argument-hint` funcionan como contrato de activación e interfaz? [DOC]
- [ ] ¿Las **convenciones permanentes** viven en `CLAUDE.md` y NO dentro de la skill? [DOC]
- [ ] ¿Frontmatter parsea (YAML válido, `name` único, `description` en una sola línea)? [INFERENCE]

## Paquete determinístico y upgrade-safety

- Declara la extensión en un schema/policy versionado **antes** de escribir `.claude/commands/` o `.claude/skills/`, para que el plan sea reproducible (artefacto, scope, frontmatter, seguridad, validaciones). [SUPUESTO: el harness de assets/scripts puede no estar provisto; si no existe, documenta el plan inline con la misma estructura]
- Ejecuta el verificador de la skill (p. ej. `scripts/check.sh`, si está disponible en el repo) antes de marcarla lista; si no existe, recorre el checklist-gate a mano. [SUPUESTO]
- **Upgrade-safe:** al modificar una extensión existente preserva `name` (id), no rompas referencias cruzadas ni rutas `.claude/`, y haz minor-bump de `version`. Nunca renombres el id ni cambies el scope sin migrar las invocaciones. [DOC]
- **Rechaza:** artefactos de equipo en user scope; skills contextuales sin `context: fork`; herramientas irrestrictas; commands con trigger contextual; frontmatter sin interfaz clara. [DOC]

## Katas y skills relacionadas

- Kata: `katas-custom-commands-skills`. [CONFIG]
- Relacionadas: `session-lifecycle-management`, `validation-retry-design`. [CONFIG]
