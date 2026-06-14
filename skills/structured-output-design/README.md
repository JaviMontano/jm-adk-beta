# structured-output-design

## Qué hace

Diseña la extracción estructurada de un modelo Claude como un **contrato de datos
verificable**: un JSON Schema defensivo emitido por una tool forzada, no prosa que
luego se parsea con `json.loads`. El resultado es una salida parseable de forma
determinista, auditable y resistente a alucinación de campos. [DOC]

Los cuatro pilares del contrato:

1. **`required` reales** — solo campos garantizados en la fuente, marcados por
   presencia real, no por deseo. [DOC]
2. **Unión nullable para opcionales** — `["string","null"]` en vez de defaults
   silenciosos (`''`, `0`, `"N/A"`) que contaminan el dataset aguas abajo. [DOC]
3. **Enum con válvula de escape** — `'other'` + campo hermano `*_details` para no
   perder señal cuando el dato no encaja en el catálogo. [DOC]
4. **Objeto cerrado** — `type=object` + `additionalProperties=false`: el modelo no
   inventa campos fuera del contrato. [CONFIG]

## Cuándo usarla

- Claude debe devolver datos que **otro sistema consume por código** (ETL, ingest a
  Postgres, pipelines de extracción). [DOC]
- `json.loads(text)` se rompe de forma intermitente (code fences, prosa extra). [INFERENCIA]
- Un opcional ausente se rellena con un default falso que ensucia el dataset. [DOC]
- Un enum cerrado pierde casos reales. [DOC]

## Cuándo NO usarla

- Prosa libre legítima (correo, resumen para humano): no impongas schema.
- El modelo debe elegir **entre varias tools**: usa `tool_choice="auto"`, no fuerces.
- Te piden saltar la validación o conservar defaults falsos: rechaza, no degrades.
- Fallback de texto libre + regex cuando la tool no sale: prohibido → retry/escalada.

## Cómo enruta y ejecuta

Spine **Inventariar → Modelar → Forzar → Parsear → Validar**:

1. Inventaria campos garantizados (`required`) vs. ocasionales (nullable).
2. Modela opcionales como unión nullable; añade válvula de escape a enums; cierra el objeto.
3. Define la tool con el schema como `input_schema`; fuerza `tool_choice` **solo** si no
   hay decisión de tool legítima.
4. Parsea desde `tool_use.input`, nunca desde el texto.
5. Valida el bloque contra el schema; enruta fallos a retry/escalada.

El `lead` resuelve el flujo, el `specialist` aporta profundidad de schema, el `support`
ejecuta los pasos y el `guardian` cierra el gate de aceptación.

## Referencias

- `SKILL.md` — capacidad, patrón correcto, anti-patrón, checklist de validación.
- `knowledge/body-of-knowledge.md` — conceptos, estándares y reglas de decisión.
- `knowledge/knowledge-graph.json` — grafo de los conceptos clave.
- `prompts/` — prompts primario, meta y variaciones quick/deep.
- `templates/output.md` — scaffold del contrato de salida entregable.
- `examples/` — ejemplo trabajado (factura → schema defensivo).
- `assets/` — paquete de policies JSON + rúbrica de calidad (ver `assets/README.md`).
- `evals/evals.json` — casos de evaluación de activación y boundaries.

## Evidencia

Todo claim lleva tag del set: `[CÓDIGO] [CONFIG] [DOC] [INFERENCIA] [SUPUESTO]`.
Una sola familia de marca por output; sin precios inventados; sin PII de cliente.
