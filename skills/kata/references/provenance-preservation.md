<!-- distilled from alfa skills/katas-provenance-preservation -->
<!-- Provenance tipada: no hay claim sin source; conflictos marcados con conflict true y escalados, nunca promediados. -->
# Katas Provenance Preservation

## Qué es

Cada afirmación factual (`claim`) extraída de fuentes mantiene un mapeo tipado a su origen: `claim, source_id, source_name, publication_date`. Los conflictos entre fuentes NO se resuelven en silencio: se marcan con `conflict=true` y se enrutan a un humano. La provenance no es un metadato opcional sino parte del schema del output: si un claim no puede señalar su fuente, no debe existir en el resultado. [DOC]

**Anti-scope.** Este kata cubre el *contrato de trazabilidad* del output (cada claim apunta a una fuente registrada; los conflictos se preservan y escalan). NO cubre: la calidad o veracidad de la fuente en sí (un `source_id` válido no implica fuente confiable), la deduplicación semántica de claims equivalentes redactados distinto, el ranking de fuentes por autoridad, ni la resolución del conflicto — eso es decisión humana aguas abajo (Kata 16). El kata garantiza que la decisión sea *posible y auditable*, no que sea correcta. [SUPUESTO]

**Supuestos del contrato.** Existe un `source_registry[]` poblado antes de emitir claims; cada subagente que aporta hechos conoce el `source_id` de lo que leyó y lo propaga; el schema del output es validable offline (no depende del juicio del modelo en runtime). Si el registry no se puebla o un subagente pierde su `source_id`, el claim degrada a "huérfano" y debe fallar la validación, no colarse sin fuente — esa es la falla que el kata evita. [SUPUESTO]

## Por qué importa (falla que evita)

Tras agregar contenido de muchas fuentes vía subagentes (Kata 4), perder el hilo de "quién dijo qué" hace imposible auditar el resultado. Los resúmenes en prosa libre se ven correctos y alucinan sin que se note: el lector no tiene forma de distinguir un dato verificado de uno inventado. La provenance tipada es la única defensa, porque convierte "confía en mi resumen" en "verifica cada claim contra su fuente". [DOC]

## Modelo mental

- No hay claim sin source: es un invariante de schema, no una buena práctica. [DOC]
- Si dos fuentes contradicen, se registran ambas bajo `conflict=true`; no se promedia, no se elige. [DOC]
- La fecha de publicación importa pero no decide: el humano necesita verla para juzgar (la fuente más reciente no siempre gana). [INFERENCIA]
- El conflicto se escala a humano (vía Kata 16), no se resuelve por heurística del modelo. [DOC]
- La agregación tras subagentes paralelos (Kata 4) es el punto donde la provenance se pierde si no es un campo obligatorio del schema. [INFERENCIA]
- Un `source_id` presente pero inexistente en el registry es peor que uno faltante: simula trazabilidad. La validación cruza ambos. [INFERENCIA]

## Decisión: preservar el conflicto vs resolverlo en el modelo

Se elige **registrar ambos valores y escalar** en lugar de que el modelo elija uno. Trade-off: el output queda "incompleto" (un claim con dos cifras y `needs_human_review=true`), lo que obliga a un paso humano antes de consumirlo. A cambio se gana la propiedad que justifica el kata: ninguna contradicción se borra en silencio. La completitud aparente que se pierde es exactamente la que produce alucinación con cara de certeza; preferimos un hueco declarado a una respuesta fabricada. La heurística `newest_wins` se rechaza porque la fecha es señal, no veredicto: un dato preliminar reciente puede ser menos fiable que uno auditado más antiguo. [INFERENCIA]

## Patrón correcto

```python
claims = [
    {
        "claim": "ARR Q3 2025 = 12M USD",
        "sources": [
            {"id": "doc-A", "name": "Annual Report", "date": "2025-12-01"},
            {"id": "doc-B", "name": "Investor Deck", "date": "2025-09-15"},
        ],
        "conflict": False,
    },
    {
        "claim": "Headcount end-2025",
        "sources": [
            {"id": "doc-A", "value": "450"},
            {"id": "doc-C", "value": "462"},
        ],
        "conflict": True,
        "needs_human_review": True,
    },
]
```

