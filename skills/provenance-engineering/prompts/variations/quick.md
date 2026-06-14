# Prompt — Variation: Quick

Revision rapida de provenance sobre un fragmento de pipeline o un merge de claims. Un solo paso, sin rediseno completo.

## Pide (solo si falta)

- El inventario de `source_id` validos.
- El atributo y los valores en conflicto (si los hay).

## Verifica en orden

1. ¿Algun claim sin `source[]` o con placeholder? -> bloquea.
2. ¿Algun `source_id` fuera del inventario? -> falla duro.
3. ¿Algun conflicto promediado/elegido en silencio? -> marca `conflict=true`, conserva ambas fuentes, enruta a cola humana.
4. ¿Diferencia solo de formato? -> normaliza, no marques conflicto espurio.
5. ¿`as_of` visible en el render? -> si no, no esta listo.

## Entrega

Lista corta de hallazgos con el fix minimo por cada uno, cada hallazgo con su tag Alfa-core. Si todo pasa, dilo con la evidencia (no "se ve bien"). Sin promedios, sin heuristicas de resolucion, sin precios inventados.
