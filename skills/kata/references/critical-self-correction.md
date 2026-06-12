<!-- distilled from alfa skills/katas-critical-self-correction -->
<!-- Evaluacion critica: cross-check numerico declarado vs calculado, mismatch flag con ambos valores, sin corregir en silencio. -->
# Kata 15 · Evaluación Crítica y Auto-Corrección

## Qué es

Cuando el modelo extrae números (totales, sumas, fechas calculadas), debe cruzar lo calculado versus lo que la fuente declara. Si discrepan más allá de un epsilon, no decide arbitrariamente: emite un flag de conflicto con ambos valores y enruta a revisión humana. Escenarios típicos: Customer Support y Structured Extraction.

## Por qué importa (falla que evita)

Un total de factura calculado por el modelo puede coincidir con el declarado, o no. Sin verificación cruzada, el sistema confía silenciosamente en la alucinación más plausible. En facturación, contabilidad o impuestos, eso es un incidente operacional, no un detalle estético.

## Modelo mental

- Dos fuentes de verdad: lo declarado en el documento (`stated`) y lo calculado por el agente (`computed`).
- Ambas deben coincidir dentro de un epsilon de tolerancia.
- Si difieren, marcar `mismatch=true` con ambos valores y el delta. Nunca "elegir el más razonable".
- Aplica a totales numéricos, sumas, conteos y fechas derivadas.
- Un `mismatch` escala vía Kata 16 (handoff humano); el origen del dato se preserva vía Kata 20 (provenance).
- El `computed` se deriva SIEMPRE de datos crudos de líneas, nunca de otro campo ya agregado por el modelo (eso sería comparar una alucinación contra sí misma).

## Supuestos y anti-scope

- **Supuesto**: el documento expone líneas atomizables (`doc.lines`) y un total declarado extraíble. Si no hay líneas recalculables, este kata no aplica: no se puede cross-check y se documenta como `computed=null, reason="not_recomputable"`.
- **Anti-scope**: este kata NO corrige, NO redondea para "cuadrar", NO decide cuál valor es correcto. Solo detecta y enruta. La corrección es decisión humana (Kata 16).
- **Anti-scope**: no valida la *semántica* del número (si el IVA es legal), solo su *consistencia* aritmética declarado-vs-calculado.

## Patrón correcto

```python
stated = extract_stated_total(doc)
computed = sum(line.amount for line in doc.lines)
if abs(stated - computed) > epsilon:
    return {
        "stated_total": stated,
        "computed_total": computed,
        "mismatch": True,
        "delta": stated - computed,
        "needs_human_review": True,
    }
```

## Anti-patrón

```python
# Confía ciegamente en lo declarado, sin recalcular:
total = extract_total(doc)

# O peor: corrige en silencio y oculta la discrepancia:
if abs(stated - computed) > epsilon:
    total = computed  # corrige silenciosamente
```

## Cómo elegir epsilon (decisión + trade-off)

| Tipo de dato | Epsilon | Justificación |
|---|---|---|
| Conteos / enteros | `0` (igualdad exacta) | No hay redondeo posible; cualquier delta es un error real. |
| Moneda (mismo símbolo) | `0.01` × nº de líneas | Absorbe redondeo de centavos acumulado por línea, sin esconder errores de magnitud. |
| Fechas derivadas | `0` (igualdad de fecha) | Una fecha calculada o coincide o es un bug de cálculo de calendario. |
| Porcentajes / tasas | `1e-6` relativo | Tolera error de punto flotante, no error de tasa. |

Trade-off: un epsilon demasiado amplio convierte mismatches reales en falsos negativos (el incidente pasa silencioso, justo lo que el kata evita); demasiado estrecho inunda al humano con ruido de redondeo y erosiona la confianza en el flag. Epsilon fijo absoluto en moneda es frágil cuando el nº de líneas varía: por eso se escala con el conteo de líneas.

## Edge cases y failure modes

- **`stated` ausente**: no hay con qué comparar. No asumir que `computed` es correcto; marcar `mismatch=true, reason="stated_missing"` y escalar.
- **Líneas vacías o `doc.lines == []`**: `computed=0`. Si `stated != 0`, es mismatch legítimo, no un caso a silenciar.
- **Monedas mixtas en las líneas**: sumar montos de distintas divisas es un bug; detectar y escalar como `reason="currency_mismatch"` antes de comparar.
- **Signos (créditos/descuentos negativos)**: incluir el signo en la suma; un descuento omitido produce un mismatch que el kata debe exponer, no enmascarar.
- **NaN / no parseable**: si una línea no parsea a número, `computed=null`, escalar; nunca tratar el fallo de parseo como cero.
- **Doble verificación contra sí misma**: si `computed` se calcula desde un campo ya emitido por el modelo, el cross-check es nulo. Falla de diseño, no de runtime.

## Argumento de certificación

- Identificar los campos numéricos sujetos a verificación cruzada.
- Definir el epsilon de tolerancia (ver tabla) y justificarlo por tipo de dato.
- Probar que el `computed` se deriva de datos crudos, no de un agregado del propio modelo.
- Conectar con Kata 16 (escalada humana) y Kata 20 (provenance).

## Criterios de aceptación

- [ ] Todo total/suma/conteo/fecha derivada tiene un `computed` recalculado desde líneas crudas.
- [ ] El output incluye `stated`, `computed` y `delta` cuando hay mismatch (no solo un booleano).
- [ ] Ningún path corrige, redondea ni elige valor en silencio.
- [ ] El epsilon está declarado, justificado por tipo de dato y escala con el nº de líneas en moneda.
- [ ] `stated` ausente, líneas vacías y parseo fallido producen escalada, no un falso "OK".
- [ ] Todo mismatch enruta a Kata 16; el origen se preserva vía Kata 20.

## Cuándo activar

- Cuando el modelo extrae o calcula totales, sumas, conteos o fechas derivadas a partir de un documento.
- En pipelines de facturación, contabilidad, impuestos o cualquier extracción donde un número incorrecto sea un incidente.
- Cuando una fuente declara un total y el agente puede recalcularlo a partir de sus líneas.

## Skills relacionadas

- `katas-human-handoff-protocol`
- `katas-provenance-preservation`
- `katas-validation-retry-feedback`
- `katas-confidence-stratified-sampling`
