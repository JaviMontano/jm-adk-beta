<!-- distilled from alfa skills/katas-posttooluse-normalization -->
<!-- Normalizacion de outputs heterogeneos via hook PostToolUse y updatedMCPToolOutput antes de entrar al historial del modelo. -->
# Katas Posttooluse Normalization

## Qué es

Kata 03 del kit JM-ADK. Un hook `PostToolUse` intercepta el `tool_response` heterogéneo de tools legacy (XML envuelto, códigos de estado arcanos como `0xA1`) y lo reescribe a JSON canónico mediante `updatedMCPToolOutput` antes de que el output entre al historial del modelo. El modelo nunca ve el XML crudo: ve solo el JSON limpio que el runtime garantiza. [DOC]

Escenarios canónicos: Customer Support y Legacy ERP Integration. [DOC]

## Por qué importa (falla que evita)

- Sin normalización central, cada token de XML legacy quema budget de contexto y dispersa la atención del modelo sobre ruido sintáctico. [INFERENCIA]
- Normalizar por-tool (cada tool decide si limpia su salida) es frágil: cualquier wrapper o handler nuevo que olvide aplicar la regla rompe la garantía y envenena el contexto con payloads sucios. [INFERENCIA]
- La normalización de outputs heterogéneos es responsabilidad del runtime, no convención voluntaria del autor de cada tool. [DOC]

## Modelo mental

- `PostToolUse` es runtime garantizado, no convención del autor de la tool: matchea por patrón y se aplica a TODAS las tools que matcheen. [DOC]
- `updatedMCPToolOutput` reemplaza el output crudo; el modelo nunca ve el XML. [DOC]
- Los mapas de traducción (`STATUS_MAP`) y esquemas viven en código recargable, en un solo lugar. [DOC]
- `additionalContext` anexa metadatos auditables (origen legacy, timestamp de normalización) sin contaminar el payload limpio que consume el modelo. [DOC]
- `PostToolUse` corre DESPUÉS de que la tool ya se ejecutó: normaliza el resultado, no lo bloquea. Para vetar la ejecución antes de que ocurra, ese es el dominio de `PreToolUse`, no de este kata. [DOC]

## Supuestos y límites (anti-scope)

- Aplica a salidas de tools cuyo `tool_response` es parseable de forma determinística (XML, campos posicionales, códigos tabulados). NO cubre normalizar prosa libre del modelo ni texto natural ambiguo: para eso, extracción defensiva con schema forzado. [SUPUESTO]
- El hook transforma la *forma* del payload, no garantiza la *veracidad* del dato legacy: si el ERP devuelve un `Total` erróneo, el JSON canónico propaga el mismo error bien tipado. [INFERENCIA]
- Asume que el matcher cubre exhaustivamente las tools legacy. Una tool legacy nueva fuera del patrón del matcher NO se normaliza y rompe la garantía silenciosamente: el matcher es el punto único de fallo a auditar. [INFERENCIA]
- NO sustituye validación de schema en cliente: `PostToolUse` reescribe, no valida tipos contra un contrato estricto server-side. Revalida el JSON canónico aguas abajo si el pipeline lo exige. [SUPUESTO]
- Un solo hook normalizando múltiples formatos heterogéneos se vuelve un dios-función: si conviven ≥2 dialectos legacy sin relación, prefiere matchers separados por familia de tool antes que ramificar dentro de un único `normalize_*`. [INFERENCIA]

## Patrón correcto

```python
STATUS_MAP = {"0xA1": "paid", "0xB2": "pending", "0xC3": "overdue"}

async def normalize_legacy(input, tool_use_id, ctx):
    raw = input["tool_response"]
    clean = {
        "order_id": raw.find("OrderId"),
        "status": STATUS_MAP.get(raw.find("StatusCode"), "unknown"),
        "amount": float(raw.find("Total")),
    }
    return {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "updatedMCPToolOutput": {"type": "text", "text": json.dumps(clean)},
            "additionalContext": "source=legacy_erp_xml; normalized=true",
        }
    }
```

## Anti-patrón

```python
# Cada tool decide por su cuenta si normaliza, via decorators @tool.
@tool
def get_order(id):
    raw = legacy_erp.fetch(id)
    return normalize(raw)  # frágil: depende de que cada autor lo recuerde

@tool
def get_invoice(id):
    return legacy_erp.fetch(id)  # un handler nuevo OLVIDÓ normalizar -> envenena contexto
```

## Casos límite

