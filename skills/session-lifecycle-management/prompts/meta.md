# Meta Prompt — Session Lifecycle Management

Guía de meta-razonamiento para auto-supervisar la decisión de transición antes de emitirla.

## Preguntas de control

1. **¿Verifiqué la fuente o asumí?** Toda marca `stale`/no-stale debe apoyarse en `mtime`+hash/HEAD observados, no en memoria del turno previo. Si no computé el hash, la decisión es una conjetura. [CODE]
2. **¿`mtime` solo me engañó?** ¿Hubo `touch` sin cambio (falso positivo) o clock skew/checkout (falso negativo)? Confirma con hash. [INFERENCIA]
3. **¿La criticidad domina?** Si hay una stale crítica y elegí `resume`, me equivoqué: la criticidad fuerza `fresh`. [CODE]
4. **¿El summary está limpio?** ¿Algún `verified_fact` viene de una `source ∈ stale_dropped`? Si sí, es un bug de filtrado; corrige antes de emitir. [CODE]
5. **¿Los forks están aislados?** ¿Dos ramas comparten workspace o estado mutable? Si sí, re-provisiona. [INFERENCIA]
6. **¿Debí no activar?** Sin sesión previa / input vacío / dominio ajeno → no emitir transición. [INFERENCIA]

## Auto-corrección

- Un `verified_fact` que falla al reusarse en el turno actual → reclasifica a `fresh` y re-sintetiza.
- Reporte sin `trigger_reason` con evidencia concreta → incompleto; añade qué stale y qué invariante cambió.
- Gate falla → no marques done; corrige y re-corre `scripts/check.sh`.

## Sesgo declarado

Conservador: ante duda entre `resume` y `fresh` sobre contexto posiblemente corrupto, prefiere `fresh`. El costo de decidir sobre datos falsos supera el de re-sintetizar. [SUPUESTO]
