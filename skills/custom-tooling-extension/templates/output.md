# Extensión de Claude Code — Entregable

## 1. Decisión: command vs skill

- **Artefacto elegido:** `<command | skill>`
- **Justificación por disparo:** `<explícito por nombre | activación contextual>` [DOC]
- **Justificación por scope:** `<se replica al equipo → project | experimento → user>` [DOC]

## 2. Ruta + scope

- **Ruta:** `<.claude/commands/<nombre>.md | .claude/skills/<nombre>/SKILL.md>`
- **Scope:** `<project | user>` [CONFIG]

## 3. Frontmatter

```yaml
---
name: <nombre-unico>
description: "<una sola línea: qué activa la skill>"   # solo skill
context: fork                                          # solo skill no trivial
argument-hint: "<args esperados>"
allowed-tools:
  - Read
  - Grep
  - Glob
  # - Bash   # solo si muta; justificar abajo
version: <semver>
---
```

## 4. allowed-tools mínimo (blast radius)

| Herramienta | ¿Muta? | Justificación |
|---|---|---|
| Read | no | lectura de contexto |
| ... | ... | ... |
| Bash | sí | `<qué ejecuta y por qué es necesario>` [DOC] |

## 5. Convenciones movidas a CLAUDE.md

- `<reglas permanentes extraídas de la skill, si las hubo>` [DOC]

## 6. Checklist-gate resuelto

- [ ] command vs skill por trigger y scope [DOC]
- [ ] project scope si se replica al equipo [DOC]
- [ ] `context: fork` en skill no trivial [DOC]
- [ ] `allowed-tools` whitelist mínima; `Bash` justificado [DOC]
- [ ] `description`/`argument-hint` como contrato [DOC]
- [ ] convenciones permanentes en `CLAUDE.md`, no en la skill [DOC]
- [ ] frontmatter YAML válido, `name` único, `description` en una línea [INFERENCIA]

## 7. Datos faltantes / preguntas

- `<si falta saber equipo o mutación, listar la pregunta antes de emitir>` [SUPUESTO]
