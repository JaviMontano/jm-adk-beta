# Body of Knowledge — WBR Weekly Review (P11)

Conocimiento de dominio para conducir un repaso semanal accionable. {CONOCIMIENTO}

## Conceptos clave

- **Cadencia P11.** Ritual operativo de cierre semanal dentro de la malla Jarvis
  OS de cadencias: la jornada (P10 daily-close), la semana (P11 WBR) y el mes
  (monthly-audit). El WBR convierte el ruido de la semana en un acta corta que se
  puede ejecutar sin reabrir la semana.
- **Los tres lentes.** Toda senal se mira por exactamente uno:
  - *Avance* — algo cerrado o movido de verdad, con artefacto verificable.
  - *Estancado* — algo en curso que no avanzo lo esperado; requiere diagnostico.
  - *Friccion* — algo que costo mas de lo debido; recurrente o puntual.
- **Causa raiz vs sintoma.** El estancado se diagnostica por su causa (dependencia,
  decision pendiente, capacidad, ambiguedad de alcance), no por su sintoma.
- **Arrastre.** Item abierto heredado de semanas previas; se cuenta en semanas. A
  partir de 3 semanas deja de ser estancado y pasa a bloqueo.
- **Compromiso con criterio de hecho.** Promesa de la proxima semana con una
  condicion observable que decide si se cumplio; no una intencion difusa.

## Estandares

- **Acta escaneable en Markdown** con seis secciones fijas (encabezado, avances,
  estancado, friccion, compromisos, arrastres). El orden no cambia.
- **Una sola familia de tags** Jarvis OS `{...}`, nunca mezclada con Alfa `[...]`;
  exactamente un tag por afirmacion no obvia. Ver `references/verification-tags.md`.
- **Semana ISO** como unidad de periodo (p.ej. 2026-W24); fecha de corte explicita.
- **Never green-as-success**: ningun avance se declara cerrado sin evidencia ligada.

## Reglas de decision

1. Item ambiguo entre avance y estancado → estancado (el avance se gana con evidencia).
2. Estancado sin dueno → mal cerrado; asignar dueno antes de entregar.
3. Estancado sin proximo paso fechado → falla el gate; "se revisara" no cuenta.
4. Friccion recurrente (≥2 semanas) → escalar a accion estructural, no a parche.
5. Arrastre ≥3 semanas → `{POR_CONFIRMAR}` + escalada a bloqueo.
6. Compromiso previo incumplido → nombrarlo y heredarlo; nunca borrarlo en silencio.
7. >5 compromisos para la proxima semana → re-priorizar; la dilucion garantiza incumplimiento.
8. Varias estaciones en un WBR → separar por alcance o pedir foco; no promediar.

## Anti-patterns

- Reporte de estado sin dueno ni proximo paso (eso es un log, no un WBR).
- Pintar todo verde para evitar conversaciones incomodas.
- Mover un estancado a avances porque "ya casi".
- Inflar avances con actividad (reuniones, lecturas) en vez de resultados.
- Inventar la semana cuando falta periodo o alcance, en vez de preguntar.

## Edge cases

- **Semana vacia / vacaciones**: registrar "sin actividad" + razon (`{SUPUESTO}`),
  no fabricar avances.
- **Todo verde, nada estancado**: sospechar subreporte; preguntar que NO se movio.
- **Compromiso previo incumplido**: nombrarlo y heredarlo a la nueva semana.
- **Conflicto de alcance**: un acta cubre un solo alcance.
