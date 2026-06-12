<!-- distilled from alfa skills/folio-generator -->
<!-- > -->
# Folio Generator

> "Un documento sin numero es un documento perdido." — Principio de archivo

## TL;DR

Genera documentos numerados automaticamente con formato `{PREFIX}-{YYYY}-{NNN}`. Soporta cotizaciones (COT), memos (MEM), facturas (FAC), minutas (MIN), y tipos personalizados. Cada folio tiene numero unico, fecha, y contenido formateado. El numero es la unica fuente de verdad: se reserva via script atomico, nunca a mano. [EXPLICIT]

## Scope & Anti-Scope

- IN: reservar el siguiente correlativo, renderizar folio HTML/markdown, registrar en tracker, distribuir (Docs/Drive/Gmail) bajo confirmacion. [DOC]
- OUT — enrutar a otra skill: contabilidad/impuestos de una factura, firma electronica, generacion de PDF firmado, plantillas legales de un contrato. El folio solo numera y maqueta. [INFERENCIA]
- OUT: reasignar o reciclar numeros ya emitidos. Un correlativo gastado nunca se reutiliza, ni siquiera tras cancelar el documento — se marca anulado, no se borra. [SUPUESTO]

## When to Activate

| Signal | Example |
|--------|---------|
| Folio explicito | "Genera el folio para esta cotizacion" |
| Cotizacion | "Crea cotizacion COT-2026-001 para el cliente" |
| Documento numerado | "Necesito un memo numerado" |
| Factura | "Genera la factura FAC-2026-015" |

## S1 — Determinar Tipo y Numero

1. Identificar tipo de documento:
   - `COT` — Cotizacion / Presupuesto
   - `MEM` — Memorandum
   - `FAC` — Factura
   - `MIN` — Minuta / Acta
   - `DOC` — Documento generico
2. Ejecutar `scripts/next-folio-number.sh --dry-run --tracker .folio-tracker.json PREFIX` para calcular el siguiente numero sin mutar estado.
3. Si el usuario confirma generacion/reserva, ejecutar `scripts/next-folio-number.sh --apply --tracker .folio-tracker.json PREFIX`.
4. Si el usuario especifica numero, validar que no exista duplicado antes de reservar.

**Decision — dry-run antes de apply, siempre.** El usuario ve el numero que va a quedar reservado antes de comprometerlo. Trade-off: dos invocaciones del script en vez de una; se acepta porque la alternativa (apply directo) gasta correlativos en falsos arranques y deja huecos en la secuencia. [INFERENCIA]

**Decision — el ano del folio sale del campo de fecha de emision, no del reloj del sistema al renderizar.** Trade-off: hay que pasar la fecha explicita; a cambio, regenerar un documento en enero no reabre la secuencia del ano anterior ni rompe la continuidad. [CONFIG]

**Edge cases** [INFERENCIA]:
- Cambio de ano: `NNN` reinicia en `001` para cada `{PREFIX}-{YYYY}` nuevo. El contador es por prefijo-y-ano, no global.
- Numero forzado por el usuario que crea hueco (p.ej. pide `015` con `010` como ultimo): permitido, pero registrar el salto; el script no rellena `011`-`014` automaticamente.
- Numero forzado menor o igual al ultimo emitido: es colision potencial — rechazar y pedir confirmacion explicita, nunca sobrescribir.
- Tracker inexistente o vacio: tratar como secuencia nueva, primer folio `001`; no es error.

## S2 — Generar Documento

1. Aplicar template con datos:
   - Folio ID en header
   - Fecha de emision
   - Destinatario / Cliente
   - Asunto
   - Cuerpo del documento
   - Pie con "Documento generado — Folio {ID}"
2. Usar `assets/folio-style.css` y `assets/brand-tokens.json` como fuente visual del HTML.
3. Renderizar HTML con `scripts/render-folio-html.py --data <datos.json>` cuando existan datos estructurados.
4. Generar version markdown como fallback portable cuando no se requiere HTML.

**Edge cases** [INFERENCIA]:
- Campos obligatorios ausentes (destinatario, asunto): no auto-rellenar con placeholder; pedir el dato o marcar `[SUPUESTO]` visible en el cuerpo, nunca silencioso.
- Cuerpo con HTML/markdown del usuario: escapar al renderizar para que no rompa el template ni inyecte estilos fuera de los tokens de marca.

## S3 — Registrar y Distribuir

1. Actualizar `.folio-tracker.json` solo via `scripts/next-folio-number.sh --apply` (nunca a mano).
2. Si solicitado: crear en Google Docs via `create_doc`.
3. Si solicitado: subir a Drive via `create_drive_file`.
4. Si solicitado: enviar por email via `send_gmail_message`.

**Decision — reservar el numero (`--apply`) ANTES de distribuir.** Si la distribucion falla, el folio ya existe y se reintenta el envio sin re-numerar. El orden inverso (distribuir y luego registrar) deja documentos emitidos que el tracker no conoce. Trade-off: un fallo de envio deja un numero reservado sin documento entregado; es recuperable (reintento) y preferible a un duplicado. [INFERENCIA]

