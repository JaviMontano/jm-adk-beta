<!-- distilled from alfa skills/katas-validation-retry-feedback -->
<!-- Validacion y retry con error feedback especifico; distinguir recuperable de no recuperable; max 2-3 intentos y luego escalar. -->
# Kata 26 · Validación y Retry con Error Feedback

## Qué es

Cuando una extracción tipada falla la validación (Pydantic / JSON Schema), no se reintenta a ciegas: se hace **retry-with-error-feedback**. La nueva llamada incluye el documento original, la extracción que falló y el error específico que produjo la validación, con la instrucción de corregir **solo** lo que el error señala. [DOC] Máximo 2-3 intentos. La distinción clave es entre errores **recuperables** (formato, tipo, campo mal estructurado) y **no recuperables** (el dato no existe en la fuente): sólo los primeros justifican retry. [DOC]

## Por qué importa (falla que evita)

- Reintentar con el mismo prompt sin feedback es ruido: el modelo no sabe qué corregir y repite el error. [INFERENCIA]
- Aceptar en silencio una salida que falló validación rompe los contratos downstream que dependen del schema. [DOC]
- Reintentar cuando el dato no existe en la fuente garantiza alucinación: el modelo inventará un valor para satisfacer el schema. [DOC]

## Modelo mental

- Loop: `extract → validate → (si error recuperable) extract+feedback → validate`. [DOC]
- Máximo 2-3 intentos; el feedback debe ser el error específico (mensaje real del validador), no genérico. [DOC]
- Tras N intentos sin éxito: marcar `needs_human_review` con la cadena de errores acumulados. [DOC]
- Error recuperable (formato) y no recuperable (información ausente) son ramas distintas del flujo; el no recuperable corta el loop sin gastar intentos. [INFERENCIA]
- Si el 80% de los fallos es el mismo error sistemático, el fix no es subir `max_retries`: es ajustar schema/prompt o normalizar en post-process. [DOC]

## Contrato determinístico

Usa los assets de `assets/` como contrato de salida antes de certificar la kata:

- `assets/validation-retry-contract.json`: campos JSON obligatorios y decisiones Guardian permitidas.
- `assets/error-classification-policy.json`: errores recuperables, no recuperables y reglas de retry.
- `assets/feedback-specificity-policy.json`: señales mínimas para considerar específico un feedback de retry.
- `assets/retry-limit-policy.json`: cap total de 2-3 intentos y reglas de escalada.
- `assets/evidence-policy.json`: evidencia mínima aceptada para validar el reporte.

Cuando el entregable sea JSON, valida offline con `scripts/validate_validation_retry_feedback.py`. Para la smoke determinística completa ejecuta `scripts/check.sh`, que acepta fixtures válidos y rechaza mutaciones inválidas. [CONFIG]

## Patrón correcto

```python
def extract_with_retry(client, doc, schema, max_retries=2):
    last_error = None
    extraction = None
    for attempt in range(max_retries + 1):
        feedback = (
            f"Intento previo falló: {last_error}\n"
            f"Output previo: {extraction}\n"
            "Corrige SOLO lo que el error señala."
        ) if last_error else ""
        resp = client.messages.create(
            tools=[schema],
            tool_choice={"type": "tool", "name": schema["name"]},
            messages=[{"role": "user", "content": doc + feedback}],
        )
        extraction = resp.tool_use.input
        try:
            validate(extraction, schema)
            return {**extraction, "attempts": attempt + 1}
        except ValidationError as e:
            if not is_recoverable(e):           # dato ausente: no reintentar
                break
            last_error = str(e)
    return {**(extraction or {}), "needs_human_review": True, "error_chain": last_error}
```

El `break` ante un error no recuperable es la rama que evita la alucinación: se escala de inmediato en vez de quemar intentos pidiendo un dato inexistente. [INFERENCIA]

## Anti-patrón

```python
for _ in range(5):
    ext = extract(doc)
    try:
        validate(ext)
        return ext
    except Exception:
        continue  # mismo prompt, sin feedback: ruido puro
# ...y aceptar una salida fallida en silencio downstream
```

Mismo prompt cinco veces sin feedback específico, más aceptar la salida fallida sin marcarla. [DOC]

## Supuestos y límites (anti-scope)

