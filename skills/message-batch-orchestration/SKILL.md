---
name: message-batch-orchestration
version: 1.1.0
description: "Orquestar Message Batches API para cargas offline con custom_id unico, fragmentacion selectiva de fallos parciales y reintento con cap."
owner: "JM Labs"
triggers:
  - message batch orchestration
  - offline batch
  - custom_id correlation
  - partial failure retry
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Message Batch Orchestration

## Capacidad

Construye orquestadores de la **Message Batches API** de Anthropic para procesar cargas masivas offline. [DOC] El patrón asigna un `custom_id` único por request para correlacionar resultados y **aísla los fallos**: cuando una fracción del lote falla, solo se reintentan esos `custom_id`, nunca el batch completo. [DOC] Ciclo de vida: `create → poll processing_status → results() → fragmentar → retry selectivo`. [CÓDIGO]

**Entradas**: lista de items con un ID de negocio estable, `model`, `max_tokens`, contenido del prompt, y un `max_retries`. [INFERENCIA]
**Salidas**: mapa `custom_id → message` para éxitos persistidos + lista de `custom_id` no resueltos tras agotar el cap, más (si se exige evidencia) un reporte JSON que pasa `scripts/check.sh`. [CONFIG]

## Cuándo usarla

- Carga **offline / latency-tolerant**: clasificación masiva, enriquecimiento de datasets, evaluaciones, backfills. No hay usuario esperando en línea. [DOC]
- El volumen justifica procesamiento asíncrono y aislamiento de fallos frente a llamadas síncronas una por una (a volumen, el modo batch también recorta coste ~50% vs. síncrono). [DOC]
- Necesitas **reintento selectivo** de items fallidos sin reprocesar los exitosos. [DOC]

### Anti-scope (NO usarla)

- Flujos **interactivos / streaming** o cualquier ruta donde el usuario espera la respuesta en línea → es `false_positive_realtime` en evals. [CONFIG]
- Tareas no relacionadas (p. ej. diseño de esquema de BD) → no activar. [CONFIG]
- Si el dataset trae `custom_id` duplicados y el usuario pide **saltar la validación de unicidad**, o pide explícitamente **sin custom_id / sin aislar fallos** → rechaza, no degrades el patrón. [CONFIG]

## Cómo construir

1. **Modela la unidad de trabajo.** Cada item es un request con `custom_id` único y **estable**, derivado del ID de negocio (no de un índice de loop), para correlacionar y deduplicar de forma idempotente entre reintentos. [CÓDIGO]
2. **Ensambla el batch.** Construye `requests`, valida unicidad de `custom_id` **antes** de enviar, y respeta los límites de tamaño/conteo del endpoint. [CÓDIGO]
3. **Crea el batch** con `client.messages.batches.create(requests=...)` y persiste el `batch.id` (checkpoint: sobrevive a un crash del orquestador). [CÓDIGO]
4. **Polling de `processing_status`** con backoff hasta `ended`; nunca asumas finalización inmediata. [CÓDIGO]
5. **Recupera resultados** vía streaming de `results()`, indexando por `custom_id`. [CÓDIGO]
6. **Fragmenta por `result.type`:** `succeeded` → persiste; `errored` / `expired` / `canceled` → agrupa en sub-lote de reintento por `custom_id`. [CÓDIGO]
7. **Reintenta solo los fallidos** creando un batch nuevo con los `custom_id` afectados, aplicando el **cap de reintentos**; al agotarlo, devuelve los irresolubles para inspección, no en silencio. [CÓDIGO]

### Decisiones y trade-offs

- **`custom_id` = ID de negocio, no índice de loop.** El índice rompe la correlación si el orden de `items` cambia entre reintentos; el ID de negocio es idempotente. [INFERENCIA]
- **Persistir `batch.id` antes de hacer polling.** Permite reanudar tras un crash sin recrear el batch (evita doble cobro). [INFERENCIA]
- **Cap de reintentos > 0 obligatorio.** Sin cap, `expired`/`errored` recurrentes producen un bucle infinito de creación de batches. [INFERENCIA]
- **Backoff en el polling, no busy-wait.** Ahorra llamadas a `retrieve` en batches que tardan minutos/horas. [INFERENCIA]

## Contrato determinístico

Usa los assets de `assets/` para certificar planes de batch: [CONFIG]

- `assets/message-batch-orchestration-contract.json`: campos JSON obligatorios del reporte.
- `assets/workload-policy.json`: criterios offline, latency-tolerant, no streaming.
- `assets/custom-id-policy.json`: unicidad y estabilidad de `custom_id`.
- `assets/lifecycle-policy.json`: lifecycle `create → poll processing_status → results`.
- `assets/retry-fragmentation-policy.json`: fragmentación y retry selectivo con cap.
- `assets/evidence-policy.json`: evidencia mínima aceptada.

