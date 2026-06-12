# Checklist del Gate — Session Lifecycle Management

Marca antes de emitir la transición. Cada ítem requiere evidencia, no intuición.

## Detección de staleness
- [ ] Cada `tool_result` se comparó con `mtime` (filtro) **y** hash/HEAD (verdad).
- [ ] Las invariantes del mundo (HEAD, lockfile hash, esquema BD) se re-computaron.
- [ ] Ningún result se marcó `stale` solo por `mtime` sin verificar hash.
- [ ] Fuentes no deterministas (red/reloj/RNG) tratadas como `stale`, nunca `verified_fact`.

## Decisión
- [ ] La transición es una de `resume | fork | fresh`.
- [ ] Una stale **crítica** forzó `fresh` (no `resume`).
- [ ] `fork` solo cuando es ramificable **sin** estado mutable compartido.
- [ ] `trigger_reason` cita evidencia concreta (qué stale, qué invariante cambió).

## TypedSummary (si `fresh`)
- [ ] Es tipado (`goal`, `decisions`, `open_questions`, `verified_facts`, `stale_dropped`), no transcript crudo.
- [ ] `stale_dropped` no está vacío cuando hubo staleness.
- [ ] Ningún `verified_fact` proviene de una fuente en `stale_dropped`.

## Forks (si `fork`)
- [ ] Cada rama declara scratchpad y workspace propios.
- [ ] Ninguna rama comparte estado mutable.
- [ ] Merge-back re-corre la detección de staleness.

## Cierre
- [ ] `scripts/check.sh` retorna `exit_code=0`.
- [ ] Casos de no-activación (sin sesión previa, input vacío, dominio ajeno) no emitieron transición.
- [ ] Toda afirmación lleva tag de evidencia; sin PII; marca única JM Labs.
