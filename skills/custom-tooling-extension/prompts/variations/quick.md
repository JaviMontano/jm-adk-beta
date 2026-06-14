# Prompt — Quick (custom-tooling-extension)

Decisión rápida command vs skill + frontmatter mínimo, en una pasada.

## Pasos

1. ¿Disparo explícito por nombre (`/x`)? → **command**. ¿Activación contextual? → **skill** con `context: fork`.
2. ¿Se replica al equipo? → **project** (`.claude/` versionado). Si no, user.
3. `allowed-tools`: read-only (`Read, Grep, Glob`) salvo que mute → añade `Bash` justificado.
4. `description` en una línea (skill) + `argument-hint`.

## Guardas

- Falta saber equipo o mutación → **pregunta**, no inventes scope ni whitelist.
- Piden el anti-patrón → explícalo, no lo emitas.

## Salida

Ruta + scope, frontmatter listo para pegar, una línea por cada decisión con su
etiqueta `[DOC]`/`[CONFIG]`/`[CÓDIGO]`.
