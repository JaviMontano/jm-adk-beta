<!-- distilled from alfa skills/katas-multipass-prompt-chaining -->
<!-- Prompt chaining multi-pass: pase local tipado por unidad y pase de integracion que solo ve resumenes, no las unidades crudas. -->
# Katas Multipass Prompt Chaining

Kata 12 · Prompt Chaining Multi-Pass · escenario Multi-Agent Orchestration.

## Qué es

Cuando una tarea no cabe cognitivamente en un solo prompt (auditar 50 archivos, resumir 200 páginas), se descompone en pases secuenciales. [DOC] El **pase local** procesa cada unidad de forma independiente y emite una salida tipada y compacta según un schema. El **pase de integración** solo ve los resúmenes tipados del pase 1, nunca las unidades crudas ni la totalidad sin filtrar. Cada pase declara su schema y el siguiente lo consume: los pases se componen como una pipeline. [DOC]

## Por qué importa (falla que evita)

Pedir "audita estos 50 archivos" en un solo prompt satura la atención del modelo: pierde detalles, alucina relaciones entre archivos y produce un resumen genérico que parece correcto pero no lo es. [INFERENCIA] Encadenar mantiene cada pase enfocado, barato y verificable, y permite paralelizar el pase 1 (un subagente por unidad). El cuello de botella deja de ser la ventana de contexto y pasa a ser el diseño de los schemas de transición. [INFERENCIA]

## Modelo mental

- **Pase 1 (paralelo):** una invocación por unidad, salida tipada y compacta según schema (p. ej. `FileFindings`). Cada unidad se procesa aislada, sin ver a las demás. [DOC]
- **Pase 2 (integración):** solo consume los outputs tipados del pase 1, no las unidades crudas; nunca ve la totalidad sin filtrar. [DOC]
- **Schemas declarados:** cada pase tiene un schema de salida; el siguiente lo consume exactamente. Sin estado de error tipado por unidad, el pase 2 cree que tiene N unidades válidas cuando tiene N-1: falla silenciosa. [INFERENCIA]
- **Pipeline:** los pases se componen; el límite de contexto de cada pase se respeta por separado. [DOC]

## Patrón correcto

```python
# Pase 1: por archivo, schema FileFindings (paralelizable)
local = [analyze_file(f, schema=FileFindings) for f in files]
# Pase 2: integración solo sobre resúmenes tipados, no sobre las unidades crudas
report = integrate(local, schema=AuditReport)
```

## Anti-patrón

```python
mega_prompt = "\n\n".join(open(f).read() for f in files)
create(messages=[{"role": "user", "content": f"Audita todo:\n{mega_prompt}"}])
# Satura la atención (Kata 11), no paraleliza, alucina entre archivos.
```

## Casos límite

- **Una unidad falla en el pase 1** → emite un `FileFindings` con estado de error tipado, no la omitas; si desaparece, el pase 2 integra N-1 creyendo que son N (falso "todo OK"). [INFERENCIA]
- **Hallazgo que solo existe en la relación entre dos unidades** → el pase 1 aislado no puede verlo por diseño; es responsabilidad del pase 2, que sí ve los resúmenes juntos. [INFERENCIA]
- **Resúmenes del pase 1 que aún no caben juntos en el pase 2** → encadena un nivel intermedio (map-reduce jerárquico: integra por lotes y luego integra los lotes), no infles la ventana. [SUPUESTO]
- **Schema del pase 1 demasiado verboso** → reintroduce el problema de contexto en el pase 2; el resumen tipado debe ser compacto, no un volcado del crudo. [INFERENCIA]
- **Tarea que cabe holgadamente en un prompt** → encadenar añade latencia y coste de coordinación sin beneficio; usa single-pass. [DOC]

## Anti-scope

- No define **cómo** paralelizar el pase 1 ni el aislamiento entre subagentes (ver `katas-subagents-parallel`). [DOC]
- No fija el presupuesto de tokens por pase ni cuándo una unidad "no cabe" (ver `katas-context-budget`). [DOC]
- No cubre la trazabilidad unidad→hallazgo a través de los pases (ver `katas-provenance-preservation`). [DOC]
- No es un esquema de consenso ni de votación entre pases; es una pipeline secuencial tipada. [DOC]

## Criterios de aceptación

- El pase 1 procesa cada unidad aislada y emite salida conforme a un schema declarado, incluido estado de error tipado por unidad. [DOC]
- El pase 2 consume únicamente los resúmenes tipados del pase 1, nunca las unidades crudas ni la totalidad sin filtrar. [DOC]
- El conteo de unidades es explícito de extremo a extremo: el pase 2 detecta N-1 en vez de asumir N. [INFERENCIA]
- Cada pase respeta su propio límite de contexto por separado; ningún pase reconcatena los crudos. [DOC]
- Existe justificación de por qué chaining vence a single-pass para esta tarea (overhead de coordinación < beneficio). [INFERENCIA]

## Argumento de certificación

- Identificar tareas candidatas para chaining versus single-pass (cuándo el overhead de coordinación se justifica y cuándo no). [DOC]
- Diseñar los schemas de transición entre pases, incluyendo estado de error tipado por unidad. [DOC]
- Conectar con Kata 4 (subagentes para paralelizar el pase 1) y Kata 11 (cada pase respeta el límite de contexto). [DOC]

## Cuándo activar

- La tarea no cabe holgadamente en una sola ventana de contexto (muchos archivos, documento largo). [DOC]
- Se requiere salida tipada y auditable por unidad antes de integrar. [DOC]
- NO activar cuando la tarea cabe holgadamente y el overhead de coordinación supera el beneficio. [DOC]

## Skills relacionadas

- `katas-subagents-parallel`
- `katas-context-budget`
- `katas-provenance-preservation`
