# Ejemplo — Output

## 1. Contexto resuelto

- **Consumidor / auditor**: analista de cumplimiento. [DOC]
- **Consecuencia de decision**: firma de apertura de cuenta. [DOC]
- **Inventario**: `coi-2024`, `aoa-2023`, `util-2025` (todos con `as_of`). Sin vacios criticos: cada atributo tiene locator. [DOC]

## 2. Modelo del Claim

`Claim(attribute, value, sources[], as_of, conflict)`; `sources[]` vacio invalido por construccion (`__post_init__` lanza si vacio). Normalizacion previa a comparar: trim + casing para nombres; ISO-8601 para fechas. [CÓDIGO]

## 3. Claims emitidos

| atributo | value | source_id(s) | as_of | conflict |
|----------|-------|--------------|-------|----------|
| `legal_name` | Acme Holdings Ltd. | `coi-2024`, `aoa-2023` | 2024-03-02 / 2023-11-18 | **false** |
| `incorporation_date` | 2024-03-02 | `coi-2024` | 2024-03-02 | false |
| `registered_address` | 12 King St, London \| 48 Queen Rd, London | `aoa-2023`, `util-2025` | 2023-11-18 / 2025-01-09 | **true** |

- `legal_name`: "Acme Holdings Ltd." vs "ACME HOLDINGS LTD" -> tras normalizar (casing/puntuacion) son el **mismo valor**; no es conflicto, se consolida conservando ambas fuentes como respaldo. [INFERENCIA]
- `registered_address`: tras normalizar siguen distintas -> `conflict=true`, **ambas** fuentes conservadas, ningun valor inventado. [CÓDIGO]
- `incorporation_date`: fuente unica, claim valido con `sources[]` de un elemento; no se fuerza conflicto. [INFERENCIA]

## 4. Cola de escalacion (conflictos)

| atributo | fuente A | fuente B | estado |
|----------|----------|----------|--------|
| `registered_address` | "12 King St, London" (`aoa-2023`, 2023-11-18) | "48 Queen Rd, London" (`util-2025`, 2025-01-09) | **pendiente humano** |

El pipeline **no** elige "la mas reciente" (`util-2025`): eso seria resolucion silenciosa. El analista decide con ambas fechas a la vista. [DOC]

## 5. Render auditable

Cada dato se muestra con `source_id` y `as_of`; `registered_address` aparece marcado con badge de conflicto enlazando a la cola de escalacion. [DOC]

## 6. Test estructural (CI)

`assert_provenance(claims, known_ids={"coi-2024","aoa-2023","util-2025"})` falla el build si: un claim queda con `sources[]` vacio, aparece un `source_id` fuera del inventario, o un conflicto fue colapsado a un valor unico. [CÓDIGO]

## 7. Gate de aceptacion

- [x] Cada claim con `source[]` no vacio (id + locator + fecha)
- [x] Cada `source_id` en el inventario
- [x] Conflicto (`registered_address`) marcado conservando ambas fuentes
- [x] Conflicto escalado a humano, no promediado ni resuelto
- [x] `as_of` visible en el render
- [x] Test estructural presente en CI
- [x] Sin valor agregado que ninguna fuente afirme

> Verdicto guardian: **PASS** — los siete gates pasan con la evidencia anterior; green del CI no se trato como prueba, se verificaron los criterios. [DOC]
