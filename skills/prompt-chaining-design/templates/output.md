# Diseño de cadena de pases — <nombre de la tarea>

## 1. Contexto y decisión chaining vs single-pass

- **Tarea**: <qué hay que procesar y producir>
- **Volumen del lote**: <conteo aproximado de unidades>
- **Decisión**: [ ] chaining  [ ] single-pass
- **Justificación**: <volumen alto | paralelismo real | aislamiento de fallos>. Si
  single-pass: por qué cabe holgado y razona mejor completo. [INFERENCIA]

## 2. Unidad atómica

- **Una unidad es**: <archivo | commit | ticket | registro | PR>
- **Independencia**: <confirmada | dependencia detectada → rediseño> [SUPUESTO]
- **Enumeración**: <cómo se listan las unidades>

## 3. Schema del pase local

| Campo | Tipo | Obligatorio | Notas |
|-------|------|-------------|-------|
| `unit_id` | str | sí | trazabilidad |
| `status` | `ok` \| `error` | sí | estado por unidad |
| `error_detail` | str \| null | si error | detalle del fallo tipado |
| `<campo_resumen>` | <tipo> | <sí/no> | consumido por el pase 2 |

Modos de fallo cubiertos por `status="error"`: <parseo | vacío | formato | ...>. [DOC]

## 4. Schema de transición

- **Contrato**: `list[UnitSummary]` — colección tipada de resúmenes.
- **Invariante**: los datos crudos NO viajan al pase 2. [DOC]

## 5. Pase local (map)

- Procesa una unidad por invocación, idempotente, paralelizable.
- El fallo se devuelve como dato (`status="error"`), nunca como excepción global.

## 6. Pase de integración (reduce)

- Lee solo la colección de resúmenes.
- Separa `ok` / `error`; sintetiza sobre `ok`; reporta `error` sin abortar.
- Tolerancia de fallos: <cuántos `error` invalidan la síntesis>.

## 7. Resultado de gates (Guardian)

| Gate | Veredicto | Evidencia |
|------|-----------|-----------|
| Pase 2 sin crudos | pass/block | [CÓDIGO]/[DOC] |
| Schema por pase | pass/block | |
| Error tipado por unidad | pass/block | |
| Pase local de una unidad | pass/block | |
| Schema de transición presente | pass/block | |
| Chaining justificado vs single-pass | pass/block | |

Cualquier `block` se corrige antes de entregar. No marcar completo con un gate en rojo.

## 8. Anexo de costo (opcional, modo deep)

- Costo chaining estimado: <lineal por unidad + reduce acotado>
- Costo mega-prompt estimado: <cuadrático por concatenación>
