<!-- distilled from alfa skills/katas-headless-code-review -->
<!-- Code review headless con claude -p output-format json validado contra schema; el humano sigue siendo gate final de merge. -->
# Katas Headless Code Review

## Qué es

Claude Code corre en CI sin TTY (`claude -p`) y produce JSON estructurado con anotaciones por línea (`file,line,severity,rule_id,message`). El pipeline valida la salida contra un schema declarado y publica comentarios deterministas en el PR. Cero parsing de prosa libre: el modelo anota, el pipeline valida, el humano decide el merge. [DOC]

## Por qué importa (falla que evita)

Un reviewer humano no escala a 100 PRs/día. Un reviewer LLM en CI encuentra issues consistentes, pero solo si su salida es estructurada. Si se parsea prosa con regex (`grep -E 'ERROR|WARNING'`), el pipeline rompe el primer día que el modelo cambie de redacción o de idioma. La estructura no es cosmética: es la única forma de que la integración sobreviva a la variabilidad del modelo. [INFERENCIA]

## Modelo mental

- `claude -p 'prompt' --output-format=json` produce JSON validable contra un schema declarado, no prosa para humanos. [DOC]
- El schema es una lista de `Annotation`: `{file, line, severity, rule_id, message}`. [CÓDIGO]
- Si la salida no valida contra el schema, el job **falla** — no se "ajusta" el parser ni se publican comentarios parciales. [DOC]
- El humano sigue siendo el gate final de merge: el LLM **anota**, no **aprueba**. Puede tener falsos positivos y falsos negativos y no asume responsabilidad legal del merge. [DOC]
- Combina tres katas: extracción defensiva con schema (Kata 5), control por señal de salida (Kata 1) y el flag `--output-format=json`. [DOC]

## Supuestos y límites

- Se asume `claude` autenticado en CI vía secret (API key / token); sin credencial válida el job falla antes de anotar. Verificación: paso `claude --version` en el runner. [SUPUESTO]
- `--output-format=json` y `--schema` deben existir en la versión de CLI instalada; fijar versión (no `latest`) para que un cambio de flags no rompa el pipeline en silencio. [SUPUESTO]
- El schema cubre forma (campos, tipos, enum de `severity`), no veracidad: un JSON válido puede contener anotaciones incorrectas. La validación filtra ruptura de contrato, no FP/FN. [INFERENCIA]
- Anti-scope: NO usar este patrón para auto-aprobar/auto-mergear, ni para gates de seguridad que exijan cero FN (el LLM no garantiza recall), ni para review local interactivo. [DOC]
- Determinismo limitado: dos corridas sobre el mismo diff pueden anotar distinto. El contrato determinista es la *forma* y la *señal de salida*, no el *conjunto* de anotaciones. [INFERENCIA]

## Contrato del schema (forma mínima)

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "required": ["file", "line", "severity", "rule_id", "message"],
    "properties": {
      "file":     {"type": "string"},
      "line":     {"type": "integer", "minimum": 1},
      "severity": {"enum": ["error", "warning", "info"]},
      "rule_id":  {"type": "string"},
      "message":  {"type": "string", "minLength": 1}
    },
    "additionalProperties": false
  }
}
```

`additionalProperties: false` y `required` son los que convierten "JSON que parece bien" en contrato: un campo extra o faltante hace fallar la validación en vez de pasar silenciosamente. [CÓDIGO]

## Patrón correcto

```yaml
# .github/workflows/review.yml
- name: LLM review
  run: |
    claude -p "$REVIEW_PROMPT" \
      --output-format=json \
      --schema annotations.schema.json > out.json
    python scripts/post_annotations.py out.json
```

`post_annotations.py` valida `out.json` contra el schema antes de publicar: si no valida, sale con código distinto de cero y el job falla. [CÓDIGO]

## Anti-patrón

```bash
claude -p "$REVIEW_PROMPT" > review.txt
grep -E 'ERROR|WARNING|issue' review.txt | awk '{...}' | xargs gh pr comment
```

Parsea prosa libre con `grep`/`awk`: se rompe en cuanto el modelo cambie de redacción, idioma o formato. No hay contrato, solo heurística frágil. [INFERENCIA]

## Modos de falla y manejo esperado

| Modo de falla | Señal | Manejo correcto |
|---|---|---|
| JSON inválido / no parsea | exit ≠ 0 en validación | Job falla; nada se publica; humano investiga. [DOC] |
| JSON válido pero array vacío | exit 0, `[]` | "Sin hallazgos"; no es error. No fabricar comentarios. [INFERENCIA] |
| `claude -p` excede timeout/rate-limit | exit ≠ 0 de la CLI | Job falla limpio; reintento controlado, no parcheo del parser. [SUPUESTO] |
| Anotación con `line` fuera del diff | pasa schema, falla post | `post_annotations.py` descarta o degrada a comentario general. [SUPUESTO] |
| Modelo emite prosa antes/después del JSON | falla validación estricta | Tratar como inválido; no intentar "rescatar" con regex. [INFERENCIA] |

Regla transversal: ante cualquier ambigüedad, **fallar cerrado** (job rojo, sin publicar) en vez de publicar comentarios dudosos. [DOC]

## Argumento de certificación

El flag `--output-format=json` fuerza salida estructurada; la validación contra schema declarado es extracción defensiva (Kata 5); el control por señal de salida (Kata 1) decide éxito o fallo del job sin parsear prosa. Si el JSON no valida, el job falla y ningún comentario se publica: un humano investiga. El humano sigue siendo el gate final de merge porque el LLM puede tener FP/FN y no asume responsabilidad del merge. [DOC]

## Criterios de aceptación

- La CLI se invoca con `--output-format=json` y `--schema`; no se parsea prosa con `grep`/`awk` en ningún paso. [DOC]
- Existe un paso de validación contra schema que sale con código ≠ 0 cuando la salida no valida, y el job depende de esa señal. [CÓDIGO]
- Schema vacío (`[]`) se trata como "sin hallazgos", no como error. [INFERENCIA]
- Ningún paso del pipeline aprueba/mergea automáticamente; el merge queda a un humano. [DOC]
- La versión de la CLI está fijada (no `latest`). [SUPUESTO]

## Cuándo activar

- Se pide correr code review automatizado en CI/CD con `claude -p`.
- Se necesita salida estructurada (JSON) validada contra schema para publicar anotaciones en un PR.
- Se quiere reemplazar parsing de prosa por un contrato declarado y determinista.
- NO activar para code review interactivo en local sin pipeline, ni cuando el objetivo es aprobar/mergear automáticamente sin humano.

## Skills relacionadas

- `katas-defensive-structured-extraction`
- `katas-mcp-structured-errors`
- `katas-human-handoff-protocol`
