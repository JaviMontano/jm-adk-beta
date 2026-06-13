# self-correction-loops

## Que hace

Construye un bucle de **verificacion cruzada declarado-vs-calculado** para campos
numericos agregados (totales, subtotales, balances, conteos). Recomputa cada
agregado de forma **independiente** desde los datos crudos, compara contra el valor
declarado por la fuente con un `epsilon` justificado por tipo de dato, y cuando la
diferencia supera la tolerancia emite `mismatch=true` con `declared`, `computed` y
`delta` (con signo) y escala a un humano. Invariante dura: **nunca corregir un
numero en silencio** [DOC].

## Cuando usarla

- Llega un agregado numerico **y** tienes los componentes para recalcularlo
  (suma de lineas, balance = debe - haber, conteo de items) [DOC].
- El costo de un numero silenciosamente equivocado es alto: finanzas, facturacion,
  inventario, reporting regulatorio [DOC].
- Necesitas rastro de auditoria: cada total debe poder mostrar declarado vs calculado.

## Cuando NO usarla

- Sin recomputo independiente (agregado huerfano) -> degrada a `[POR_CONFIRMAR]`
  humano; ver `validation-retry-design` para formato/parsing.
- Peticion de "corregir los numeros para que cuadren" -> se rechaza, no se ejecuta.
- Input vacio o tarea no numerica.

## Como ejecuta (routing)

1. **lead** identifica los campos verificables y abre el bucle (ver `agents/lead.md`).
2. **specialist** justifica el `epsilon` por tipo de dato y define la formula de
   recomputo (ver `agents/specialist.md` y `assets/epsilon-policy.json`).
3. **support** recomputa desde crudos y arma el registro tipado por campo
   (ver `agents/support.md` y `templates/output.md`).
4. **guardian** corre los gates: recomputo independiente, mismatch escalado sin
   sobreescritura, contrato JSON, test estructural (ver `agents/guardian.md`).

## Referencias

- `SKILL.md` — contrato completo, patron correcto, anti-patrones, checklist.
- `knowledge/body-of-knowledge.md` — conceptos, reglas de decision, taxonomia de evidencia.
- `knowledge/knowledge-graph.json` — grafo de los conceptos clave.
- `prompts/` — prompt primario, meta y variaciones quick/deep.
- `templates/output.md` — scaffold del reporte de verificacion.
- `examples/` — ejemplo trabajado (input -> output) con mismatch escalado.
- `assets/` — politicas y contrato JSON que rigen tolerancias, mismatch y escalada.

## Evidencia

Cada afirmacion lleva tag: `[CODE]` `[CONFIG]` `[DOC]` `[INFERENCIA]` `[SUPUESTO]`.
Sin precios. Single-brand (JM Labs). Sin PII de cliente.
