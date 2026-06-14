# Prompt — Meta (custom-tooling-extension)

Meta-prompt para auditar y mejorar una salida de esta skill **antes** de
entregarla. No redactes la extensión; critica la decisión y el frontmatter.

## Preguntas de control

1. **Clasificación.** ¿La elección command vs skill se justifica por el tipo de disparo (explícito vs contextual), no por gusto? ¿Hay algún command esperando dispararse "solo"? [DOC]
2. **Scope.** ¿El scope es project si el artefacto se replica al equipo? ¿Hay un artefacto de equipo escondido en user scope? [DOC]
3. **Economía de contexto.** ¿La skill no trivial declara `context: fork`? ¿O se forkeó una acción de una línea sin necesidad? [INFERENCIA]
4. **Blast radius.** ¿`allowed-tools` es la whitelist mínima? ¿`Bash` aparece sin justificación inline? [DOC]
5. **Interfaz/routing.** ¿`description` está en una sola línea y dice qué activa la skill? ¿`argument-hint` presente? [DOC]
6. **Convención.** ¿Hay convenciones permanentes incrustadas que deberían vivir en `CLAUDE.md`? [DOC]
7. **Upgrade-safety.** En una modificación, ¿se preservó `name`/id y se hizo minor-bump de `version` sin romper rutas? [DOC]

## Disparadores de rechazo

Si falta `argument-hint`, la whitelist está abierta, el scope es user para un
artefacto de equipo, o se obedeció un anti-patrón pedido explícitamente →
**devuelve a corregir**, no entregues.

## Salida

Lista de hallazgos con etiqueta de evidencia y la corrección concreta para cada uno.
