# Ejemplo — Salida

## 1. Decisión: command vs skill

- **Artefacto elegido:** **skill**.
- **Justificación por disparo:** la petición llega en lenguaje natural ("genera las release notes entre v1.2 y v1.3"), no por un nombre fijo `/x` → activación contextual, que es el dominio de las skills, no de los commands. [DOC]
- **Justificación por scope:** debe servir a todo el equipo → **project**, versionado en el repo. [DOC]

## 2. Ruta + scope

- **Ruta:** `.claude/skills/release-notes/SKILL.md`
- **Scope:** project [CONFIG]

## 3. Frontmatter

```yaml
---
name: release-notes
description: "Genera notas de versión desde git log entre dos tags; se activa al pedir changelog/release notes."
context: fork
argument-hint: "<tag-desde> <tag-hasta>"
allowed-tools:
  - Read
  - Grep
  - Bash
version: 1.0.0
---
```

[CÓDIGO]

## 4. allowed-tools mínimo (blast radius)

| Herramienta | ¿Muta? | Justificación |
|---|---|---|
| Read | no | leer archivos de changelog/plantilla del repo |
| Grep | no | filtrar entradas del log por convención de commits |
| Bash | sí (acotado) | ejecutar `git log <desde>..<hasta>` y `git tag` en **solo lectura**; no se permiten `git push`, `git reset` ni escrituras [DOC] |

`context: fork` aísla la sub-tarea: el `git log` puede ser enorme y no debe
inflar ni contaminar la sesión principal. [DOC]

## 5. Convenciones movidas a CLAUDE.md

- Ninguna: la convención de formato de commits ya vive en `CLAUDE.md` del repo; la skill solo la consume, no la duplica. [DOC]

## 6. Checklist-gate resuelto

- [x] command vs skill por trigger (contextual) y scope (equipo→project) [DOC]
- [x] project scope porque se replica al equipo [DOC]
- [x] `context: fork` porque el log es no trivial y puede inflar la sesión [DOC]
- [x] `allowed-tools` mínima; `Bash` justificado como solo-lectura de git [DOC]
- [x] `description` en una línea + `argument-hint` con los dos tags [DOC]
- [x] sin convenciones permanentes incrustadas [DOC]
- [x] YAML válido, `name` único, `description` en una sola línea [INFERENCIA]

## 7. Datos faltantes / preguntas

- Ninguno: el equipo confirmó replicación, solo-lectura y los dos argumentos. No hubo que inventar scope ni whitelist. [SUPUESTO resuelto]
