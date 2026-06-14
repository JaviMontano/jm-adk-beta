<!-- distilled from alfa skills/katas-multiagent-error-propagation -->
<!-- Propagacion de errores multi-agente: distinguir access failure de valid empty, local recovery primero y coverage gap annotation. -->
# Katas Multiagent Error Propagation

## Qué es

En una arquitectura hub-and-spoke, un coordinador delega búsquedas en subagentes. Cuando un subagente falla, debe propagar el error al coordinador con **contexto estructurado**, no un payload silencioso. [DOC] El contrato mínimo de propagación es:

`failure_type`, `attempted_query`, `partial_results`, `suggested_alternatives`. [DOC]

Cuatro reglas gobiernan la propagación:

1. **Local recovery primero** — el subagente reintenta fallos transitorios (broaden query, longer timeout) antes de propagar. [DOC]
2. **Distinguir access failure de valid empty** — un timeout o un permission denied NO es lo mismo que una búsqueda que devolvió 0 matches legítimamente. [DOC]
3. **Coverage gap annotation** — cuando un dominio queda sin cubrir, se anota explícitamente en el synthesis del coordinador. [DOC]
4. **Nunca enmascarar error como success vacío** — un fallo nunca se devuelve como `{results:[]}`. [DOC]

## Por qué importa (falla que evita)

Devolver `{results:[]}` en un timeout hace que el coordinador asuma "no había información" y produzca un report confiado con un **hueco silencioso**: el usuario recibe una respuesta que parece completa pero omite una fuente que simplemente falló. [INFERENCIA] Por el otro extremo, un genérico `'search unavailable'` priva al coordinador del contexto (`attempted_query`, `suggested_alternatives`) necesario para decidir alternativas o anotar el gap. [INFERENCIA] Ambos modos rompen la confiabilidad del synthesis multi-agente. [DOC]

## Modelo mental

- **Local recovery primero:** el subagente reintenta transients (broaden, longer timeout) antes de escalar al coordinador. [DOC]
- **Access failure != valid empty:** timeout/permission = el sistema no pudo mirar; search OK con 0 matches = el sistema miró y no había nada. Señales y manejo distintos. [DOC]
- **Coverage gap annotation:** si una fuente no se pudo consultar, el synthesis lo declara explícitamente; no se infiere ausencia de datos. [DOC]
- **Nunca enmascarar:** un error de acceso jamás se serializa como un success vacío. `success:False` con contexto, o `success:True, empty_valid:True`. [DOC]
- **`retryable=False` (permission)** es una señal explícita: escalar / anotar coverage gap, no reintentar la misma query. [DOC]

## Contrato determinístico

Cada respuesta de subagente cae en exactamente una de tres formas; el coordinador ramifica por `success`/`empty_valid`, nunca por prosa. [INFERENCIA]

| Caso | Forma del payload | Acción del coordinador |
|------|-------------------|------------------------|
| Hit | `success:True, results:[...]` | Sintetizar resultados |
| Vacío válido | `success:True, results:[], empty_valid:True` | Registrar "miró, no había nada" |
| Fallo de acceso | `success:False, failure_type, attempted_query, partial_results, suggested_alternatives` | Anotar coverage gap; evaluar `retryable` |

`partial_results` permite degradación parcial: si la primera página llegó y la segunda hizo timeout, se propaga lo recuperado más el fallo, no se descarta todo. [SUPUESTO]

## Patrón correcto

```python
# Subagente: propagación estructurada con local recovery
def search_subagent(query):
    try:
        results = http_search(query, timeout=10)
        if not results:
            return {"success": True, "results": [], "empty_valid": True}
        return {"success": True, "results": results}
    except TimeoutError:
        try:
            return {"success": True, "results": broaden(query)}  # local recovery
        except Exception:
            return {
                "success": False,
                "failure_type": "timeout",
                "attempted_query": query,
                "partial_results": [],
                "suggested_alternatives": ["broaden terms", "longer timeout"],
            }
    except PermissionError as e:
        return {
            "success": False,
            "failure_type": "permission",
            "retryable": False,
            "explanation": str(e),
        }
```

## Anti-patrón

```python
# Enmascara el error como success vacío:
# el coordinador asume "no había info" y escribe un report con hueco silencioso.
def search_subagent(query):
    try:
        return {"results": http_search(query, timeout=10)}
    except Exception:
        return {"results": []}
```

Segundo anti-patrón: el genérico `return {"error": "search unavailable"}`. No miente sobre el éxito, pero descarta `attempted_query` y `suggested_alternatives`, dejando al coordinador sin material para decidir alternativa o anotar el gap con precisión. [INFERENCIA]

## Decisiones y trade-offs

