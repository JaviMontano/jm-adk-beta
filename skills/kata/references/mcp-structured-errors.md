<!-- distilled from alfa skills/katas-mcp-structured-errors -->
<!-- Errores MCP tipados (isError, errorCategory, isRetryable, retryAfterSeconds); la politica de retry vive en el cliente. -->
# Kata 06 · Errores estructurados en MCP

## Qué es

Un servidor MCP que falla devuelve un payload tipado con `isError`, `errorCategory`, `isRetryable` y `retryAfterSeconds`. El agente decide entre reintentar, escalar o abortar leyendo esos flags, no la prosa del mensaje. `explanation` existe para el humano que audita el log, no para que el modelo lo interprete. Las políticas de retry concretas (backoff, número máximo de intentos) viven en el cliente. [DOC]

Escenarios canónicos: Customer Support y API Integration Reliability.

**Alcance.** Define el *contrato* de error y quién consume cada campo. No define el wire format del transporte MCP ni el esquema de éxito. [SUPUESTO]
**Anti-alcance.** No mueve la política de retry al modelo, no usa `explanation` en lógica de control, no inventa categorías fuera del enum cerrado. [DOC]

## Por qué importa (falla que evita)

Un string genérico como `"something went wrong"` obliga al modelo a adivinar la intención. El resultado es uno de tres comportamientos degenerados: reintenta para siempre, abandona una operación que solo necesitaba backoff, o escala a un humano casos que se habrían resuelto solos con una espera. El error sin estructura traslada al modelo una decisión que debería ser determinista. [INFERENCIA]

## Modelo mental

- Tres ejes de decisión por fallo: ¿es error? (`isError`), ¿es reintentable? (`isRetryable`), ¿qué categoría? (`errorCategory`). [DOC]
- El agente lee flags, nunca prosa. La prosa (`explanation`) es para auditoría humana del log. [DOC]
- Las políticas de retry (backoff exponencial, n máximo de intentos) viven en el cliente, no en el modelo. [DOC]
- Error sin categoría → tratar como non-retryable, categorizar como `unknown`, loggear. [DOC]

### Enum cerrado de `errorCategory` → acción del cliente

| `errorCategory` | `isRetryable` | Acción y trade-off | Campo clave |
|---|---|---|---|
| `transient` | true | Backoff exponencial con jitter. Trade-off: latencia añadida vs. evitar tormenta de reintentos. | — |
| `rate_limit` | true | Esperar **exactamente** `retryAfterSeconds`; nunca backoff propio (re-dispara el límite). | `retryAfterSeconds` |
| `auth` | false | Escalar a humano / refrescar credencial. Reintentar quema cuota sin chance de éxito. | — |
| `not_found` | false | Abortar la rama; el recurso no existe, reintentar es inútil. | — |
| `validation` | false | Abortar y reportar; el input es el defecto, no el momento. | `explanation` (al humano) |
| `unknown` | false | Fallback seguro ante categoría ausente/no reconocida: non-retryable + log. | — |

Regla de oro: ante ambigüedad, **non-retryable gana**. Un falso `transient` cuesta una tormenta; un falso `not_found` cuesta un reintento perdido. [INFERENCIA]

## Patrón correcto

```python
# Servidor MCP: devuelve un contrato tipado
try:
    return do_work(args)
except RateLimitException as e:
    return {
        "isError": True,
        "errorCategory": "rate_limit",
        "isRetryable": True,
        "retryAfterSeconds": e.retry_after,
        "explanation": f"Rate limit alcanzado; reintentar en {e.retry_after}s",
    }

# Cliente: la política de retry vive aquí, no en el modelo
if result.get("isError") and result.get("isRetryable"):
    delay = result.get("retryAfterSeconds")
    time.sleep(delay if delay is not None else backoff(attempt))  # rate_limit usa el valor exacto
    return retry(args)
if result.get("errorCategory") in ("auth", "validation"):
    return escalate_to_human(result)
# categoría ausente o no reconocida → fallback seguro
if result.get("isError"):
    log.warning("unknown error category", extra=result)
    return abort(result)
```

## Anti-patrón

```python
except Exception as e:
    return {"error": f"failed: {e}"}  # string genérico, sin flags tipados
```

Variantes igual de rotas: `isRetryable: True` sin `errorCategory`; backoff propio sobre `rate_limit` ignorando `retryAfterSeconds`; el cliente parseando `explanation` con regex para decidir. [INFERENCIA]

## Edge cases y modos de fallo

- `isRetryable: true` pero `retryAfterSeconds` ausente → usar backoff del cliente, no `sleep(None)`. [CÓDIGO]
- `errorCategory` fuera del enum → homologar a `unknown`, nunca crashear el cliente. [INFERENCIA]
- `rate_limit` con `retryAfterSeconds` enorme → respetar o abortar por presupuesto de tiempo; nunca acortarlo. [SUPUESTO]
- `isError: false` con payload de error → contradicción; el cliente confía en `isError`, loggea la inconsistencia. [INFERENCIA]
- Cadena de reintentos sin tope → el cliente impone `max_attempts`; el contrato no lo lleva. [DOC]

## Argumento de certificación

Los errores de MCP son contratos tipados (`isError`, `errorCategory`, `isRetryable`); la política de retry vive en el cliente, no en el modelo. Quien certifica esta kata debe demostrar que el servidor emite los flags, que el cliente decide a partir de ellos y que `explanation` no participa en la lógica de control. [DOC]

### Criterios de aceptación
- El servidor emite los cuatro campos; `errorCategory` pertenece al enum cerrado. [DOC]
- El cliente decide solo por flags; `explanation` solo aparece en logs/escalado humano. [DOC]
- `rate_limit` respeta `retryAfterSeconds` exacto; el resto de retryables usa backoff del cliente. [DOC]
- Categoría ausente/desconocida → `unknown`, non-retryable, loggeada; nunca crash. [DOC]
- Existe un tope de reintentos en el cliente, no en el payload. [DOC]

## Cuándo activar

- Se diseña o revisa el contrato de error de un tool o servidor MCP.
- Un agente reintenta indefinidamente, abandona prematuro, o escala fallos que solo necesitaban backoff.
- Se necesita separar la semántica del error (servidor) de la política de retry (cliente).

## Skills relacionadas

- `katas-validation-retry-error-feedback`
- `katas-error-propagation-multi-agent`
- `katas-tool-description-quality`