- Asume que el error del validador es legible y apunta al campo concreto; un error opaco ("invalid") no es feedback accionable y degrada el retry a ruido. [SUPUESTO] Verificar: el mensaje nombra campo + razón.
- Asume que feedback en lenguaje natural reduce el error; NO garantiza convergencia: un error de ambigüedad de la fuente puede persistir pese al feedback perfecto. [INFERENCIA]
- Cubre fallos de formato/tipo/estructura; NO cubre datos correctos-pero-incorrectos (pasan el schema y son falsos): eso es tarea de provenance/confidence, no de este kata. [DOC]
- El cap 2-3 es regla, no parámetro a tunear: subirlo enmascara un problema estructural de schema/prompt en vez de resolverlo. [DOC]
- Cada retry es una llamada de costo: el cap también acota gasto y latencia, no sólo alucinación. [INFERENCIA]

## Edge cases y failure modes

- Feedback genérico ("output inválido, reintenta") en vez del error real: el retry deja de informar y vuelve al anti-patrón. Inyectar siempre `str(e)`. [DOC]
- Error no recuperable clasificado como recuperable: se gastan los 3 intentos y se acaba inventando el dato. Clasificar ANTES de reintentar. [INFERENCIA]
- Error recuperable clasificado como no recuperable: se escala algo arreglable con un retry barato → ruido para el humano. La clasificación es bidireccionalmente costosa. [INFERENCIA]
- 80% de fallos = mismo error: señal de fix estructural (schema/prompt/post-process), no de subir `max_retries`. [DOC]
- Output truncado por límite de tokens marcado como ValidationError: es fallo de longitud, no de extracción; subir `max_tokens`, no reintentar igual. [INFERENCIA]
- Escalar sin `error_chain`: el humano recibe "falló" sin las N causas → revisión a ciegas. Acumular siempre la cadena. [DOC]

## Ejemplo trabajado (recuperable vs no recuperable)

1. Doc sin campo `tax_id`. Intento 1 → `ValidationError: tax_id required`. Clasificación: **no recuperable** (dato ausente). `break`, `needs_human_review=True`. Cero alucinación, 1 llamada. [INFERENCIA]
2. Doc con `amount: "1.234,50"`. Intento 1 → `ValidationError: amount not a float`. Clasificación: **recuperable** (formato). Feedback con el error → intento 2 normaliza a `1234.50` → válido, `attempts=2`. [DOC]
3. Mismo error de formato en el 80% del lote: no subir retries; añadir normalización de separador decimal en post-process y bajar el retry a respaldo. [DOC] Verificar con set fijo. [SUPUESTO]

## Argumento de certificación

- Distinguir error recuperable (formato) de no recuperable (dato ausente en la fuente).
- Describir el loop con feedback específico (error real, no mensaje genérico).
- Identificar patrones sistemáticos para un fix estructural en lugar de subir retries.
- Escalar con la cadena de errores cuando `max_retries` se agota (`needs_human_review`).
- Probar que ningún intento supera el cap total de 2-3 intentos ni reintenta un error marcado como no recuperable.

## Acceptance criteria

- El feedback de cada retry contiene el mensaje literal del validador (campo + razón), no un texto genérico. [DOC]
- Existe una función de clasificación recuperable/no-recuperable invocada ANTES de gastar el intento. [DOC]
- Ningún caso supera el cap de 2-3 intentos sobre el set fijo. [DOC] Verificar con `scripts/check.sh`. [CONFIG]
- Toda salida no validada se marca `needs_human_review` con `error_chain` no vacío; ninguna pasa silenciosa a downstream. [DOC]
- Un error no recuperable corta el loop sin reintentar. [SUPUESTO] Verificar con fixture de dato ausente.

## Cuándo activar

- Una extracción tipada (Pydantic / JSON Schema) falla validación y hay que decidir el retry.
- Escenarios CI/CD y Structured Extraction donde el contrato downstream exige salida válida.
- Cuando aparece un loop de reintentos sin feedback o se acepta salida inválida en silencio.

## Skills relacionadas

- `katas-provenance-preservation`
- `katas-confidence-stratified-sampling`
- `katas-false-positive-criteria`
- `katas-multipass-prompt-chaining`