- **`empty_valid` explícito vs `results:[]` desnudo:** el flag cuesta un campo extra pero elimina la ambigüedad timeout-vs-vacío en el coordinador. Sin él, "miró y no había" y "no pudo mirar" colapsan en la misma señal. [INFERENCIA]
- **Local recovery en el subagente vs en el coordinador:** reintentar transients localmente evita un round-trip hub-spoke y mantiene el contexto del fallo donde existe. Trade-off: el subagente debe acotar sus reintentos (1 retry, no bucle) para no esconder latencia al coordinador. [SUPUESTO]
- **`partial_results` vs todo-o-nada:** propagar lo parcial mejora la cobertura del synthesis, pero el coordinador debe marcar el resultado como incompleto, no como final. [SUPUESTO]
- **`retryable` flag vs inferir del `failure_type`:** un flag explícito es contrato; inferir (timeout→retry, permission→no) acopla al coordinador a la taxonomía y rompe si se añade una categoría. [INFERENCIA]

## Edge cases y modos de falla

- **Timeout tras resultados parciales:** primera página OK, segunda timeout → `success:False` con `partial_results` poblado, no `[]`. El coordinador usa lo parcial y anota el gap. [SUPUESTO]
- **Permission denied:** `retryable:False`; reintentar la misma query es inútil y quema presupuesto. Escalar o anotar, nunca loop. [DOC]
- **Vacío legítimo confundido con fallo:** marcar `empty_valid:True` evita que el coordinador trate "0 matches reales" como una fuente caída. [DOC]
- **Local recovery infinito:** el reintento debe ser acotado (un intento de broaden); un bucle de recovery esconde latencia y puede colgar al coordinador. [SUPUESTO]
- **`failure_type` desconocido:** si el subagente no clasifica el error, propagar `failure_type:"unknown"` con `retryable:False` y loggear; nunca silenciar. [INFERENCIA]
- **Subagente que crashea sin payload:** el coordinador trata la ausencia de respuesta como fallo de acceso, no como vacío válido; un timeout del lado coordinador es coverage gap. [INFERENCIA]

## Supuestos y límites (anti-scope)

- Asume topología hub-and-spoke con un coordinador que sintetiza; no cubre malla peer-to-peer ni agentes sin coordinador. [SUPUESTO]
- Define el **contrato de propagación** (forma del payload + ramas), no la **política de retry/backoff** del coordinador (ver `katas-validation-retry-feedback`). [DOC]
- No cubre el contrato de error de un servidor MCP individual (`isError`, `errorCategory`); eso es `katas-mcp-structured-errors`. Aquí el foco es subagente→coordinador. [DOC]
- No prescribe el formato del coverage gap en el report final, solo exige que se anote explícitamente. [SUPUESTO]
- Asume que `broaden(query)` y los `suggested_alternatives` son específicos del dominio; el kata no los define. [SUPUESTO]

## Argumento de certificación

- Distinguir **access failure** de **valid empty** y manejarlos por ramas separadas. [DOC]
- Defender **local recovery** + **propagación estructurada** (failure_type, attempted_query, partial_results, suggested_alternatives). [DOC]
- Insistir en **coverage gap annotation** explícita en el synthesis. [DOC]
- Rechazar enmascarar errores como success vacío y rechazar el genérico `'search unavailable'`. [DOC]
- Reconocer `retryable=False` (permission) como señal de escalar/anotar, no de reintentar la misma query. [DOC]

## Criterios de aceptación

- Un timeout produce `success:False` con los cuatro campos del contrato, nunca `{results:[]}`. [DOC]
- Una búsqueda con 0 matches reales produce `success:True, empty_valid:True`, distinguible de un fallo. [DOC]
- Un `permission` denied lleva `retryable:False` y no dispara reintento de la misma query. [DOC]
- El synthesis del coordinador anota explícitamente toda fuente no consultada como coverage gap. [INFERENCIA]
- El local recovery está acotado (no bucle) y solo aplica a transients. [SUPUESTO]

## Cuándo activar

- Diseño o revisión de arquitecturas hub-and-spoke / multi-agente donde un coordinador sintetiza resultados de subagentes. [DOC]
- Cuando un report multi-agente "se ve completo" pero podría tener huecos silenciosos por fallos de fuente. [INFERENCIA]
- Diferenciar manejo de timeout/permission vs búsqueda vacía válida. [DOC]
- Escenarios de Customer Support y Multi-Agent con orquestación de búsquedas. [DOC]

## Skills relacionadas

- `katas-mcp-structured-errors`
- `katas-validation-retry-feedback`
- `katas-critical-self-correction`
- `katas-independent-reviewer-multipass`