## Failure Modes

| Sintoma | Causa probable | Fix |
|---|---|---|
| Dos documentos con el mismo folio | apply concurrente o edicion manual del tracker | Reconciliar contra el tracker; anular el segundo y reemitir con apply | [INFERENCIA] |
| Hueco en la secuencia | dry-run tomado como definitivo, o apply abortado a medias | Aceptar el hueco (no rellenar) o documentar el motivo | [INFERENCIA] |
| Folio reservado sin documento | distribucion fallo tras apply | Reintentar envio con el mismo numero; no re-numerar | [INFERENCIA] |
| Ano equivocado en el ID | fecha tomada del reloj, no del campo de emision | Pasar fecha de emision explicita y regenerar | [CONFIG] |
| Tracker corrupto tras grep/sed | edicion ad hoc fuera del script | Restaurar desde control de versiones; usar solo `--apply` | [CONFIG] |

## Acceptance Criteria

- [ ] Numero unico, sin duplicados, en formato `PREFIX-YYYY-NNN`. [DOC]
- [ ] `NNN` corresponde a la secuencia del `PREFIX-YYYY` correcto (reinicia por ano). [DOC]
- [ ] `--dry-run` no muta `.folio-tracker.json`; solo `--apply` escribe. [CÓDIGO]
- [ ] Tracker actualizado tras cada generacion confirmada; documento y tracker coinciden. [DOC]
- [ ] Documento renderizado con todas las secciones (header, fecha, destinatario, asunto, cuerpo, pie con folio). [DOC]
- [ ] Estilo aplicado solo desde `folio-style.css` + `brand-tokens.json`; sin colores ni fuentes fuera de los tokens. [CONFIG]
- [ ] Distribucion (Docs/Drive/Gmail) ocurre solo bajo confirmacion explicita del usuario. [INFERENCIA]

## Anti-Patterns

- Generar folios sin actualizar el tracker. [DOC]
- Permitir o forzar numeros duplicados (numero <= ultimo emitido sin confirmacion). [DOC]
- Usar formato inconsistente entre documentos. [DOC]
- Editar `.folio-tracker.json` con grep/sed o texto ad hoc. [CONFIG]
- Tomar el ano del reloj al renderizar en vez del campo de emision. [CONFIG]
- Distribuir antes de reservar el numero. [INFERENCIA]
- Reutilizar un correlativo de un documento anulado. [SUPUESTO]

## Folio Format Rules

| Prefijo | Tipo | Ejemplo |
|---------|------|---------|
| COT | Cotizacion | COT-2026-001 |
| MEM | Memorandum | MEM-2026-015 |
| FAC | Factura | FAC-2026-042 |
| MIN | Minuta | MIN-2026-003 |
| DOC | Generico | DOC-2026-100 |

Reglas: `PREFIX` en mayusculas A-Z; `YYYY` ano de 4 digitos de la fecha de emision; `NNN` correlativo de 3+ digitos con ceros a la izquierda, secuencia independiente por cada par `PREFIX-YYYY`. Prefijos personalizados se permiten si son unicos y no colisionan con los reservados. [CONFIG]

## Worked Example

Entrada: cotizacion para "Cliente X", ultimo COT-2026 registrado es `007`, fecha de emision 2026-06-11.

1. `next-folio-number.sh --dry-run ... COT` -> imprime `COT-2026-008`, tracker intacto. [CÓDIGO]
2. Usuario confirma -> `next-folio-number.sh --apply ... COT` -> reserva `008`, tracker pasa a `008`. [CÓDIGO]
3. `render-folio-html.py --data cot.json` -> HTML con header `COT-2026-008`, pie "Documento generado — Folio COT-2026-008". [INFERENCIA]
4. Usuario pide Drive -> `create_drive_file`; envio falla -> se reintenta con el mismo `COT-2026-008`, sin re-numerar. [INFERENCIA]

## Deterministic Script Contract

- Runtime script: `scripts/next-folio-number.sh`
- Rendering script: `scripts/render-folio-html.py`
- Contract check: `scripts/check.sh`
- Validation command: `python3 scripts/validate-skill-scripts.py --strict --run-checks`
- Default behavior: `--dry-run` imprime el siguiente folio sin crear ni mutar el tracker. `--apply` es la unica via de escritura. [CÓDIGO]

## Assets Contract

- Los assets visuales viven en `assets/`.
- `assets/manifest.json` lista cada asset de salida y donde se usa. [CÓDIGO]
- `assets/folio-style.css` es la hoja de estilo print-safe para folios HTML. [CÓDIGO]
- `assets/brand-tokens.json` lleva los design tokens neutros de negocio por defecto. [CÓDIGO]

## Related Skills

- `acta-formal` — actas numeradas con folio
- `invoice-generator` — facturas (puede usar folio)
- `proposal-writing` — cotizaciones con folio

## Usage

- `/folio-generator` — generar documento numerado
- "genera folio COT-2026 para la cotizacion del cliente X"
- "crea un memo numerado sobre el cambio de politica"
