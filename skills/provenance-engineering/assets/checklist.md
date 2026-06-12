# Checklist — Provenance Engineering (gate determinista)

Recorrer antes de declarar done. Cada casilla exige evidencia, no juicio optimista. Mapea 1:1 con el gate de aceptacion de `SKILL.md` y la rubrica en `assets/quality-rubric.json`.

## Vacio critico (antes de extraer)

- [ ] Inventario de fuentes presente: cada `source_id` con documento, version y `as_of`.
- [ ] Locator presente por cada atributo en cada fuente.
- [ ] Si falta inventario o locator -> bloqueado, no se invento `source_id`.

## Claim y source

- [ ] Cada claim con `source[]` no vacio (`source_id` + `locator` + `as_of`).
- [ ] `source[]` vacio invalido por construccion (no solo por convencion).
- [ ] Sin placeholders ("varias fuentes", "interno") en `source[]`.
- [ ] Cada `source_id` existe en el inventario.

## Conflicto

- [ ] Valores comparados **normalizados** (trim/casing/fecha/moneda).
- [ ] Diferencia solo de formato -> NO marcada como conflicto.
- [ ] Valores discrepantes -> `conflict=true` conservando todas las fuentes.
- [ ] Sin promedio/mediana/concat que pierda atribucion fuente-por-valor.
- [ ] Sin heuristica de resolucion ("mas reciente/mas confiable gana").

## Escalacion y visibilidad

- [ ] Cada `conflict=true` tiene item en la cola humana (ambas fuentes + fecha).
- [ ] Render expone `as_of` y marcador de conflicto junto a cada dato.

## Blindaje

- [ ] Test estructural en CI: falla ante claim sin source, `source_id` desconocido o conflicto silenciado.

## Evidencia y gobernanza

- [ ] Cada claim no obvio con un tag Alfa-core; `[CÓDIGO]` solo donde el patron existe.
- [ ] Cada `[SUPUESTO]` con verificacion.
- [ ] Sin precios inventados, sin PII de cliente, brand unico.
- [ ] Green del CI verificado contra criterios, no tratado como prueba.
