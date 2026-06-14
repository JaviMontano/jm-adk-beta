# dbr-daily-plan

Cadencia diaria **Drum-Buffer-Rope** (Teoria de Restricciones) que convierte un
backlog/agenda disperso en el plan del dia **P09**: como maximo **3
prioridades-tambor**, su buffer de proteccion y una lista explicita de **no-hoy**.
No es una to-do list — es una decision de foco bajo restriccion.

## What it does

- Encuentra el **tambor** del dia: las 1-3 prioridades que marcan el ritmo segun
  impacto-en-la-restriccion, no por urgencia percibida.
- Reserva **buffer**: el riesgo principal de cada prioridad y el margen/mitigacion
  que la protege.
- Defiende el foco con **no-hoy**: candidatos descartados de forma explicita.
- Verifica **capacidad**: suma estimada + buffer <= horas reales disponibles.
- Emite un **primer paso** accionable hoy en <15 min para la prioridad #1.

## When to use

- Inicio de jornada/turno: hay mas trabajo candidato que capacidad realista.
- El usuario pide "plan del dia", "prioridades de hoy", "dbr" o "P09".

No usar para planificacion semanal/trimestral, gestion multi-dia de dependencias,
ni para captura de tareas sin priorizar.

## How it routes / executes

Cuatro fases (ver `SKILL.md` → Procedure):

1. **Discover** — reune backlog, restriccion del dia y continuidad de ayer.
   Backlog vacio ⇒ `{VACIO_CRITICO}` terminal: detener y pedir.
2. **Analyze** — ordena por impacto-en-la-restriccion; fuerza el recorte a <=3;
   valida capacidad antes de planificar.
3. **Execute** — escribe el plan P09 con tambor, buffer, no-hoy y primer paso.
4. **Validate** — corre el Validation Gate; si algo falla, **degrada** el plan
   (menos prioridades) en vez de entregar inflado.

## Evidence taxonomy

Familia **Jarvis OS** (operador): `{MEMORIA}`, `{ADJUNTO}`, `{EXTRAIDO_HILO}`,
`{SUPUESTO}`, `{INFERENCIA}`, `{AUTOCOMPLETADO}`, `{POR_CONFIRMAR}`,
`{VACIO_CRITICO}`. No mezclar con la familia Alfa. `{VACIO_CRITICO}` es terminal.

## Bundle map

| Recurso | Para que |
|---------|----------|
| `SKILL.md` | Contrato canonico: procedure, gate, anti-patterns, edge cases |
| `agents/` | Roles: `lead` orquesta, `specialist` profundidad TOC, `support` ejecuta, `guardian` valida |
| `knowledge/body-of-knowledge.md` | Conceptos TOC/DBR, reglas de decision, definicion de tambor |
| `knowledge/knowledge-graph.json` | Grafo de los conceptos clave de la cadencia |
| `prompts/` | `primary`, `meta`, y variaciones `quick`/`deep` |
| `templates/output.md` | Scaffold del plan P09 |
| `examples/` | Caso trabajado entrada → P09 |
| `evals/evals.json` | Casos de aceptacion de la cadencia |
| `assets/` | Rubrica de calidad y checklist del gate (ver `assets/README.md`) |

## Related skills

`workspace-governance`, `workflow-forge`, `quality-guardian`.
