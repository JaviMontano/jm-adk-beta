# Example Input — pristino-calibration

A `full + substantive` request where the `persona-calibrate.sh` hook fired and
injected a block. The persona is `Arquitecto de Software`, the optimizer is on,
and one input (peak throughput) is missing — so the optimizer must surface a
`VACIO_CRITICO` and proceed with a tagged assumption rather than fabricate it.

## Injected block (additionalContext)

```
PRISTINO-CALIBRATION:
PERSONA: Arquitecto de Software
PERSONA-ID: arquitecto-software
CONFIDENCE: 0.86
MODE: full
COMPLEXITY: substantive
DELEGATE: revisor-arquitectura, analista-no-funcionales
OPTIMIZER: true
```

## User prompt

> Diseña una arquitectura de ingesta de eventos para un catálogo de productos.
> Tiene que tolerar picos y no perder mensajes. No tengo todavía las cifras de
> volumen.

## Expected handling

- Line 1 must be `Arquitecto de Software`.
- Run all three optimizer sections + Canvas.
- "Tolerar picos / no perder mensajes" are real constraints; peak throughput is a
  missing figure → surface it as a `VACIO_CRITICO`, assume an MVP single-region
  baseline tagged `[ASSUMPTION]`, and add the verification step.
- Delegations limited to `revisor-arquitectura` and `analista-no-funcionales`
  (both in the persona's `capability_agents`); inventing any other agent is
  blocked.
- `estado` cannot be `success` while the volume figure is unverified → `degraded`.
