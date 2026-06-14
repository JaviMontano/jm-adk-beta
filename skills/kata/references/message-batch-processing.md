<!-- distilled from alfa skills/katas-message-batch-processing -->
<!-- Procesamiento masivo con Message Batches API, custom_id unico por request y fragmentacion selectiva de fallos parciales. -->
# Kata 17 · Procesamiento Masivo con Message Batches API

## Qué es

Para cargas no interactivas (auditorías, backfills, evaluaciones de regresión, extracciones estructuradas masivas), la Message Batches API (`POST /v1/messages/batches`) procesa requests offline a ~50% del costo real-time. [DOC] Cada request lleva un `custom_id` único que correlaciona request↔response y aísla fallos parciales: si una falla, las demás siguen y se identifica exactamente cuál reprocesar. [DOC]

Escenarios objetivo: CI/CD Automation y Structured Extraction.

## Por qué importa (falla que evita)

Pagar tarifa real-time por trabajo offline es desperdicio puro. [INFERENCIA] Procesar 10000 prompts con un `for` rompe rate limits, no maneja fallos parciales y tarda horas. [INFERENCIA] El batch da 50% de ahorro, aislamiento por request y escalabilidad. [DOC] Sin `custom_id` un fallo parcial obliga a reprocesar todo el lote y no hay mapeo fiable response→input. [INFERENCIA]

Falla silenciosa más cara: iterar resultados asumiendo que todos son `succeeded`. Un batch `ended` mezcla `succeeded`, `errored`, `canceled` y `expired`; guardar `r.result` sin discriminar el tipo persiste errores como si fueran respuestas válidas y contamina el dataset sin lanzar excepción. [INFERENCIA]

## Modelo mental

- Un batch es una colección de requests independientes, cada una con `custom_id` único. [DOC]
- Ciclo de vida: `create → poll processing_status → results`. `processing_status` pasa por `in_progress` y termina en `ended`; `results` solo está disponible tras `ended`. [DOC]
- `ended` ≠ éxito total: es éxito parcial. Cada resultado trae `result.type` ∈ {`succeeded`, `errored`, `canceled`, `expired`}. [DOC]
- `custom_id` es la única clave de correlación; se devuelve verbatim. Duplicarlo introduce ambigüedad irresoluble. [DOC]
- Reproceso selectivo: reintentar solo lo recuperable por su `custom_id`, nunca el lote completo. [INFERENCIA]
- Elegibilidad: carga offline y tolerante a latencia (minutos/horas, no tiempo real). [INFERENCIA]

## Límites y supuestos operativos

- Máx 100 000 requests o 256 MB por batch; lo que exceda se fragmenta en sub-batches. [DOC]
- Duración típica <1 h, techo duro 24 h; lo no terminado a las 24 h queda `expired`. [DOC]
- Resultados disponibles 29 días tras `create`; persistir antes de ese vencimiento. [DOC]
- `params` debe ser un Messages create NO-streaming (`MessageCreateParamsNonStreaming`); streaming no aplica en batch. [DOC]
- `custom_id` ≤ 64 chars y único en el batch. [DOC] Como vuelve en claro, nunca embeber PII ni secretos — usar un id opaco y mapear fuera del batch. [INFERENCIA]
- Todas las features de Messages aplican (visión, tools, prompt caching). [DOC] Caching reduce aún más el costo si las requests comparten prefijo estable. [INFERENCIA]

## Taxonomía de resultados y política de reintento

| `result.type` | Causa | Acción |
|---|---|---|
| `succeeded` | OK | persistir `result.message` |
| `errored` · `invalid_request` | request mal formada (validación determinista) | NO reintentar igual; corregir el `params` y reenviar |
| `errored` · `api_error`/overloaded | fallo transitorio del servidor | reintentar (idempotente vía `custom_id`) |
| `canceled` | batch cancelado en vuelo | reenviar si aún se necesita |
| `expired` | no terminó en 24 h | reenviar, idealmente en sub-batch más pequeño |

Reintentar a ciegas un `invalid_request` desperdicia cuota y nunca converge: es la trampa clave. [INFERENCIA]

## Patrón correcto

```python
batch = client.messages.batches.create(
    requests=[
        {"custom_id": f"audit-{i}", "params": {...}}  # params NO-streaming
        for i, _ in enumerate(items)
    ]
)
while batch.processing_status != "ended":
    sleep(30)
    batch = client.messages.batches.retrieve(batch.id)

retry = []
for r in client.messages.batches.results(batch.id):
    t = r.result.type
    if t == "succeeded":
        save(r.custom_id, r.result.message)
    elif t == "errored" and r.result.error.type == "invalid_request":
        quarantine(r.custom_id, r.result.error)        # corregir, no reintentar igual
    else:                                              # errored transitorio / canceled / expired
        retry.append(r.custom_id)                      # sub-batch de reintento selectivo
```

## Anti-patrón

```python
for item in ten_thousand_items:
    r = client.messages.create(**params(item))  # tarifa real-time, rompe rate limits
    save(r)                                       # sin custom_id, sin aislamiento de fallos
```

Procesa cada item en real-time, paga el doble, no aísla fallos y se estrella contra rate limits. [INFERENCIA] Variante igual de peligrosa: usar batch pero guardar `r.result` sin mirar `result.type` (persiste errores como éxitos). [INFERENCIA]

## Argumento de certificación

- Identificar qué cargas son elegibles para Batch (offline, tolerantes a latencia).
- Describir el ciclo `create → poll → results` y que `results` solo existe tras `ended`.
- Justificar `custom_id` como clave de correlación y por qué no debe llevar PII.
- Discriminar los cuatro `result.type` y aplicar la política de reintento (no reintentar `invalid_request` sin corregir).
- Explicar la fragmentación selectiva: reintentar solo lo recuperable, nunca todo el lote.

### Criterios de aceptación (de una implementación batch)

- Cada request tiene `custom_id` único, ≤64 chars y sin PII.
- El loop de resultados ramifica sobre `result.type`; ningún `errored`/`expired` se persiste como éxito.
- Los `invalid_request` se aíslan para corrección, no se reencolan idénticos.
- El reproceso reenvía solo los `custom_id` afectados, no el batch completo.
- Los resultados se persisten antes del vencimiento de 29 días.

## Cuándo activar

- El usuario habla de procesar miles de prompts, backfills, auditorías masivas o evaluaciones offline.
- Aparecen términos como `message batches`, `batch processing`, `custom_id`, `offline batch`.
- El trabajo no requiere respuesta interactiva en tiempo real y el costo importa.

### Anti-scope (cuándo NO)

- Cargas interactivas o sensibles a latencia (chat, autocompletado): el batch tarda minutos/horas. [INFERENCIA]
- Volúmenes pequeños donde el overhead de poll/results supera el ahorro. [INFERENCIA]
- Pipelines que necesitan el output de una request para construir la siguiente: eso es chaining secuencial, no batch. [INFERENCIA]

## Skills relacionadas

- `katas-multipass-prompt-chaining`
- `katas-validation-retry-feedback`
- `katas-confidence-stratified-sampling`
