# Retro semanal — 2026-06-05 a 2026-06-11

> Cadencia P12 · operador · marca unica: JM Labs

## Fuentes leidas
- `TAREAS.md` · entrada del sprint de skills — {EXTRAIDO_HILO}
- `orchestration/changelog.md` · dos entradas sobre re-correr el validador — {MEMORIA}
- Hilo de hoy · depuracion del knowledge-graph — {EXTRAIDO_HILO}

## Ayudo
- Reusar el sibling `daily-close` como plantilla aceleró el armado del bundle de
  skills; el costo de arranque cayó a casi cero. — `TAREAS.md` {EXTRAIDO_HILO}

## Friccion
- Olvidar el flag `--skip-script-checks` y tener que re-correr el validador —
  ocurrencias: 2 (esta semana y la anterior) — changelog {MEMORIA}
- Escribir un knowledge-graph.json a mano sin validar; ~40 min de depuracion —
  ocurrencias: 1 — hilo {EXTRAIDO_HILO}

## Regla candidata (P12)
- **Regla:** Al validar un skill, correr siempre con `--skip-script-checks` salvo
  que el skill tenga `scripts/`. — destino: `orchestration/preferences-log.md` —
  basada en friccion vista 2>=2 veces — {INFERENCIA}

### Diff propuesto (esperar confirmacion antes de aplicar)
```diff
# archivo: orchestration/preferences-log.md
+ - Validacion de skills: correr `validate-skill-dod.py` con `--skip-script-checks`
+   por defecto; omitir el flag solo cuando el skill incluya `scripts/`.
```
Estado: pendiente de confirmacion

## Acciones — proxima semana
1. Terminar el gate de evals del scaffold — primer paso: correr el validador
   sobre los tres skills pendientes. {INFERENCIA}
2. Validar todo JSON antes de guardarlo — primer paso: `python3 -m json.tool`
   sobre cada knowledge-graph nuevo. {INFERENCIA}

## Observaciones (no promovidas)
- JSON a mano sin validar (1 ocurrencia) — en watch; si reaparece, asciende a
  regla la proxima ventana. {SUPUESTO}

## Gate de validacion
- [x] evidence — un tag Jarvis por claim; familia unica; sin `{WEB}` sin cita
- [x] quality_criteria — 2 acciones concretas; regla con umbral >=2 cumplido
- [x] upgrade_safety — diff mostrado, pendiente de confirmacion; append; sin `--force`

Veredicto guardian: conditional (regla pendiente de confirmacion del operador)
