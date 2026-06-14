# Checklist operativa — self-correction-loops

Gate de aceptacion del bucle de verificacion cruzada. PASA solo si TODOS marcan.

- [ ] Campos numericos verificables identificados, cada uno con recomputo
      **independiente** desde los datos crudos.
- [ ] `epsilon` justificado por tipo de dato: 0 para enteros, tolerancia pequena
      documentada para moneda/float (segun `epsilon-policy.json`).
- [ ] El `computed` se deriva de componentes crudos, no del agregado declarado.
- [ ] `delta = declared - computed` con signo conservado en el registro.
- [ ] Comparador estricto: `mismatch = abs(delta) > epsilon`.
- [ ] Ante mismatch: `declared` y `computed` ambos visibles, `action=escalate_to_human`.
- [ ] El campo declarado NO se sobreescribe en ningun caso.
- [ ] Agregados sin recomputo posible degradados a `unverifiable` / revision humana,
      no a un calculado inventado.
- [ ] Test estructural: caso con mismatch inyectado produce el flag; jamas
      `total=computed` silencioso.
- [ ] Reporte conforme a `self-correction-loops-contract.json`; `scripts/check.sh`
      pasa fixtures positivas y negativas.

Evidencia por item: `[CODE]` `[CONFIG]` `[DOC]` `[INFERENCIA]`. Sin precios.
