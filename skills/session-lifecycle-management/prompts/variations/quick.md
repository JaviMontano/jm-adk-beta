# Quick Prompt — Session Lifecycle (decisión rápida)

Decisión de transición en una pasada, para sesiones con pocos `tool_results`.

1. ¿Hay `SessionContext` previo? Si no → no-activación.
2. Corre staleness con hash/HEAD (no solo `mtime`). ¿Alguna stale **crítica**?
   - Sí → `fresh` + `TypedSummary` (con `stale_dropped` no vacío).
3. Sin stale crítica:
   - Objetivo continuo → `resume` (dropea cualquier stale no crítica del summary).
   - Ramificable sin estado mutable compartido → `fork` (scratchpad aislado por rama).
4. Emite `transition` + `trigger_reason` con evidencia. Pasa `scripts/check.sh`.

Salida mínima: `{ transition, stale[], trigger_reason }` (+ `typed_summary` si `fresh`). Tags de evidencia obligatorios.
