# weekly-retro — README

Cadencia personal de retro semanal (promocion **P12**) para el operador de
Jarvis OS. Cierra la semana convirtiendo la experiencia en mejoras accionables
y, cuando un patron se repite, en una **regla persistente** de la memoria
operativa. No es journaling libre: produce un artefacto estructurado de tres
ejes y, condicionalmente, un cambio gated en la memoria. {DOC}

## Que hace

- Recorre **Discover → Analyze → Execute → Validate** sobre la ventana de la
  semana (default: ultimos 7 dias).
- Clasifica la semana en tres ejes P12: **Ayudo / Friccion / Regla candidata**,
  cada item con un tag de evidencia de la familia Jarvis OS.
- Emite **0..n promociones P12**: una friccion vista >=2 veces (o un acierto que
  quieras volver default) asciende a regla, redactada en imperativo, una linea.
- Aterriza la regla en la memoria destino **solo tras diff mostrado +
  confirmacion explicita** del operador. Nunca promueve en automatico. {SUPUESTO}

## Cuando usarla / cuando no

- **Usar:** cierre de semana o sprint; al detectar friccion repetida; para
  consolidar un aprendizaje antes de que se pierda.
- **No usar:** post-mortem de un incidente puntual (flujo de incidentes); retro
  de equipo multi-persona con facilitacion (esto es cadencia personal). {INFERENCIA}

## Como rutea y ejecuta

Triggers: `weekly-retro`, `retro-semanal`. `allowed-tools`: Read, Write, Edit,
Bash. El flujo lee fuentes verificables (TAREAS.md/tasklog, changelog, hilos,
commits) antes de escribir; si no hay ninguna fuente leible, se detiene con
`{VACIO_CRITICO}` y pide. Las escrituras a memoria pasan siempre por el gate de
`upgrade_safety`. {CONFIG}

## Roles (agents/)

- **lead** — orquesta Discover→Analyze→Execute→Validate y entrega al guardian.
- **specialist** — criterio de la regla de los 3 ejes y umbral de promocion P12.
- **support** — lectura de fuentes, ensamblado del bloque y diff de memoria.
- **guardian** — gate de `evidence` / `quality_criteria` / `upgrade_safety`.

## Referencias

- `SKILL.md` — contrato completo (inputs, procedure, gate, edge cases).
- `references/verification-tags.md` — familia Jarvis OS de tags de evidencia.
- `knowledge/body-of-knowledge.md` — concepto P12, umbral de promocion, reglas.
- `templates/output.md` — scaffold del bloque de retro.
- `assets/` — rubrica de calidad y checklist del gate (ver `assets/README.md`).
- `evals/evals.json` — casos de verificacion del gate.
