# Deep Prompt — Session Lifecycle (análisis exhaustivo)

Para sesiones largas, multi-fork, o con invariantes ambiguas.

## Fase 1 — Contrato de validez
Enumera explícitamente qué hace válido el `SessionContext`: `timestamp`, cada `tool_result` con su `source`/`mtime`/`hash`, e invariantes del mundo (HEAD, lockfile hash, esquema de BD). Marca cuáles son **críticos**.

## Fase 2 — Detección de staleness con doble fuente
Para cada `tool_result` y cada invariante:
- Computa `mtime` actual (filtro barato). Si difiere, computa hash/HEAD (verdad).
- Clasifica: `fresh`, `stale-no-crítica`, `stale-crítica`. Documenta `{ source, expected, observed, critical }`.
- Trata fuentes no deterministas (red/reloj/RNG) como `stale` siempre.

## Fase 3 — Matriz de decisión razonada
- Stale crítica o mundo cambiado → `fresh`.
- Válido + continuo → `resume`.
- Ramificable sin estado mutable compartido → `fork`; si comparte estado, resuelve la compartición antes de ramificar.

## Fase 4 — TypedSummary (si fresh) o saneamiento (si resume)
Construye `{ goal, decisions[], open_questions[], verified_facts[] (con source), stale_dropped[] }`. Verifica la invariante: ningún `verified_fact` desde una fuente en `stale_dropped`.

## Fase 5 — Forks
Declara scratchpad y workspace propios por rama. Para merge-back, re-corre la detección de staleness sobre el contexto de la rama ganadora (pudo envejecer).

## Fase 6 — Trazabilidad y gate
Registra `trigger_reason` con evidencia. Adjunta hashes/HEAD usados (reproducibilidad). Pasa `scripts/check.sh`. Nunca verde sin evidencia. Tags de evidencia en cada juicio.
