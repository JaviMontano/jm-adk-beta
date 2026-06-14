# Example Output — pristino-calibration

Response that honors the block in `examples/example-input.md`.

---

Arquitecto de Software

## 1) Pedido original
Diseña una arquitectura de ingesta de eventos para un catálogo de productos.
Tiene que tolerar picos y no perder mensajes. No tengo todavía las cifras de
volumen.

## 2) Prompt optimizado
- **Objetivo:** arquitectura de ingesta de eventos para catálogo de productos,
  tolerante a picos y sin pérdida de mensajes.
- **Contexto:** dominio de catálogo; eventos de alta/baja/actualización de
  producto. [ASSUMPTION → asumo eventos de mutación de catálogo, no telemetría].
- **Restricciones:** tolerancia a picos (back-pressure), entrega sin pérdida
  (at-least-once + idempotencia).
- **Faltantes / VACIO_CRITICO:** volumen pico (eventos/seg) y regiones — sin
  cifras no se dimensiona el buffer. [ASSUMPTION → MVP single-region, ~1k ev/s].
- **Definition of Done:** diagrama de componentes + decisiones clave + riesgos.
- **Forma de salida + clamp:** Canvas, ≤ 1 pantalla.
- **Anti-drift:** Incluye topología de ingesta y garantías de entrega. NO incluye
  pricing, IaC, ni el esquema de datos del catálogo.

## 3) Respuesta — Canvas output contract
- **Resumen:** ingesta basada en un log de eventos particionado con consumidores
  idempotentes y una cola de mensajes muertos (DLQ); el desacople absorbe picos
  sin perder mensajes.
- **Evidencia:** at-least-once + idempotencia es el patrón estándar para "sin
  pérdida" sin exactly-once costoso [DOC]; el dimensionamiento real depende del
  volumen pico aún no provisto [ASSUMPTION].
- **Decisiones y criterios:** log particionado (no cola simple) para escalar por
  partición; DLQ para no bloquear el flujo ante mensajes envenenados.
- **Opciones:**
  | Opción | Impacto | Esfuerzo | Riesgo |
  |--------|---------|----------|--------|
  | Log particionado + idempotencia | Alto (escala + sin pérdida) | Medio | Bajo |
  | Cola simple + reintentos | Medio | Bajo | Medio (sin orden por clave) |
  - **Recomendación:** log particionado + consumidores idempotentes; mejor relación
    garantías/esfuerzo para el objetivo declarado.
- **Plan con DoD:** (1) confirmar volumen pico → done: cifra registrada;
  (2) definir clave de partición → done: orden por producto garantizado;
  (3) diseñar DLQ + alertas → done: runbook de reproceso.
- **Riesgos / límites / validación:** dimensionamiento sin volumen es provisional;
  validar throughput con una prueba de carga antes de fijar particiones.
- **Estado:** degraded · **Confianza:** 0.6

---

**Why this passes the gate:** persona_line present; full+substantive shape with
the three sections + Canvas; one tag family (Alfa core); the missing volume is a
`VACIO_CRITICO` handled with `[ASSUMPTION]` + a verification step (no fabrication);
delegations stay within `capability_agents`; `estado` is `degraded` (not a false
`success`) because the volume figure is unverified.
