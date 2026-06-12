# Prompt — Deep (custom-tooling-extension)

Diseño exhaustivo de la extensión cuando hay ambigüedad de scope, operaciones
mutadoras, o una migración de una extensión existente.

## Procedimiento extendido

1. **Modelo de disparo.** Mapea todos los disparos posibles. Si conviven invocación por nombre y activación contextual, decide cuál es primario; no dupliques la capacidad como command y skill (drift). [SUPUESTO]
2. **Scope y gobernanza.** Project replica y versiona (pasa por revisión); user es ágil pero no llega al equipo. Documenta el trade-off elegido. [DOC]
3. **Economía de contexto.** Justifica `context: fork` por tamaño/autocontención de la sub-tarea; descarta fork para acciones de una línea (pierdes contexto vivo sin ganancia). [INFERENCIA]
4. **Blast radius por operación.** Enumera cada operación (lectura/mutación) y deriva la whitelist mínima. Cada herramienta de mutación (`Bash`) lleva justificación inline de qué ejecuta y por qué. [DOC]
5. **Separación convención/capacidad.** Identifica reglas permanentes y muévelas a `CLAUDE.md`; deja en la skill solo lo condicional. [DOC]
6. **Upgrade-safety.** Si modificas una extensión: preserva `name`/id, no rompas rutas `.claude/` ni referencias cruzadas, minor-bump de `version`, y migra invocaciones si el id o scope cambian. [DOC]
7. **Gate con evidencia.** Recorre el checklist de `SKILL.md` y la rúbrica de `assets/quality-rubric.json`; verde-con-evidencia, nunca verde-por-defecto.

## Salida

Entregable completo de `templates/output.md` + tabla de blast radius por
operación + nota de migración si aplica, todo con etiquetas de evidencia.
