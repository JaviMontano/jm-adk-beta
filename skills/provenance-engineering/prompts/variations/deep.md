# Prompt — Variation: Deep

Diseno completo de un pipeline de provenance multi-fuente con escalacion y test estructural en CI. Usa el flujo lead -> specialist -> support -> guardian.

## Fase 0 — Contexto (lead)

Resuelve y, si falta algo, **detente y pide**:
- Inventario de fuentes: cada `source_id` con documento, version, `as_of`.
- Atributos a extraer y, por atributo, el `locator` en cada fuente.
- Consumidor que audita y consecuencia de decision (que se firma/cita).
Confirma scope: hay consecuencia de decision y posibilidad de conflicto (si no, anti-scope, declina).

## Fase 1 — Diseno de dominio (specialist)

- Tipo `Claim` (`value`, `source[]` no vacio, `as_of`), invalido por construccion si `source[]` vacio.
- `Source` con `source_id`, `locator`, `as_of`.
- Regla de normalizacion previa (trim/casing/fecha/moneda).
- Criterio conflicto vs diferencia de formato.

## Fase 2 — Ejecucion (support)

- Captura de provenance en extraccion.
- Consolidacion con `conflict=true` conservando todas las fuentes.
- Cola de escalacion humana (ambas fuentes + fecha).
- Render auditable (`source_id`, `as_of`, marcador de conflicto).
- Test estructural en CI (sin source / id desconocido / conflicto silenciado -> falla el build).

## Fase 3 — Validacion (guardian)

Aplica los siete gates de `agents/guardian.md`. PASS solo si todos pasan; FAIL con gate + span + fix minimo. Nunca trates green como prueba.

## Salida

Pipeline diseñado por fases + el gate de aceptacion de `SKILL.md` resuelto casilla por casilla, cada decision con su tag Alfa-core, cada `[SUPUESTO]` con verificacion. Sin resolucion silenciosa, sin precios inventados, sin PII, brand unico.
