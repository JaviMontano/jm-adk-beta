<!-- distilled from alfa skills/katas-custom-commands-skills -->
<!-- Slash commands vs skills: context fork, allowed-tools whitelist y argument-hint; convenciones permanentes van en CLAUDE.md. -->
# Kata 24 · Slash Commands Custom y Skills

## Qué es

Claude Code ofrece dos mecanismos de extensión distintos. Los slash commands viven en `.claude/commands/X.md` y se disparan explícitamente escribiendo `/X`. Las skills viven en `.claude/skills/X/SKILL.md` y se activan on-demand cuando el modelo detecta que la metadata del frontmatter encaja con la tarea. [DOC] El frontmatter de una skill declara su contrato operativo: `context: fork` aísla la ejecución en un sub-agente, `allowed-tools` define la whitelist de herramientas permitidas, y `argument-hint` documenta los argumentos esperados. [DOC]

## Por qué importa (falla que evita)

- Un command en `~/.claude/commands/` no se replica al equipo: solo existe en la máquina de quien lo creó; el resto nunca lo recibe vía git. [DOC]
- Una skill sin `context: fork` contamina la sesión principal con output verbose: un análisis exploratorio puede inyectar ~5000 tokens de ruido en el contexto activo. [INFERENCIA]
- Una skill sin `allowed-tools` puede escribir o borrar archivos por accidente: nada limita las operaciones destructivas disponibles. [INFERENCIA]
- Meter una convención siempre-aplicable en una skill/command la vuelve opt-in: deja de aplicarse cuando nadie la invoca. [INFERENCIA]

## Modelo mental

- Slash command = trigger explícito que el usuario invoca; skill = workflow on-demand con metadata que el modelo decide activar. [DOC]
- Project scope (`.claude/`) viaja con git y llega a todo el equipo; user scope (`~/.claude/`) es personal y no se comparte. [DOC]
- `context: fork` aísla la skill en un sub-agente → economía de contexto: el output verbose no contamina la sesión principal. [INFERENCIA]
- `allowed-tools` es una whitelist que limita por diseño: una skill exploratoria con `[Read, Grep, Glob]` no puede `Write` ni `Bash`. [DOC]
- Convenciones siempre-aplicables → CLAUDE.md (reglas permanentes, siempre cargadas); skills → workflows on-demand; commands → atajos invocados a mano. [INFERENCIA]

## Supuestos y límites

- **Activación por metadata, no garantizada.** El modelo decide activar una skill leyendo `name`+`description`; una descripción vaga o solapada con otra skill provoca no-activación o activación cruzada. La descripción es la superficie de match: trátala como API, no como adorno. [INFERENCIA]
- **`context: fork` no comparte estado.** El sub-agente devuelve solo su resumen final; no hereda variables ni archivos abiertos de la sesión padre más allá del prompt de invocación. No lo uses para flujos que necesiten ida y vuelta con el contexto principal. [SUPUESTO]
- **Anti-scope.** Esta kata cubre custom commands y skills locales (`.claude/`/`~/.claude/`); NO cubre selección de built-in tools (Grep/Read/Edit) ni configuración de MCP servers (ver skills relacionadas). [DOC]
- **`allowed-tools` filtra, no eleva.** Restringe el set disponible; nunca otorga permisos que la sesión no tenga. Omitirlo hereda TODO el toolset, incluidos los destructivos. [SUPUESTO]

## Patrón correcto

```
# .claude/skills/codebase-analysis/SKILL.md
---
name: codebase-analysis
description: "Mapea estructura y dependencias de un módulo o feature."
context: fork
allowed-tools: ["Read", "Grep", "Glob"]
argument-hint: "<dir-or-feature>"
---
# El body hace Glob -> Grep -> devuelve un resumen tipado.
# context:fork aísla los ~5000 tokens de exploración en un sub-agente.
# allowed-tools sin Write ni Bash impide mutaciones por accidente.
```

## Anti-patrón

```
# ~/.claude/skills/codebase-analysis/SKILL.md   (user scope: NO replica al equipo)
---
name: codebase-analysis
# sin context: fork  -> 5000 tokens contaminan la sesión principal
# sin allowed-tools  -> puede Write/Bash y borrar por accidente
---
```

## Edge cases y modos de falla

- **Command en user scope que el equipo "no tiene".** El autor lo usa, nadie más lo ve; el síntoma es "a mí me funciona". Decisión: si sirve al equipo va en `.claude/commands/` versionado; `~/.claude/` solo para atajos personales. [DOC]
- **Skill que nunca se activa.** `description` genérica o redundante → el modelo no la elige. Decisión: descripción específica con el disparador concreto, sin solaparse con otra skill. [INFERENCIA]
- **Skill exploratoria que muta.** Falta `allowed-tools` y el body termina con un `Write`/`Bash` no previsto. Decisión: whitelist mínima (`[Read, Grep, Glob]`); si necesita escribir, hazlo explícito y revisable. [INFERENCIA]
- **Regla permanente que se cuela en skill/command.** Queda opt-in y se ignora cuando nadie invoca. Decisión: moverla a CLAUDE.md. [INFERENCIA]
- **Nombre/slug que choca con un command o skill de plugin.** Colisión de namespace → invocación ambigua. Decisión: prefijo o slug único; nunca renombrar uno ya referenciado por rutas. [SUPUESTO]

## Decisiones y trade-offs

- **`context: fork` vs ejecución inline.** Fork aísla tokens y protege la sesión; trade-off: sin estado compartido y con coste de un turno de sub-agente. Se acepta cuando el output es voluminoso o ruidoso. [INFERENCIA]
- **Skill (on-demand) vs slash command (explícito).** Skill economiza la decisión humana pero depende de un match fiable de metadata; command es determinístico pero exige recordarlo. Elige por quién dispara: el modelo → skill; el humano → command. [INFERENCIA]
- **Project scope vs user scope.** Project replica al equipo vía git pero versiona la config; user es privado pero invisible para los demás. Default: project, salvo experimento personal. [DOC]

## Criterios de aceptación

- Command/skill correcto según trigger (explícito vs on-demand) y scope (project vs user). [DOC]
- Toda skill exploratoria declara `context: fork` y `allowed-tools` mínimo; ninguna muta sin Write explícito y revisable. [INFERENCIA]
- Las convenciones siempre-aplicables viven en CLAUDE.md, no en skill ni command. [DOC]
- `name`/`description` son específicos y no colisionan con otra skill o command. [INFERENCIA]

## Argumento de certificación

- Escoger command vs skill según trigger (explícito vs on-demand) y scope (project vs user). [DOC]
- Explicar el frontmatter: `context`, `allowed-tools` y `argument-hint`. [DOC]
- Conectar `context: fork` con la economía de contexto (sub-agente aislado, ~5000 tokens fuera de la sesión). [INFERENCIA]
- Defender que las convenciones permanentes van en CLAUDE.md, no en una skill ni en un command. [DOC]

## Cuándo activar

- El usuario pregunta por crear o versionar slash commands custom.
- Hay que decidir entre command y skill, o entre project scope y user scope.
- Se diseña el frontmatter de una skill (`context: fork`, `allowed-tools`, `argument-hint`).
- Se discute dónde ubicar convenciones permanentes del equipo.

## Skills relacionadas

- `katas-context-dilution-mitigation`
- `katas-prefix-caching`
- `katas-session-resume-fork`
