# daily-close

Cadencia P10 de fin de jornada para Jarvis OS. Cierra el dia en tres ejes
—**Cerrado**, **Pendiente**, **Aprendido**— y deja **sembrado** el dia siguiente
para que el arranque no parta de cero.

## Que hace

Toma la jornada (TAREAS.md, hilo, notas) y la persiste de forma **aditiva** en la
bitacora/MEMORY del workspace activo como un bloque de cierre fechado, mas una
**semilla** de 1-3 pendientes priorizados con su primer paso ejecutable en frio.
Toda afirmacion no obvia lleva exactamente un tag Jarvis OS `{...}`.

## Cuando usarla

- Trigger explicito `daily-close` / `cierre-diario`, o al final de una jornada de
  ejecucion. {EXTRAIDO_HILO}
- NO para planificacion semanal/mensual, retros de proyecto, ni resumen de una
  tarea aislada — esas son otras cadencias. {INFERENCIA}

## Como enruta y ejecuta

Flujo lineal de 5 pasos (no hay ramas de topic; es una cadencia unica):

1. **Discover** — lee fuente del dia + destino de persistencia (read-before-write).
2. **Classify** — cada item a exactamente un eje (Cerrado / Pendiente / Aprendido).
3. **Seed next day** — prioriza 1-3 pendientes, primer paso por cada uno.
4. **Persist** — append a bitacora/MEMORY; nunca sobrescribe historico.
5. **Validate** — corre el gate de aceptacion antes de declarar cierre.

El **lead** orquesta el spine; el **specialist** aporta criterio de clasificacion
y priorizacion; el **support** ejecuta lectura/escritura aditiva y arma evidencia;
el **guardian** corre el gate y bloquea el "hecho" si algun check falla.

## Referencias

- `references/verification-tags.md` — familia de tags Jarvis OS `{...}` y reglas
  de uso (una familia, sin mezclar con Alfa `[...]`).
- `knowledge/body-of-knowledge.md` — conceptos, estandares y reglas de decision.
- `knowledge/knowledge-graph.json` — grafo de los conceptos clave de la cadencia.
- `templates/output.md` — scaffold del bloque de cierre + semilla.
- `prompts/` — prompt primario, meta y variaciones quick/deep.
- `examples/` — ejemplo de entrada y salida real de un cierre.
- `assets/` — rubrica de calidad y checklist de gate (ver `assets/README.md`).

## Garantias de seguridad

- Persistencia **aditiva** por defecto; `--force` solo tras revisar diff.
- Disciplina de **marca unica**: no fusiona bitacoras de marcas/proyectos distintos.
- Sin evidencia, el item se marca `{SUPUESTO}` o `{POR_CONFIRMAR}`, nunca como hecho.
