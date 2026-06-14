---
name: dbr-daily-plan
version: 0.2.0
description: "Cadencia DBR: selecciona <=3 prioridades-tambor del dia y emite el plan diario P09 con buffers y evidencia."
owner: "JM Labs"
triggers:
  - dbr
  - daily-plan
  - plan-diario
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# Dbr Daily Plan

Cadencia diaria **Drum-Buffer-Rope** (Teoria de Restricciones) que produce el
plan del dia **P09**: como maximo **3 prioridades-tambor** que marcan el ritmo,
mas el buffer que las protege. No es una to-do list: es una decision de foco
bajo restriccion. [INFERENCIA]

## When To Use

- Inicio de jornada o turno: convertir backlog/agenda dispersa en un plan de
  <=3 focos ejecutables. [DOC]
- El usuario pide "plan del dia", "prioridades de hoy", "dbr" o "P09".
- Hay mas trabajo candidato que capacidad realista del dia (sintoma de tambor). [INFERENCIA]

**No usar** para planificacion semanal/trimestral, gestion de proyecto multi-dia
(usa la cadencia que corresponda), ni cuando el usuario solo quiere capturar
tareas sin priorizar.

## Inputs Expected

- **Backlog/agenda del dia** (tareas, reuniones, compromisos). Si falta, es
  `{VACIO_CRITICO}`: detener y pedirlo.
- **Restriccion del dia**: horas reales disponibles, energia, dependencias,
  hard deadlines. Si no se da, estimar y marcar `{AUTOCOMPLETADO}`.
- **Contexto de continuidad**: plan/compromisos de ayer, WIP abierto
  (`{MEMORIA}` si viene de MEMORY.md, `{EXTRAIDO_HILO}` si del hilo).
- **Definicion de "dia ganado"** (opcional): que resultado hace que el dia
  cuente. Si falta, derivarlo de la prioridad #1.

## Outputs Expected — el plan P09

1. **Tambor**: 1-3 prioridades ordenadas, cada una con resultado verificable
   ("hecho" observable, no "avanzar en X").
2. **Buffer**: para cada prioridad, el riesgo que la puede frenar y el margen/
   mitigacion reservado.
3. **No-hoy**: candidatos descartados explicitamente (protege el foco).
4. **Primer paso** de la prioridad #1 (accionable en <15 min).
5. **Tags de evidencia** en toda fuente o supuesto no trivial.

## Procedure

### Discover
Reune backlog, restriccion y continuidad de ayer. Si el backlog esta vacio,
emite `{VACIO_CRITICO}` y para. Marca origen de cada item
(`{MEMORIA}`/`{EXTRAIDO_HILO}`/`{ADJUNTO}`). [DOC]

### Analyze (encontrar el tambor)
- Ordena candidatos por impacto-en-la-restriccion, no por urgencia percibida.
- Si >3 superan el corte, fuerza el recorte: el valor de DBR es decir "no". [INFERENCIA]
- Verifica capacidad: suma estimada de las prioridades <= horas reales menos
  buffer. Si no cabe, recorta antes de planificar — nunca sobre-comprometas. [INFERENCIA]

### Execute
Escribe el plan P09 con tambor, buffer, no-hoy y primer paso. Cada prioridad
con resultado verificable. Mantén el plan en una pantalla. [DOC]

### Validate
Corre el gate de abajo antes de entregar. Si algun item falla, corrige o
degrada el plan (menos prioridades) en vez de entregar inflado. [DOC]

## Validation Gate (acceptance criteria)

Entregar SOLO si todas se cumplen: [DOC]

- [ ] **<=3 prioridades-tambor.** 4+ es un fallo de la cadencia, no un plan rico.
- [ ] Cada prioridad tiene **resultado verificable** (criterio de "hecho").
- [ ] **Capacidad respeta la restriccion**: suma estimada + buffer <= horas reales.
- [ ] Existe **buffer/mitigacion** para el riesgo principal de cada prioridad.
- [ ] Hay lista **no-hoy** explicita (el foco se defiende descartando).
- [ ] **Primer paso** de la #1 es accionable hoy en <15 min.
- [ ] Toda fuente/supuesto no trivial lleva **tag** de la familia Jarvis.

## Anti-Patterns

- **To-do list disfrazada**: 8 items sin tambor ni buffer. No es P09. [INFERENCIA]
- **Falso buffer**: prioridades que ya llenan el 100% del dia sin margen — el
  primer imprevisto rompe el plan. [INFERENCIA]
- **Urgencia = prioridad**: ordenar por lo que grita mas alto en vez de por
  impacto en la restriccion.
- **Recompromiso silencioso**: arrastrar el plan de ayer sin revisar si sigue
  siendo el tambor correcto.
- **Sobre-tagueo**: tags en lo evidente; degrada la escaneabilidad. [DOC]

## Edge Cases

- **Backlog vacio**: `{VACIO_CRITICO}` — pide la agenda/tareas, no inventes.
- **Todo es P0**: si el usuario marca todo critico, expon la contradiccion y
  fuerza un ranking; DBR requiere un solo tambor a la vez. [INFERENCIA]
- **Dia ya saturado por reuniones**: el tambor puede ser proteger 1 bloque de
  foco; di explicitamente que la capacidad ejecutable es minima. [SUPUESTO]
- **Requisitos en conflicto**: nombra el conflicto y elige la lectura mas segura.
- **Personalizacion local**: preserva archivos `.local`/`user-context`; cambios
  aditivos. No sobrescribas ediciones del usuario.

## Quality Criteria

- El plan responde "¿que hace que hoy cuente?" con <=3 focos.
- Claims tagueados con evidencia cuando el entorno anfitrion lo exige.
- No se sobrescriben overrides locales ni archivos generados sin `--force`.
- Resultado accionable, en una pantalla, con criterios de aceptacion claros.

## Assumptions and Limits

- No sustituye revision experta en decisiones legales, medicas, financieras o
  de seguridad de alto riesgo.
- Si no hay evidencia, marca el claim como `{SUPUESTO}` o `{POR_CONFIRMAR}`.
- Planifica un (1) dia; no es roadmap ni gestion de dependencias multi-dia. [INFERENCIA]

## Related Skills

- `workspace-governance`
- `workflow-forge`
- `quality-guardian`

## Evidence Requirements

- Usa la familia **Jarvis OS** (operador): `{MEMORIA}`, `{ADJUNTO}`,
  `{EXTRAIDO_HILO}`, `{SUPUESTO}`, `{INFERENCIA}`, `{AUTOCOMPLETADO}`,
  `{POR_CONFIRMAR}`, `{VACIO_CRITICO}`. No mezclar con la familia Alfa. [DOC]
- `{VACIO_CRITICO}` es terminal: detener y preguntar, nunca auto-rellenar.

## Assets

- Rubrica y checklist del gate en `assets/` (`quality-rubric.json`,
  `gate-checklist.md`); ver `assets/README.md`.

## Update-Safety Notes

- Los archivos de soporte generados son missing-only por defecto.
- Usa `--force` solo tras revisar diffs.
