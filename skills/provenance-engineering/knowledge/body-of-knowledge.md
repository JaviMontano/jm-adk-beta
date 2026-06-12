# Body of Knowledge — Provenance Engineering

Conocimiento de dominio para disenar pipelines de extraccion/sintesis con provenance tipada. [DOC]

## 1. Conceptos clave

- **Claim** — afirmacion tipada con `value`, `source[]` no vacio y `as_of`. Es la unidad atomica del output; no existe un claim valido sin source. [CÓDIGO]
- **Source** — origen tipado de un valor: `source_id`, `locator` (pagina/celda/span), `as_of` (fecha del documento). [DOC]
- **Inventario de fuentes** — conjunto cerrado de `source_id` declarados. Todo `source_id` en un claim debe pertenecer a el. [DOC]
- **Locator** — direccion precisa del dato dentro de la fuente; permite que un humano vuelva al origen exacto. [DOC]
- **Conflicto** — dos o mas fuentes afirman valores distintos (tras normalizacion) para el mismo atributo. Se representa con `conflict=true` conservando todas las fuentes. [CÓDIGO]
- **Escalacion** — enrutar un conflicto a revision humana con ambas fuentes y fecha visibles; el pipeline no resuelve. [DOC]
- **Invariante estructural** — "no hay claim sin source" garantizada por tipo + test, no por convencion. [INFERENCIA]
- **Resolucion silenciosa** — colapsar un desacuerdo a un valor unico (promedio, primera, mas reciente) sin rastro; el anti-objetivo central. [DOC]

## 2. Estandar de provenance (campos obligatorios)

Por cada claim emitido: [DOC]

| Campo | Obligatorio | Regla |
|-------|-------------|-------|
| `value` | si | valor normalizado |
| `source[]` | si, no vacio | sin placeholders; ids reales del inventario |
| `source_id` | si | debe existir en el inventario |
| `locator` | si | pagina/celda/span concreto |
| `as_of` | si | fecha del documento; ausencia = vacio critico, no `None` |
| `conflict` | si (bool) | `true` cuando >1 valor normalizado distinto |

## 3. Reglas de decision

1. **Comparar normalizado, no crudo.** Normaliza (trim, casing, formato fecha/moneda) **antes** de decidir conflicto. Diferencia solo de formato no es conflicto. [INFERENCIA]
2. **Conservar, no elegir.** Ante valores distintos, conserva todas las fuentes con `conflict=true`; nunca elijas una en silencio. [CÓDIGO]
3. **Escalar, no resolver.** Ningun conflicto se resuelve automaticamente; va a cola humana. "Mas reciente gana" es resolucion silenciosa disfrazada. [DOC]
4. **Invariante por construccion Y por test.** El tipo previene `source[]` vacio; el test cubre el output serializado contra ids desconocidos y conflictos silenciados. Se usan ambos. [INFERENCIA]
5. **Falla duro ante id desconocido.** Un `source_id` fuera del inventario es indistinguible de un claim fabricado. [DOC]
6. **Hazlo visible.** `as_of` y marcador de conflicto junto a cada dato en el render; un auditor debe verlos sin excavar. [DOC]

## 4. Trade-offs documentados

- **Conservar ambas fuentes vs elegir una** — conservar cuesta verbosidad; elegir destruye auditabilidad de forma irreversible. Se prioriza auditabilidad. [INFERENCIA]
- **Escalar vs heuristica** — la heuristica parece eficiente pero produce un valor que ninguna fuente afirma. Se escala siempre. [INFERENCIA]
- **Tipo vs test** — el test atrapa regresiones; el tipo las previene. Se combinan. [INFERENCIA]

## 5. Anti-scope

No aplica cuando el output es prosa exploratoria sin consecuencia de decision, o cuando una sola fuente de verdad es indiscutible sin posibilidad de conflicto. Forzar provenance ahi anade ceremonia sin valor de auditoria. [DOC]

## 6. Taxonomia de evidencia

Cada claim no obvio lleva exactamente un tag Alfa-core: `[DOC]`, `[CÓDIGO]`, `[CONFIG]`, `[INFERENCIA]`, `[SUPUESTO]`. `[CÓDIGO]` solo si el patron existe en el archivo. Cada `[SUPUESTO]` se empareja con un paso de verificacion. Sin mezcla de familias de tags. Sin precios inventados; sin PII de cliente; brand unico. [DOC]
