---
name: weekly-retro
version: 0.2.0
description: "Cadencia de retro semanal (P12): captura que ayudo, que friccion hubo, y promueve aprendizajes recurrentes a reglas persistentes."
owner: "JM Labs"
last_updated: 2026-06-11
triggers:
  - weekly-retro
  - retro-semanal
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# Weekly Retro

Ritual semanal de cierre: convierte la experiencia de la semana en mejoras
accionables y, cuando un patron se repite, en una **regla persistente** (la
promocion P12). No es un journal libre — produce un artefacto estructurado y,
condicionalmente, un cambio en la memoria operativa. [DOC]

## When to use / not use

- **Use**: cierre de semana o de sprint; al detectar friccion repetida; cuando
  quieras consolidar un aprendizaje en regla antes de que se pierda. [DOC]
- **No uses**: post-mortem de un incidente puntual (usa el flujo de incidentes);
  retro de equipo multi-persona con facilitacion (esto es cadencia personal de
  operador). [INFERENCIA]

## Inputs

- **Ventana**: rango de la semana/sprite a revisar (default: ultimos 7 dias). [AUTOCOMPLETADO]
- **Fuentes de evidencia**: TAREAS.md / tasklog, changelog, hilos relevantes,
  commits. Sin al menos una fuente verificable, marca `{VACIO_CRITICO}` y pide. [DOC]
- **Memoria destino**: ruta del archivo de reglas/MEMORY donde aterriza una
  promocion P12 (si el operador quiere promover). [SUPUESTO]

## Outputs

- Bloque de retro estructurado: **Ayudo / Friccion / Regla candidata**, cada
  item con su tag de evidencia. [DOC]
- Lista de acciones para la proxima semana (owner implicito = operador). [DOC]
- 0..n **promociones P12**: regla redactada + ruta destino, aplicada solo tras
  confirmacion explicita del operador. [SUPUESTO]

## Procedure

### 1. Discover
Define la ventana y abre las fuentes de evidencia (tasklog, changelog, hilos).
Si no hay ninguna fuente leible, detente con `{VACIO_CRITICO}`. [DOC]

### 2. Analyze — los tres ejes (P12)
- **Que ayudo**: que practica/herramienta/decision aceleró el trabajo. Cita la
  fuente (`{EXTRAIDO_HILO}`, `{MEMORIA}`, commit). [DOC]
- **Que friccion**: que costo tiempo o causó retrabajo. Distingue ruido de una
  semana (no promover) de patron recurrente (candidato a regla). [INFERENCIA]
- **Que se vuelve regla**: solo asciende friccion vista **>=2 veces** o un acierto
  que quieras volver default. Redacta la regla en imperativo, una linea. [INFERENCIA]

### 3. Execute
Escribe el bloque de retro. Para cada regla candidata, presenta el diff exacto
sobre el archivo de memoria destino y **espera confirmacion** antes de aplicar
(`Write`/`Edit`). Nunca promuevas en automatico. [SUPUESTO]

### 4. Validate
Corre el gate de abajo antes de cerrar. [DOC]

## Validation gate (acceptance criteria)

Cierra solo si TODO se cumple — mapea a los checks de `evals.json`
(`evidence`, `quality_criteria`, `upgrade_safety`). El guardian verifica contra
`assets/quality-rubric.json` y `assets/checklist.md` (ver `assets/README.md`): [CONFIG]

- [ ] **evidence**: cada item de Ayudo/Friccion lleva exactamente un tag del set
  Jarvis OS; ningun `{WEB}` sin cita; todo `{SUPUESTO}`/`{POR_CONFIRMAR}` con
  paso de verificacion. [DOC]
- [ ] **quality_criteria**: hay >=1 accion concreta para la proxima semana y, si
  no hubo regla, una linea que justifica por que (no todo patron asciende). [INFERENCIA]
- [ ] **upgrade_safety**: ninguna promocion P12 escribio memoria sin diff
  mostrado + confirmacion; archivos locales preservados; `--force` no usado a
  ciegas. [CONFIG]

## Edge cases

- **Sin evidencia legible** → `{VACIO_CRITICO}`, pide la fuente, no inventes la
  semana. [DOC]
- **Semana vacia / sin friccion** → retro valido y corto; registra "sin patron
  nuevo" y omite promocion. No fuerces una regla. [INFERENCIA]
- **Friccion vista una sola vez** → registrala como observacion, **no** la
  asciendas a regla todavia. [INFERENCIA]
- **Regla candidata contradice una regla ya en memoria** → no sobrescribas;
  expón el conflicto y pide al operador resolver. [SUPUESTO]
- **Operador rechaza la promocion** → conserva la observacion en el bloque de
  retro para la proxima ventana. [INFERENCIA]

## Anti-patterns

- Promover en automatico sin confirmacion (rompe `upgrade_safety`). [CONFIG]
- Ascender ruido de una sola semana a regla (inflación de reglas). [INFERENCIA]
- Retro como prosa sin los tres ejes ni tags de evidencia. [DOC]
- Mezclar familias de tags (Jarvis vs Alfa) en el mismo bloque. [DOC]

## Self-correction triggers

- Escribiste una regla pero no mostraste el diff destino → vuelve al paso 3. [INFERENCIA]
- Un item de Friccion no tiene fuente citable → degradalo a observacion o
  marcalo `{POR_CONFIRMAR}` con su verificacion. [DOC]
- La retro no produjo ni accion ni regla → revisa: ¿faltó leer una fuente? [INFERENCIA]

## Evidence convention

Usa el **set Jarvis OS (operador)** de `references/verification-tags.md`:
`{MEMORIA}` `{ADJUNTO}` `{EXTRAIDO_HILO}` `{WEB}` `{CONOCIMIENTO}` `{SUPUESTO}`
`{INFERENCIA}` `{AUTOCOMPLETADO}` `{POR_CONFIRMAR}` `{VACIO_CRITICO}`. Una sola
familia por documento; un tag por claim; ante duda elige el mas debil. [DOC]

## Assumptions and limits

- Cadencia personal de operador, no facilitacion de equipo. [SUPUESTO]
- No reemplaza revision experta en decisiones legales/medicas/financieras/
  seguridad de alto riesgo. [DOC]

## Related skills

- `workflow-forge` — convierte una regla recurrente en flujo formal.
- `quality-guardian` — valida el gate de evidencia del bloque de retro.
- `workspace-governance` — gobierna donde aterrizan las promociones P12.
