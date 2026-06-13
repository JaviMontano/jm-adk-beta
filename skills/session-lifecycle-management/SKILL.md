---
name: session-lifecycle-management
version: 1.1.0
description: "Decidir resume vs fork vs fresh con summary tipado segun validez de contexto y deteccion de tool results stale."
owner: "JM Labs"
last_updated: 2026-06-11
triggers:
  - session lifecycle management
  - resume vs fork
  - fresh summary session
  - stale context
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Session Lifecycle Management

## Capacidad

Decidir de forma **auditable**, no por intuición del modelo, entre tres transiciones de sesión de agente: `resume` (contexto aún válido, objetivo continuo), `fork` (explorar ramas paralelas sin interferencia) y `fresh` con `TypedSummary` (el mundo cambió y el scratchpad quedó stale). [DOC]

El núcleo de ingeniería es la **detección de staleness**: identificar cuándo los resultados cacheados (lecturas de archivo, salidas de comando, estados de build) ya no reflejan el estado actual, y comprimir el scratchpad en hechos verificables —no un transcript crudo. [INFERENCIA]

## Cuándo usarla

- Agente de larga duración que sobrevive a múltiples turnos/reinicios y debe decidir si reusar el contexto previo. [DOC]
- Hubo refactor, migración o despliegue entre dos turnos y dudas si el contexto en memoria sigue siendo confiable. [DOC]
- Quieres probar varias hipótesis en paralelo sin que un experimento contamine al otro. [DOC]
- El scratchpad creció tanto que pegarlo completo es caro y ruidoso. [DOC]

**No la uses (anti-scope)** para: tareas de dominio sin sesión persistente (p. ej. generar un reporte financiero), un solo turno sin contexto previo, o input vacío. Si no hay `SessionContext` previo, no hay transición que decidir → no activar. [INFERENCIA]

## Inputs / Outputs

- **Input:** `SessionContext` (timestamp de captura, `tool_results[]` con su `source`+`mtime`/hash, invariantes del mundo: HEAD de git, hash del lockfile, esquema de BD) y un `Goal` (continuo | ramificable). [CODE]
- **Output:** una `Transition` (`Resume | Fork | Fresh`) + un **reporte JSON de decisión** con: transición elegida, `stale[]` detectados, razón del disparo, y `TypedSummary` cuando es `fresh`. [CODE]
- **Gate:** el reporte JSON valida offline con `bash skills/session-lifecycle-management/scripts/check.sh`. [CONFIG]

## Cómo construir

1. **Contrato de validez de contexto.** Modela qué hace válido un `SessionContext`: timestamp, `tool_results` con hash/`mtime` de origen, e invariantes del mundo (HEAD, lockfile, esquema). [CODE]
2. **Detector de staleness.** Compara cada result cacheado contra su fuente actual; si `mtime`/hash divergió, márcalo `stale`. Una sola dependencia stale **crítica** invalida el `resume`. [CODE]
3. **Matriz de decisión.** Reglas explícitas: válido y objetivo continuo → `resume`; ramificable sin estado mutable compartido → `fork`; staleness crítico o mundo cambiado → `fresh`. [CODE]
4. **`TypedSummary`.** Emite objeto tipado, no transcript: `goal`, `decisions[]`, `open_questions[]`, `verified_facts[]` (cada hecho con su evidencia), `stale_dropped[]`. [CODE]
5. **Aísla los forks.** Cada rama con su propio scratchpad y workspace; dos forks nunca comparten estado mutable. [CODE]
6. **Traza la decisión.** La transición queda registrada con su razón (qué disparó el `fresh`, qué quedó stale) y pasa el gate. [CODE]

## Decisiones y trade-offs

- **`mtime` + hash, no solo `mtime`.** `mtime` solo da falsos positivos (touch sin cambio) y falsos negativos (clock skew, checkout). El hash es la verdad; `mtime` es el filtro barato que evita hashear todo. Trade-off: doble fuente por algo de costo. [INFERENCIA]
- **`TypedSummary` sobre transcript crudo.** El transcript reintroduce results stale que el modelo tratará como verdad actual y quema tokens. El tipado fuerza a descartar lo stale explícitamente. Trade-off: pierdes matiz conversacional a cambio de hechos verificables. [INFERENCIA]
- **Fork aislado por defecto.** Estado mutable compartido entre ramas produce resultados no reproducibles e imposibles de atribuir. Trade-off: más workspaces que gestionar. [INFERENCIA]
- **Una stale crítica fuerza `fresh`.** Sesgo conservador: el costo de un `resume` sobre contexto corrupto (decisiones sobre datos falsos) supera el de re-sintetizar. [SUPUESTO]

