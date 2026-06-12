# Body of Knowledge — custom-tooling-extension

Dominio: diseño de extensiones de Claude Code de producción (slash commands y
skills). El conocimiento aquí es estable; lo condicional vive en `SKILL.md`.

## 1. Conceptos clave

- **Slash command** — artefacto en `.claude/commands/<nombre>.md`. Se invoca **explícitamente por nombre** (`/nombre arg`). Argumentos posicionales vía `$ARGUMENTS`. Su contexto corre **inline** en la sesión actual. Ideal para acciones cortas y predecibles. [DOC]
- **Skill** — artefacto en `.claude/skills/<nombre>/SKILL.md`. Se activa por **contexto/semántica** vía su `description`. Puede correr con ventana propia (`context: fork`) y herramientas acotadas (`allowed-tools`). Ideal para sub-tareas con disparo no nominal. [DOC]
- **`context: fork`** — corre la skill en una ventana aislada para que la sub-tarea no contamine ni infle la sesión principal. Economía de contexto a cambio de perder el contexto vivo de la sesión. [DOC]
- **`allowed-tools`** — whitelist de herramientas habilitadas. Acota el **blast radius** de operaciones mutadoras. Sin mutación → read-only; con ejecución → `Bash` explícito y justificado. [DOC]
- **`description`** — en una skill funciona como **contrato de routing**: en una sola línea, dice qué la activa. Vaga o multilínea → el router no la activa bien. [DOC]
- **`argument-hint`** — contrato de interfaz: le dice al invocante qué argumentos pasar. [DOC]
- **Scope** — project (`.claude/` versionado, se replica al equipo, pasa por revisión) vs user (`~/.claude/`, ágil pero no llega al equipo). [DOC]
- **Blast radius** — alcance de daño potencial de las operaciones que la extensión puede ejecutar; se acota con la whitelist mínima. [DOC]

## 2. Estándares de frontmatter

- `name` único y estable; es el id. Nunca renombrarlo sin migrar invocaciones. [DOC]
- `description` en una sola línea, con el trigger explícito. [DOC]
- `context: fork` en skills de trabajo no trivial. [DOC]
- `allowed-tools` como lista mínima; read-only por defecto (`Read, Grep, Glob`). [DOC]
- `argument-hint` siempre que el artefacto reciba argumentos. [DOC]
- `version` con minor-bump en cada modificación upgrade-safe. [DOC]

## 3. Reglas de decisión

1. ¿El usuario lo invoca por nombre y es predecible? → **command**. ¿Activación por contexto + ventana propia + herramientas acotadas? → **skill** con `context: fork`. [DOC]
2. ¿Se replica al equipo? → **project scope** (`.claude/` versionado). User scope solo para experimentos personales. [DOC]
3. ¿La operación puede mutar repo/sistema? → whitelist mínima con `Bash` justificado; si no muta, read-only. [DOC]
4. ¿Es una convención permanente del repo? → va en `CLAUDE.md`, no en la skill. [DOC]
5. ¿Falta saber si es de equipo o qué muta? → **pregunta antes de emitir** scope o whitelist. [SUPUESTO]

## 4. Anti-patrones

- Command con activación contextual esperada (los commands solo se invocan por nombre). [INFERENCIA]
- `description` multilínea o vaga (rompe el routing). [INFERENCIA]
- `Bash` en la whitelist sin justificación (blast radius abierto). [DOC]
- Skill que incrusta convenciones permanentes (van en `CLAUDE.md`). [DOC]
- Misma capacidad duplicada como command y skill (drift de comportamiento). [SUPUESTO]
- Artefacto de equipo en user scope (no se replica; cada quien lo recrea). [DOC]

## 5. Taxonomía de evidencia

`[DOC]` regla del modelo de extensiones · `[CONFIG]` valor de frontmatter o ruta
`.claude/` · `[CÓDIGO]` snippet emitido · `[INFERENCIA]` juicio de diseño ·
`[SUPUESTO]` dato faltante que obliga a preguntar.
