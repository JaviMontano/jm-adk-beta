# wbr-weekly-review

Cadencia **WBR (P11)**: repaso semanal de una estacion, sector o proyecto a traves
de tres lentes — **avances**, **estancado**, **friccion** — que produce un acta
corta y accionable. Cada item estancado o friccionado queda con dueno y proximo
paso fechado, de modo que el lunes se actua sin reabrir la semana. {CONOCIMIENTO}

## Que hace

- Cierra la semana ISO de un alcance unico y mide cumplimiento **real** de los
  compromisos previos (cumplido / parcial / no-cumplido), sin omitir los fallidos.
- Clasifica cada senal en exactamente un lente; un estancado nunca se disfraza de
  avance.
- Diagnostica cada estancado (antiguedad, causa raiz, dueno) y deriva 3-5
  compromisos para la proxima semana desde estancado+friccion, no desde deseos.
- Arrastra items abiertos heredados con conteo de semanas; ≥3 semanas escala a
  bloqueo.

## Cuando usarlo / cuando no

- **Usar**: cierre semanal, handoff entre semanas, deteccion temprana de
  estancamiento. Disparadores: `wbr`, `weekly-review`, `repaso-semanal`.
- **No usar**: planificacion intradia (`dbr-daily-plan`), auditoria mensual
  (`monthly-audit`), retro formal de equipo. {INFERENCIA}
- Sin periodo ni alcance claro → `{VACIO_CRITICO}`: detener y preguntar, no
  inventar la semana.

## Como enruta / ejecuta

`Recolectar → Clasificar → Diagnosticar estancado → Comprometer → Validar`.
El acta solo se declara hecha tras pasar el gate de aceptacion (ver SKILL.md).
Roles: lead orquesta el flujo, specialist aporta criterio de clasificacion y causa
raiz, support arma evidencia y tablas, guardian corre el gate.

## Referencias

- `SKILL.md` — contrato operativo, inputs/outputs, gate, edge cases, anti-patterns.
- `references/verification-tags.md` — familia de tags Jarvis OS `{...}` (una sola
  familia por documento). {DOC}
- `knowledge/body-of-knowledge.md` — conceptos, estandares y reglas de decision.
- `templates/output.md` — scaffold del acta WBR.
- `prompts/` — prompts primario, meta y variaciones quick/deep.
- `examples/` — ejemplo trabajado de entrada y acta resultante.
- `assets/` — rubrica de calidad y checklist del gate (ver `assets/README.md`).

## Skills relacionados

- `dbr-daily-plan` — cadencia diaria que alimenta este WBR. {CONFIG}
- `daily-close` — cierres de jornada cuyos arrastres entran al estancado semanal.
- `monthly-audit` — agrega varios WBR en una mirada mensual.
