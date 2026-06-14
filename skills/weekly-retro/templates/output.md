# Retro semanal — {VENTANA: AAAA-MM-DD a AAAA-MM-DD}

> Cadencia P12 · operador · marca unica: {WORKSPACE}

## Fuentes leidas
- {tasklog/TAREAS.md · ancla} — {tag}
- {changelog · ancla} — {tag}
- {hilo/commit · ref} — {tag}

(Si ninguna fuente fue leible: `{VACIO_CRITICO}` — detente y pide la fuente.)

## Ayudo
- {Acierto 1: que practica/decision aceleró el trabajo} — {fuente} {tag}
- {Acierto 2} — {fuente} {tag}

## Friccion
- {Friccion 1: que costó tiempo/retrabajo} — ocurrencias: {n} — {fuente} {tag}
- {Friccion 2} — ocurrencias: {n} — {fuente} {tag}

## Regla candidata (P12)
- **Regla:** {imperativo, una linea} — destino: `{ruta/memoria.md}` — basada en
  friccion vista {n}>=2 veces — {tag}
- (Si no hubo regla) **Sin patron nuevo esta semana.** Justificacion:
  {por que ninguna friccion alcanzó el umbral} {tag}

### Diff propuesto (esperar confirmacion antes de aplicar)
```diff
# archivo: {ruta/memoria.md}
+ {linea de la regla en imperativo}
```
Estado: { pendiente de confirmacion | confirmado y aplicado (append) | rechazado }

## Acciones — proxima semana
1. {Accion concreta} — primer paso: {paso ejecutable} {tag}
2. {Accion concreta} — primer paso: {paso ejecutable} {tag}

## Observaciones (no promovidas)
- {Friccion vista 1 vez, en watch para la proxima ventana} {tag}

## Gate de validacion
- [ ] evidence — un tag Jarvis por claim; familia unica; `{WEB}` con cita
- [ ] quality_criteria — >=1 accion; regla cumple umbral o justificacion de "sin regla"
- [ ] upgrade_safety — diff mostrado + confirmacion; append; sin `--force`

Veredicto guardian: { pass | conditional | fail | not-verified }