## Anti-patrón

```python
summary = "La empresa tiene ARR de 12M USD y 462 empleados..."
# sin source_id, sin fecha, sin conflicto marcado: provenance perdida
```

## Casos límite

- *Una sola fuente para un claim*: válido, `sources[]` con un elemento, `conflict=false`. El invariante exige ≥1 fuente, no ≥2. [DOC]
- *Dos fuentes coinciden en el valor*: NO es conflicto; se listan ambas con `conflict=false` (refuerzo, no contradicción). El conflicto es por valor divergente, no por fuente múltiple. [INFERENCIA]
- *Tres o más fuentes, una discrepa*: `conflict=true` y se preservan las tres; no se vota por mayoría ni se descarta el outlier — el humano ve la distribución completa. [INFERENCIA]
- *Claim derivado de cómputo* (p.ej. suma de dos cifras): hereda la provenance de TODOS los insumos; conectar con Kata 15 para que la verificación numérica y la trazabilidad no se separen. [INFERENCIA]
- *Subagente devuelve claim sin `source_id`*: rechazar en el límite de agregación (Kata 4), no rellenar con un id placeholder ni con el último source visto. [SUPUESTO]
- *Fechas en formatos o zonas distintas*: normalizar a ISO-8601 antes de comparar; una fecha no parseable marca el source como inválido, no como "sin fecha". [INFERENCIA]

## Argumento de certificación

- Enunciar el invariante "no hay claim sin source" como propiedad del schema, no como recomendación. [DOC]
- Describir la política de conflictos: registrar ambas posturas, no promediar ni elegir, escalar vía Kata 16. [DOC]
- Conectar con Kata 4 (agregación tras subagentes paralelos) y Kata 15 (verificación numérica). [DOC]
- Demostrar un test estructural que asserta que cada `claim` del output tiene un campo `sources[]` no vacío con `source_id` existente. [DOC]

## Criterios de aceptación

- Todo `claim` del output tiene `sources[]` no vacío. (Prueba: filtrar claims con `len(sources)==0` debe dar conjunto vacío.) [DOC]
- Todo `source_id` referenciado existe en `source_registry[]`. (Prueba: `set(claim_sources) - set(registry_ids)` es vacío.) [INFERENCIA]
- Todo claim con valores divergentes tiene `conflict=true`, `needs_human_review=true` y `escalation_route` declarada. (Prueba: ningún claim con ≥2 `value` distintos tiene `conflict=false`.) [DOC]
- Ninguna resolución usa `average`, `newest_wins`, `model_choice` ni `silent_choice`. (Prueba: el conjunto de valores de un claim en conflicto coincide con el de sus fuentes; no aparece un valor sintético ausente de toda fuente.) [INFERENCIA]
- Dado solo el JSON (sin la conversación ni las fuentes), un auditor puede ubicar cada cifra en su origen. [INFERENCIA]

## Contrato determinístico

- `source_registry[]` declara cada fuente con `source_id`, `source_name` y `publication_date`. [CONFIG]
- Cada `claim` debe tener `sources[]` no vacío y cada `source_id` debe existir en `source_registry`. [CONFIG]
- Los conflictos deben conservar todos los valores contradictorios, marcar `conflict=true`, fijar `needs_human_review=true` y declarar `escalation_route`. [CONFIG]
- Está prohibido resolver conflictos con `average`, `newest_wins`, `model_choice` o `silent_choice`. [CONFIG]
- La validación offline usa `assets/provenance-preservation-contract.json`, `assets/claim-source-policy.json`, `assets/conflict-policy.json` y `assets/evidence-policy.json`. [CONFIG]
- Comando local: `bash skills/katas-provenance-preservation/scripts/check.sh`. [CONFIG]

## Cuándo activar

- Extracción estructurada que agrega datos de múltiples documentos o fuentes. [DOC]
- Salidas de orquestación multi-agente donde varios subagentes aportan hechos. [DOC]
- Cualquier reporte factual que deba ser auditable claim por claim. [DOC]
- Cuando dos fuentes pueden contradecirse y la respuesta debe preservar ambas. [DOC]

## Skills relacionadas

- `katas-parallel-subagent-aggregation`
- `katas-numeric-verification`
- `katas-human-escalation`
