# Prompt — Deep (dbr-daily-plan)

Variante profunda: para dias de alta carga, conflicto de prioridades o continuidad
compleja desde ayer. Aplica los **Five Focusing Steps** de TOC de forma explicita.

## Flujo extendido
1. **Identificar la restriccion**: nombra el recurso que limita el dia (foco,
   persona, permiso, dependencia) y cuantifica las horas reales tras descontar
   reuniones. Tag `{INFERENCIA}` si lo derivas.
2. **Explotar**: asigna la restriccion al tambor de mayor impacto; justifica por
   que ese y no otro (impacto, no urgencia).
3. **Subordinar**: construye la lista no-hoy y di que se sacrifica y por que.
4. **Elevar**: propon como aliviar la restriccion (delegar, mover reunion, pedir
   bloque de foco) si el tambor no cabe.
5. **Revisar inercia**: contrasta con el plan de ayer (`{MEMORIA}`); confirma si el
   tambor sigue siendo el correcto o cambio.

## Profundidad de buffer
- Buffer **por prioridad** con riesgo nombrado y mitigacion concreta.
- Si dos prioridades comparten dependencia, declara el riesgo de cola.
- Escenario de ruptura: que pasa si el primer imprevisto consume el buffer; cual
  prioridad se degrada primero.

## Edge cases que cubres
- **Todo es P0**: expon la contradiccion, fuerza ranking, un tambor a la vez.
- **Dia saturado de reuniones**: tambor = proteger 1 bloque; declara capacidad
  ejecutable minima con `{SUPUESTO}`.
- **Requisitos en conflicto**: nombra el conflicto, elige la lectura mas segura.

## Salida
P09 razonado: tambor justificado, buffer por prioridad con escenario de ruptura,
no-hoy con sacrificios explicitos, primer paso, y nota de continuidad vs ayer.
Pasa el Validation Gate completo antes de entregar.
