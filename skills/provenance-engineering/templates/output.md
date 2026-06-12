# Diseno de pipeline con provenance tipada — <entidad/encargo>

## 1. Contexto resuelto

- **Consumidor / auditor**: <quien>
- **Consecuencia de decision**: <que se firma/cita/decide con estos datos>
- **Inventario de fuentes**:

| source_id | documento | version | as_of |
|-----------|-----------|---------|-------|
| <id>      | <doc>     | <ver>   | <fecha> |

- **Atributos y locators**:

| atributo | source_id | locator (pagina/celda/span) |
|----------|-----------|------------------------------|
| <attr>   | <id>      | <locator>                    |

> Vacio critico: <ninguno | lista de inventario/locator faltante -> bloqueado>

## 2. Modelo del Claim

- `Claim(value, source[], as_of, conflict)`; `source[]` vacio invalido por construccion. [CÓDIGO]
- Regla de normalizacion previa a comparacion: <trim/casing/fecha/moneda>. [INFERENCIA]

## 3. Claims emitidos

| atributo | value | source_id(s) | as_of | conflict |
|----------|-------|--------------|-------|----------|
| <attr>   | <val> | <id1[,id2]>  | <fecha> | true/false |

## 4. Cola de escalacion (conflictos)

| atributo | valor fuente A (source_id, as_of) | valor fuente B (source_id, as_of) | estado |
|----------|-----------------------------------|-----------------------------------|--------|
| <attr>   | <valA> (<id>, <fecha>)            | <valB> (<id>, <fecha>)            | pendiente humano |

## 5. Render auditable

<descripcion del render: source_id + as_of + marcador de conflicto junto a cada dato>

## 6. Test estructural (CI)

<resumen del test: falla ante claim sin source, source_id desconocido, conflicto silenciado>

## 7. Gate de aceptacion

- [ ] Cada claim con `source[]` no vacio (id + locator + fecha)
- [ ] Cada `source_id` en el inventario
- [ ] Conflictos `conflict=true` conservando todas las fuentes
- [ ] Conflictos escalados a humano, no resueltos/promediados
- [ ] `as_of` visible en el render
- [ ] Test estructural presente en CI
- [ ] Sin valor agregado que ninguna fuente afirme

> Evidencia: cada fila no obvia con su tag Alfa-core; cada `[SUPUESTO]` con verificacion. Sin precios inventados, sin PII, brand unico.