## Casos borde

- **Staleness parcial no crítica** (un result stale, ninguno crítico): `resume` permitido pero el `TypedSummary` debe dropear ese result, no arrastrarlo. [INFERENCIA]
- **Fuente no determinística** (red, reloj, RNG): no es cacheable; trátala como `stale` siempre o no la almacenes como `verified_fact`. [SUPUESTO]
- **Merge-back de un fork:** al reincorporar una rama ganadora, re-corre el detector de staleness sobre su contexto; el fork pudo envejecer mientras corrían las otras ramas. [INFERENCIA]
- **Lockfile cambió, objetivo continuo:** sigue siendo `fresh` —la criticidad de la dependencia manda sobre la continuidad del objetivo. [CODE]

## Self-correction (revisar la decisión)

- Elegiste `resume` pero un `verified_fact` falla al reusarse en el turno actual → reclasifica a `fresh` y re-sintetiza. [INFERENCIA]
- Un `fork` empieza a leer/escribir el workspace de otro → el aislamiento se rompió; detén y re-provisiona scratchpads. [INFERENCIA]
- El `TypedSummary` contiene un hecho sin `source` o cuyo source está en `stale_dropped` → bug de filtrado; corrige antes de emitir. [CODE]

## Patrón correcto

```python
# GOOD: decision explicita basada en validez de contexto + staleness tipado
def decide_transition(ctx: SessionContext, goal: Goal) -> Transition:
    stale = [tr for tr in ctx.tool_results if is_stale(tr)]  # mtime/hash vs origen
    if any(tr.critical for tr in stale):
        # el mundo cambio: no reusar, sintetizar y reiniciar
        return Fresh(summary=typed_summary(ctx, drop=stale))
    if goal.is_branchable and not goal.shares_mutable_state:
        return Fork(branches=goal.hypotheses, isolated_scratchpad=True)
    return Resume(ctx)  # contexto valido y objetivo continuo


def typed_summary(ctx: SessionContext, drop: list[ToolResult]) -> TypedSummary:
    dropped_sources = {d.source for d in drop}
    return TypedSummary(
        goal=ctx.goal,
        decisions=ctx.decisions,
        open_questions=ctx.open_questions,
        verified_facts=[f for f in ctx.facts if f.source not in dropped_sources],
        stale_dropped=list(dropped_sources),
    )
```

## Anti-patrón

```python
# ANTI: resume ciego tras un refactor masivo + transcript crudo como "summary"
def next_session(prev_transcript: str, goal: Goal) -> Session:
    # 1) Reusa el contexto sin verificar si los archivos cambiaron (resume tras refactor).
    # 2) Pega el transcript completo viejo: ruido, tokens, y tool results stale
    #    que el modelo tratara como verdad actual.
    return Session(context=prev_transcript, goal=goal)
```

Otros anti-patrones: marcar `stale` solo por `mtime` sin verificar hash; forks que comparten un workspace; emitir un `TypedSummary` que conserva results de fuentes droppeadas. [INFERENCIA]

## Checklist de construcción

- [ ] ¿Se detectaron los tool results stale comparando contra la fuente actual (mtime **y** hash/HEAD)?
- [ ] ¿El summary es tipado (goal, decisions, open_questions, verified_facts, stale_dropped) y no un transcript crudo?
- [ ] ¿Los forks corren con scratchpad y workspace aislados, sin estado mutable compartido?
- [ ] ¿La transición resume/fork/fresh quedó trazada con su razón?
- [ ] ¿Una dependencia stale crítica fuerza `fresh` en lugar de `resume`?

## Gate de aceptación (antes de "done")

> Apóyate en `assets/` (rúbrica `assets/quality-rubric.json` y `assets/checklist.md`) para puntuar el reporte antes del done. [CONFIG]

1. El reporte JSON pasa `scripts/check.sh` sin errores. [CONFIG]
2. La transición es una de `resume | fork | fresh` y su razón referencia evidencia concreta (qué stale, qué invariante cambió). [CODE]
3. Si es `fresh`: existe `TypedSummary` y `stale_dropped` no está vacío cuando hubo staleness. [CODE]
4. Si es `fork`: cada rama tiene scratchpad propio declarado. [CODE]
5. Ningún `verified_fact` proviene de una fuente listada en `stale_dropped`. [CODE]
6. Casos de no-activación (sin sesión previa, input vacío, dominio ajeno) **no** emiten transición. [INFERENCIA]

## Katas y skills relacionadas

- Kata 25 — decisión de ciclo de vida de sesión.
- `katas-session-resume-fork`
- `workspace-governance`
- `workflow-forge`
- `quality-guardian`
