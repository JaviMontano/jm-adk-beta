# Body of Knowledge — self-correction-loops

Conocimiento de dominio para construir bucles de verificacion cruzada
declarado-vs-calculado sobre campos numericos agregados.

## 1. Conceptos clave

- **Declarado (`declared`)**: el valor que la fuente afirma (el `total` de la
  factura, el balance de la cuenta, el conteo del reporte). Es entrada, no verdad.
- **Calculado (`computed`)**: el valor que recomputas de forma **independiente**
  desde los componentes crudos (suma de lineas, debe - haber, conteo real).
- **Recomputo independiente**: el calculado se deriva de datos mas primitivos que
  el agregado, nunca del agregado mismo. Reusar el declarado convierte el check en
  un no-op que siempre pasa.
- **Epsilon (`epsilon`)**: tolerancia maxima admisible de la diferencia, justificada
  por tipo de dato. No es un parametro libre; un epsilon arbitrario oculta errores.
- **Delta (`delta`)**: `declared - computed`, con signo conservado. El signo indica
  sobre-declaracion (positivo) o sub-declaracion (negativo).
- **Mismatch flag (`mismatch`)**: `abs(delta) > epsilon`. Comparador estricto.
- **Escalada (`escalate_to_human`)**: ante mismatch, la decision pertenece a una
  persona; el sistema adjunta el flag y deriva, no corrige.
- **Agregado huerfano (`unverifiable`)**: agregado sin componentes para recomputar;
  se degrada a revision humana, no se inventa un calculado.

## 2. Estandares y politicas (assets)

- `self-correction-loops-contract.json`: campos obligatorios del reporte
  (`field`, `declared`, `computed`, `delta`, `mismatch`).
- `epsilon-policy.json`: tolerancias permitidas por `data_type`
  (entero=0, moneda=0.005, float=1e-6) [CONFIG].
- `mismatch-policy.json`: obliga a mostrar `declared` y `computed` ambos visibles.
- `escalation-policy.json`: obliga a escalar sin sobreescribir el declarado.
- `structural-test-policy.json`: pruebas estructurales que deben quedar en `true`.

## 3. Reglas de decision

1. **Dos condiciones para activar**: declarado disponible **y** recomputo
   independiente posible. Si falta cualquiera, el bucle no aplica.
2. **Epsilon por tipo**: cero para enteros; tolerancia documentada para moneda y
   float. Un epsilon de moneda sobre un entero es un defecto.
3. **Comparador estricto `>`**: `delta == epsilon` cuenta como match; asi `epsilon=0`
   marca solo diferencias reales y no el caso `delta==0`.
4. **Signo conservado en `delta`**: usar `abs()` solo para el comparador del flag,
   nunca para el registro de auditoria.
5. **Mismatch = senal, no defecto**: jamas mutar el campo declarado; escalar.
6. **Huerfano = degradar**: marcar `unverifiable`, no fabricar un calculado.

## 4. Anti-patrones (a bloquear)

- **ANTI 1 — Correccion silenciosa**: `invoice["total"] = computed`. Oculta el
  conflicto y propaga un dato falso con apariencia de validado.
- **ANTI 2 — Recomputo no-independiente**: `computed = invoice["total"]`. El check
  nunca puede fallar; falsa sensacion de control.
- **ANTI 3 — Epsilon arbitrario**: tolerancia sin justificacion que enmascara
  errores reales bajo la etiqueta "redondeo".

## 5. Fronteras (anti-scope)

- Validacion de formato/parsing (JSON valido, campo presente, tipo correcto) ->
  `validation-retry-design`, no este skill.
- A donde va el mismatch (canal, SLA de revision) -> `human-escalation-design`.
- Rastro de procedencia del declarado -> `provenance-engineering`.
- No expandir a retry, orquestacion ni formato: skills hermanas.

## 6. Taxonomia de evidencia

Toda afirmacion lleva tag: `[CODE]` (en codigo del bucle), `[CONFIG]` (en assets
de politica), `[DOC]` (en SKILL.md / contrato), `[INFERENCIA]` (deduccion del
diseno), `[SUPUESTO]` (asuncion no verificada). Sin precios. Single-brand JM Labs.