- **Código de estado desconocido** (`0xD4` no está en `STATUS_MAP`): cae en fallback explícito `unknown`, nunca lanza ni inventa un estado plausible. [DOC]
- **Campo ausente o vacío** en el XML (`raw.find("Total")` devuelve `None`): `float(None)` lanza; el hook debe envolver la coerción y degradar a `null`/`unknown`, no propagar la excepción al runtime. [INFERENCIA]
- **XML malformado o no parseable**: si el parseo falla, el hook NO debe pasar el crudo al modelo como fallback silencioso; debe emitir un payload canónico de error (`{"status":"parse_error"}`) auditable vía `additionalContext`. [SUPUESTO]
- **Tool legacy fuera del matcher**: no se normaliza. Se detecta auditando el matcher contra el inventario de tools, no en runtime. [INFERENCIA]
- **Doble normalización**: si un payload ya canónico vuelve a entrar al hook (re-ejecución/retry), el `STATUS_MAP.get(...)` sobre un valor ya mapeado cae en `unknown`. Haz la transformación idempotente o detecta el marcador `normalized=true`. [INFERENCIA]

## Decisiones y trade-offs

- **Hook central vs. normalización por-tool**: el hook centraliza la garantía a cambio de un punto único (el matcher) que hay que mantener al día. Se elige central porque el costo de un matcher desactualizado es auditable; el de "cada autor lo recuerda" es invisible hasta que envenena el contexto. [INFERENCIA]
- **`updatedMCPToolOutput` vs. `additionalContext` para el dato**: el JSON canónico va en `updatedMCPToolOutput` (lo consume el modelo); los metadatos de procedencia van en `additionalContext` (auditoría, no consumo). Mezclarlos reintroduce ruido en el contexto que el kata busca eliminar. [DOC]
- **`STATUS_MAP` en código recargable vs. inline**: vivir en un solo lugar recargable permite ampliar el mapa sin redeploy del hook y mantiene una fuente única de verdad. [DOC]

## Argumento de certificación

La normalización de outputs heterogéneos es responsabilidad del runtime vía `PostToolUse`, no convención de cada tool. Defiende: el hook matchea por patrón y garantiza la transformación para todas las tools; `updatedMCPToolOutput` impide que el XML crudo entre al historial; `additionalContext` sirve para metadatos auditables que el modelo no necesita ver. Quiz de referencia: C·B·B. [DOC]

## Contrato determinístico

- El hook debe declarar `hookEventName: "PostToolUse"` y estar registrado con matcher que cubra todas las tools legacy. [DOC]
- `updatedMCPToolOutput` debe reemplazar el payload crudo por JSON canónico. [DOC]
- `additionalContext` debe contener sólo metadatos auditables, no XML ni payload crudo. [DOC]
- `STATUS_MAP` y el esquema canónico viven en un lugar recargable. [DOC]
- Los códigos no mapeados deben caer en fallback explícito `unknown`. [DOC]
- La validación offline usa `assets/posttooluse-normalization-contract.json`, `assets/updated-output-policy.json`, `assets/normalization-policy.json` y `assets/evidence-policy.json`. [CÓDIGO]
- Comando local: `bash skills/katas-posttooluse-normalization/scripts/check.sh`. [CÓDIGO]

## Criterios de aceptación

- Inyectar un `tool_response` con `StatusCode=0xA1` produce `{"status":"paid"}` y el modelo nunca recibe el XML crudo. [DOC]
- Un `StatusCode` no presente en `STATUS_MAP` produce `"unknown"`, no excepción ni estado inventado. [DOC]
- El payload entregado al modelo (`updatedMCPToolOutput.text`) es JSON parseable; `additionalContext` no contiene XML ni payload crudo. [DOC]
- Una tool legacy adicional cubierta por el matcher se normaliza sin tocar su handler. [INFERENCIA]
- `bash skills/katas-posttooluse-normalization/scripts/check.sh` pasa contra los cuatro assets de política listados. [CÓDIGO]

## Modos de falla (qué vigilar)

- Matcher demasiado estrecho: tools legacy nuevas pasan sin normalizar. Detección: auditoría matcher↔inventario. [INFERENCIA]
- Excepción no capturada en la coerción (`float`, `find`) aborta el hook y filtra el crudo. Detección: test de campo ausente/malformado. [INFERENCIA]
- `additionalContext` usado como canal de datos: reintroduce ruido en contexto. Detección: assert de que no contiene XML. [DOC]
- Transformación no idempotente: un retry re-mapea y corrompe el estado. Detección: test de doble paso. [INFERENCIA]

## Cuándo activar

- Una o más tools devuelven payloads heterogéneos o legacy (XML, códigos de estado opacos) que conviene canonizar.
- Se quiere una sola fuente de verdad para la transformación, robusta ante tools nuevas.
- El usuario menciona `PostToolUse`, `updatedMCPToolOutput`, normalización de output o payloads legacy.

## Skills relacionadas

- `katas-tool-result-defensive-extraction`
- `katas-hook-driven-control`
- `katas-headless-code-review`

## Evidence Requirements

- Cita el código del hook, el `STATUS_MAP` y la firma de `updatedMCPToolOutput` usados.
- Marca inferencias y supuestos explícitamente.

## Update-Safety Notes

- Los archivos de soporte generados son missing-only por defecto.
- Usa `--force` solo tras revisar diffs.
