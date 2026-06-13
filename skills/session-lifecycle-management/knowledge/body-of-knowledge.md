# Body of Knowledge — Session Lifecycle Management

## 1. Conceptos clave

- **SessionContext.** Snapshot tipado del estado de una sesión: `timestamp` de captura, `tool_results[]` (cada uno con `source`, `mtime`, `hash`), invariantes del mundo (HEAD de git, hash del lockfile, esquema/versión de BD), `decisions[]`, `open_questions[]`, `facts[]`. Es el objeto cuya **validez** se evalúa. [CODE]
- **Transition.** El resultado de la decisión: `Resume | Fork | Fresh`.
  - `Resume`: el contexto sigue válido y el objetivo es continuo → reusar.
  - `Fork`: el objetivo es ramificable y no comparte estado mutable → explorar ramas aisladas en paralelo.
  - `Fresh`: el mundo cambió o hay staleness crítica → re-sintetizar con `TypedSummary` y reiniciar. [DOC]
- **Staleness.** Condición de un `tool_result` cuyo origen divergió respecto al snapshot. Se mide con doble fuente: `mtime` (filtro barato) + hash/HEAD (verdad). [INFERENCIA]
- **Criticidad.** Atributo de una dependencia stale: una stale **crítica** (lockfile, esquema, HEAD del módulo en uso) invalida el `resume`; una no crítica permite `resume` pero obliga a dropear el result. [CODE]
- **TypedSummary.** Compresión del scratchpad en objeto tipado —no transcript crudo—: `goal`, `decisions[]`, `open_questions[]`, `verified_facts[]` (cada uno con `source`), `stale_dropped[]`. [CODE]

## 2. Estándares y convenciones

- **Evidencia tipada.** Toda afirmación lleva tag: `[CODE]` (contrato/función), `[CONFIG]` (gate/script), `[DOC]` (documentado), `[INFERENCIA]` (deducción sólida), `[SUPUESTO]` (hipótesis a validar).
- **Doble fuente para staleness.** Nunca `mtime` solo: produce falsos positivos (`touch`) y falsos negativos (clock skew, checkout). El hash es la verdad; `mtime` evita hashear todo. [INFERENCIA]
- **Aislamiento de forks por defecto.** Cada rama con scratchpad y workspace propios; cero estado mutable compartido. [CODE]
- **Gate offline obligatorio.** El reporte de decisión valida con `scripts/check.sh` antes de done. [CONFIG]

## 3. Reglas de decisión (matriz)

| Validez de contexto | Objetivo | Estado mutable compartido | → Transición |
|---|---|---|---|
| Válido (sin stale crítica) | Continuo | — | `resume` |
| Válido | Ramificable | No | `fork` |
| Stale crítica / mundo cambiado | Cualquiera | — | `fresh` |
| Ramificable | Ramificable | Sí | no `fork` (resolver compartición primero) |

Reglas finas:
1. Una sola stale **crítica** fuerza `fresh` aunque el objetivo sea continuo (sesgo conservador: reusar contexto corrupto cuesta más que re-sintetizar). [SUPUESTO]
2. Staleness parcial no crítica → `resume` permitido, pero el `TypedSummary` dropea ese result. [INFERENCIA]
3. Fuente no determinista (red/reloj/RNG) → siempre `stale`, nunca `verified_fact`. [SUPUESTO]
4. Merge-back de fork → re-correr el detector sobre su contexto (pudo envejecer). [INFERENCIA]
5. Lockfile cambió + objetivo continuo → `fresh` (criticidad > continuidad). [CODE]

## 4. Invariantes de integridad

- Ningún `verified_fact` proviene de una `source ∈ stale_dropped`. [CODE]
- `stale_dropped` no vacío cuando hubo staleness y la transición es `fresh`. [CODE]
- Cada `fork` declara scratchpad propio. [CODE]
- La transición cita su `trigger_reason` con evidencia concreta. [CODE]

## 5. Anti-patrones

- **Resume ciego** tras refactor/deploy sin verificar fuentes. [INFERENCIA]
- **Transcript crudo como summary**: reintroduce results stale como verdad y quema tokens. [INFERENCIA]
- **`mtime`-only** para marcar stale. [INFERENCIA]
- **Forks que comparten workspace** → resultados no reproducibles. [INFERENCIA]
- **`TypedSummary` con hechos de fuentes droppeadas** → bug de filtrado. [CODE]

## 6. No-activación

Sin `SessionContext` previo, input vacío, o dominio ajeno (p. ej. generar un reporte financiero) → **no** emitir transición. La skill solo decide transiciones de sesión existentes. [INFERENCIA]
