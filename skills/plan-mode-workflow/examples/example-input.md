# Ejemplo — Entrada (plan-mode-workflow)

## Escenario

Un agente debe modificar por primera vez un **repo de pagos desconocido**
(`payments-core`) para añadir un campo de idempotencia al endpoint de captura. El
repo tiene trabajo no commiteado de otro dev en el mismo módulo y la organización
exige aprobación auditable antes de mutar archivos en producción.

## Petición del usuario

> Vamos a tocar `payments-core` por primera vez. Es un repo de pagos en producción
> y hay cambios sin commitear de otro compañero en `capture/`. Diseña un gate de
> dos modos: explora en read-only, dame un `plan.md` firmable, y bloquea cualquier
> escritura por hook hasta que yo firme el hash exacto. La aprobación tiene que
> quedar como evento auditable (hash, aprobador, timestamp), y si el plan cambia
> después de firmado, que vuelva a pedir firma.

## Contexto disponible

- **Repo objetivo:** `payments-core`
- **Aprobador:** `lead-pagos@jmlabs`
- **Blast radius:** alto (producción, módulo `capture/` con trabajo ajeno sin commitear)
- **Objetivo del cambio:** añadir campo de idempotencia al endpoint de captura

## Resultado esperado

El contrato del gate de dos modos: estado de modo, write-blocklist fail-closed,
`plan.md`, evento de firma por hash, hook `PreToolUse` y checklist de aceptación
—con la lógica de re-firma ante cambios del plan.
