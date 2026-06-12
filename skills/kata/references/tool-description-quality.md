<!-- distilled from alfa skills/katas-tool-description-quality -->
<!-- Calidad de descripciones de tools como contrato de seleccion; rename y split sobre overloading para evitar misroute. -->
# Katas Tool Description Quality

## Qué es

La descripción de un tool es el único mecanismo que el modelo usa para escoger entre tools similares; nunca ve la implementación. [DOC] Una buena descripción no es prosa decorativa: es un contrato de uso que declara tres cosas concretas: el **input format** que acepta, **ejemplos de query** que la disparan, y la **frontera explícita** ("usa esto en lugar de X cuando..."). [DOC] El nombre del tool es parte del contrato; cuando el nombre confunde, ninguna cantidad de explicación lo arregla. [INFERENCIA]

Aplica a tres escenarios: Customer Support (enrutamiento entre tools de respuesta), Multi-Agent (selección entre agentes con capacidades solapadas) y Dev Productivity (tools de análisis y extracción que compiten por el mismo turno). [DOC]

## Por qué importa (falla que evita)

Cuando dos tools tienen descripciones genéricas (`Analyzes content` vs `Analyzes documents`), el modelo enruta mal en 20–30% de los turnos. [INFERENCIA] El síntoma es traicionero: una "respuesta razonable pero del tool incorrecto", que pasa desapercibida en los logs hasta que un componente downstream rompe porque recibió el shape equivocado. [INFERENCIA] No es un crash visible; es deriva silenciosa de routing que se acumula. [SUPUESTO]

## Modelo mental

- **Descripción = contrato de uso.** Contratos solapados son ambiguos por diseño; el modelo no puede desempatar lo que tú no desambiguaste. [DOC]
- **Renombrar suele superar a "explicar más"** cuando el nombre confunde: `analyze_content` → `extract_web_results` resuelve más misroutes que tres párrafos extra. [INFERENCIA]
- **Splitting beats overloading:** cinco tools con un propósito único son mejores que uno con cinco modos. Un tool multimodo obliga al modelo a inferir el modo además del tool. [DOC]
- **El system prompt interactúa con la descripción:** ciertas keywords en el prompt pueden sesgar el routing hacia un tool aunque el contenido pida otro. [INFERENCIA]
- La frontera debe ser **recíproca:** si A dice "para PDF usa B", B debe decir "para HTML usa A". [DOC]

## Contrato deterministico

Usa los assets solo cuando el caso requiera detalle verificable: [CONFIG]

- `assets/tool-description-contract.json`: campos obligatorios del reporte. [CONFIG]
- `assets/description-quality-policy.json`: elementos minimos por descripcion. [CONFIG]
- `assets/routing-risk-policy.json`: reglas para overlap, rename, split y sesgo de prompt. [CONFIG]
- `assets/action-priority-policy.json`: orden deterministico de acciones. [CONFIG]
- `assets/evidence-policy.json`: evidencia aceptada y claims bloqueados. [CONFIG]

Cuando se requiera handoff machine-checkable, emite JSON que pase:

```bash
python3 -B skills/katas-tool-description-quality/scripts/validate_tool_description_quality.py <report.json>
```

## Patrón correcto

```json
{
  "name": "extract_web_results",
  "description": "Parses HTML pages from a search query into a list of {title,url,snippet}. Use when input is a URL or raw HTML; for PDF/DOCX use parse_document instead."
}
```

Con su par recíproco `parse_document`, cuya descripción declara el input format inverso y devuelve la frontera ("para HTML o URLs usa `extract_web_results`"). [DOC] La descripción correcta cubre los tres campos del contrato: **format** (HTML/URL), **ejemplo de query** (search query), **frontera** (PDF/DOCX → otro tool). [DOC]

## Anti-patrón

```json
[
  {"name":"analyze_content","description":"Analyzes content"},
  {"name":"analyze_document","description":"Analyzes documents"}
]
```

Dos contratos genéricos y solapados, sin input format, sin frontera, sin ejemplo de query. El modelo adivina y acierta el 70–80% de las veces. [INFERENCIA] Mismo verbo (`Analyzes`), sustantivos casi sinónimos (`content`/`document`), cero frontera recíproca: la firma textual del overlap. [DOC]

## Casos límite

- **Rename rompe llamadas existentes:** cambiar el `name` invalida prompts, tests y cachés que referencian el nombre viejo. Renombra solo con migración coordinada del lado del cliente. [SUPUESTO]
- **Split multiplica la superficie de routing:** cinco tools de propósito único pueden saturar la ventana de selección si el toolset ya es grande; el split ayuda contra overloading, no contra exceso de tools. [INFERENCIA]
- **Frontera no recíproca:** declarar "para PDF usa B" en A pero omitir el par en B reintroduce ambigüedad desde el otro lado; la frontera debe existir en **ambas** descripciones. [DOC]
- **Sesgo del system prompt sobrevive a buenas descripciones:** una keyword del prompt puede ganarle a la frontera; neutralízala enunciando la frontera explícitamente, no solo afinando el prompt. [INFERENCIA]
- **Solapamiento legítimo:** si dos tools deben cubrir el mismo input por diseño (p. ej. fallback), la frontera debe declarar el criterio de desempate (coste, latencia), no fingir exclusividad. [SUPUESTO]

## Anti-scope

- No define el **schema de parámetros** del tool (tipos, required); cubre la descripción/contrato de selección, no la firma de input JSON. [DOC]
- No cubre selección de **built-in tools** ni de MCP servers (ver skills relacionadas). [DOC]
- No mide accuracy de routing en producción; propone el contrato, no instrumenta el A/B. [INFERENCIA]
- No reescribe el system prompt; solo neutraliza su sesgo vía frontera en la descripción. [SUPUESTO]

## Argumento de certificación

Para certificar dominio de esta kata hay que sostener cuatro afirmaciones:

1. La descripción es el árbitro de selección entre tools; el modelo no ve la implementación. [DOC]
2. Saber identificar tools ambiguos por contrato solapado (mismo verbo, sustantivos casi sinónimos, cero frontera). [DOC]
3. Proponer **rename + split** antes que "explicar más" cuando el nombre es la fuente de confusión. [DOC]
4. Detectar keywords del system prompt que sesgan el routing y neutralizarlas enunciando la frontera explícitamente en la descripción. [DOC]

## Criterios de aceptación

- Cada descripción declara los tres campos: input format, ejemplo de query y frontera explícita. [CONFIG]
- Toda frontera es recíproca: si A nombra a B, B nombra a A con el criterio inverso. [DOC]
- Ante nombre confuso, la acción priorizada es rename+split antes que ampliar prosa. [CONFIG]
- El reporte JSON valida contra `assets/tool-description-contract.json` y pasa `validate_tool_description_quality.py` sin red ni random. [CONFIG]

## Cuándo activar

- Hay dos o más tools que el modelo confunde y se observan respuestas correctas pero del tool equivocado.
- Se diseña una toolset nueva y se quiere prevenir misroute por contrato solapado.
- Un tool acumula modos (overloading) y conviene evaluar split.
- El system prompt menciona keywords que sesgan el routing hacia el tool equivocado.

## Skills relacionadas

- `katas-mcp-server-configuration`
- `katas-builtin-tool-selection`
- `katas-custom-commands-skills`