Cuando el entregable sea JSON, valida offline con `scripts/validate_message_batch_orchestration.py`. [CÓDIGO] Para la smoke determinística completa ejecuta `scripts/check.sh`, que acepta fixtures válidos y rechaza mutaciones inválidas. [CÓDIGO]

## Patrón correcto

```python
# GOOD: batch offline con custom_id único + fragmentación selectiva de fallos
import time
from anthropic import Anthropic

client = Anthropic()

def build_requests(items):
    seen = set()
    requests = []
    for it in items:
        cid = it["id"]  # ID de negocio estable, no índice de loop
        if cid in seen:
            raise ValueError(f"duplicate custom_id: {cid}")  # gate de unicidad
        seen.add(cid)
        requests.append({
            "custom_id": cid,
            "params": {
                "model": "claude-sonnet-4-5",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": it["prompt"]}],
            },
        })
    return requests

def run_batch(items, max_retries=2):
    pending = items
    succeeded = {}
    for attempt in range(max_retries + 1):
        batch = client.messages.batches.create(requests=build_requests(pending))
        # persiste batch.id aquí para poder reanudar tras un crash
        while True:
            status = client.messages.batches.retrieve(batch.id).processing_status
            if status == "ended":
                break
            time.sleep(min(30, 2 ** attempt))  # backoff en el polling

        failed = []
        for result in client.messages.batches.results(batch.id):
            if result.result.type == "succeeded":
                succeeded[result.custom_id] = result.result.message
            else:  # errored | expired | canceled -> aísla solo el fallo
                failed.append(result.custom_id)

        if not failed:
            break
        pending = [it for it in items if it["id"] in set(failed)]  # retry selectivo
    return succeeded, [it["id"] for it in pending if it["id"] not in succeeded]
```

> Modelo `claude-sonnet-4-5` fijado por el contrato de evals de esta skill (`large_dataset_checkpointing`); cámbialo solo si el usuario nombra otro. [CONFIG]

## Anti-patrón

```python
# ANTI: loop síncrono real-time, sin custom_id, sin fail-isolation
for item in items:                          # uno por uno: caro y lento
    resp = client.messages.create(          # rompe rate limits a volumen
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": item["prompt"]}],
    )
    results.append(resp)                     # un fallo aborta todo el lote;
                                             # sin custom_id no hay retry selectivo
```

## Self-correction triggers

Si te sorprendes haciendo cualquiera de esto, vuelve a "Cómo construir": [INFERENCIA]
- Llamando `client.messages.create()` en un loop sobre items offline → debías batchear.
- Usando `enumerate()`/índice como `custom_id` → usa el ID de negocio.
- Reintentando el batch completo tras un fallo parcial → fragmenta y reintenta solo `failed`.
- Tratando `processing_status != "ended"` como terminal, o asumiendo finalización inmediata → sigue en polling con backoff.
- Reintentando sin cap → bucle infinito ante `expired`/`errored` recurrentes.

## Checklist de validación (acceptance gate)

Marca TODAS antes de dar por hecho el entregable: [DOC]
- [ ] La carga es offline / latency-tolerant y justifica el modo batch.
- [ ] Cada request tiene `custom_id` único y estable derivado del ID de negocio.
- [ ] La unicidad de `custom_id` se valida **antes** de enviar (gate que lanza en duplicado).
- [ ] El polling de `processing_status` usa backoff y espera el estado `ended`.
- [ ] Los resultados se fragmentan en éxitos vs. fallidos por `result.type` (`succeeded` aparte de `errored`/`expired`/`canceled`).
- [ ] El reintento es selectivo (solo fallidos) y tiene cap; al agotarlo se devuelven los irresolubles.
- [ ] No queda ningún loop síncrono one-by-one en la ruta offline.
- [ ] Si se exige evidencia offline, el reporte pasa `scripts/check.sh`.

## Edge cases

- **Batch parcialmente `expired`/`canceled`.** Trátalos como fallidos reintegrables igual que `errored`; entran al sub-lote de retry bajo el mismo cap. [CÓDIGO]
- **Duplicados en el ID de negocio de origen.** Falla en `build_requests` (no envíes); deduplica aguas arriba o pide regla de desempate. No silencies el duplicado. [CÓDIGO]
- **Crash durante el polling.** Con `batch.id` persistido, reanuda con `retrieve`/`results` sin recrear el batch. [INFERENCIA]
- **Todos los items fallan en el último intento.** Devuelve la lista de `custom_id` irresolubles para inspección; nunca retornes éxito vacío como si fuera completo. [INFERENCIA]

## Katas y skills relacionadas

- Kata 17.
- Skill relacionada: `katas-message-batch-processing`.
