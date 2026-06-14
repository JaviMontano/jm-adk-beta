---
name: daily-close
version: 0.2.0
description: "Cadencia de cierre diario: captura cerrado/pendiente/aprendido y siembra el dia siguiente (P10)."
owner: "JM Labs"
triggers:
  - daily-close
  - cierre-diario
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# Daily Close

Cadencia P10 de fin de jornada. Cierra el dia en tres ejes — **cerrado**,
**pendiente**, **aprendido** — y deja sembrado el dia siguiente para que el
arranque no parta de cero. Operador-facing: usa la familia de tags Jarvis OS
`{...}` (ver `references/verification-tags.md`). {MEMORIA}

## When to use

- Trigger explicito `daily-close` / `cierre-diario`, o al final de una jornada
  de ejecucion. {EXTRAIDO_HILO}
- NO usar para: planificacion semanal/mensual, retros de proyecto, o resumen
  de una sola tarea aislada — eso es otra cadencia. {INFERENCIA}

## Inputs

| Input | Obligatorio | Si falta |
|---|---|---|
| Fecha del cierre | si | autocompleta hoy `{AUTOCOMPLETADO}`, marca la suposicion |
| Fuente del dia (TAREAS.md, hilo, notas) | si | `{VACIO_CRITICO}`: pregunta que cerrar antes de inventar |
| Bitacora/MEMORY destino donde persistir | si | usa el destino por defecto del workspace activo |
| Foco/objetivo del dia siguiente | no | se infiere de los pendientes priorizados |

## Outputs

- **Bloque de cierre** con tres secciones: Cerrado, Pendiente, Aprendido.
- **Semilla del dia siguiente**: 1-3 pendientes priorizados + primer paso
  concreto de cada uno (accionable sin recontexto).
- **Notas de evidencia** con tags Jarvis OS en toda afirmacion no obvia.
- **Estado de validacion** y riesgos/bloqueos abiertos que cruzan al manana.

## Procedure

### 1. Discover
Lee la fuente del dia (TAREAS.md, hilo, notas) y MEMORY/bitacora destino antes
de escribir. Read-before-write es obligatorio. {MEMORIA} Identifica la fecha; si
no es explicita, autocompleta hoy y marca `{AUTOCOMPLETADO}`.

### 2. Classify
Asigna cada item a exactamente un eje:
- **Cerrado** — completado y verificable hoy. Liga evidencia (commit, archivo,
  hilo). {EXTRAIDO_HILO}
- **Pendiente** — abierto; anota por que no cerro y el primer paso de manana.
- **Aprendido** — insight, friccion o decision reusable. Sin esto, el cierre es
  un changelog, no una cadencia. {INFERENCIA}

### 3. Seed next day
Prioriza 1-3 pendientes (no la lista entera) y para cada uno escribe el primer
paso ejecutable en frio. Una semilla que necesita recontexto no esta sembrada.

### 4. Persist
Aplica el cierre de forma **aditiva** (append) a la bitacora/MEMORY destino con
Write/Edit. Nunca sobrescribas historico ni ediciones locales sin `--force` tras
revisar el diff. {SUPUESTO}

### 5. Validate
Corre el gate de aceptacion antes de declarar cierre.

## Validation gate (acceptance criteria)

- [ ] Los tres ejes presentes; ninguno vacio sin justificacion explicita.
- [ ] Cada item Cerrado tiene evidencia ligada y verificable. {DOC}
- [ ] La semilla tiene 1-3 pendientes priorizados, cada uno con primer paso.
- [ ] Toda afirmacion no obvia lleva exactamente un tag Jarvis OS; sin mezclar
      familias; `{WEB}` sin cita es invalido. {DOC}
- [ ] Persistencia aditiva; historico y ediciones locales intactos.
- [ ] Bloqueos abiertos marcados `{POR_CONFIRMAR}` con paso de verificacion.

Si algun check falla, corrige y reevalua — no entregues un cierre parcial.
El gate se opera con `assets/checklist.md` y `assets/quality-rubric.json`.

## Self-correction triggers

- Item ambiguo entre Cerrado y Pendiente → es Pendiente (el cierre se gana, no
  se asume). {INFERENCIA}
- Eje Aprendido vacio → relee la jornada por fricciones/decisiones antes de
  declararlo vacio; el vacio real es legitimo, el vacio por pereza no.
- Semilla > 3 items → re-prioriza; sembrar todo es no sembrar nada.
- Fecha o fuente ausente → `{VACIO_CRITICO}`, detente y pregunta.

## Edge cases

- **Dia sin actividad**: registra el cierre igual (mantiene la cadencia) y
  marca explicitamente "sin avances" en lugar de omitir la entrada.
- **Dia desbordado**: captura cabeceras, no transcripcion; el cierre es indice,
  no acta.
- **Requisitos en conflicto** (p.ej. "cierra pero ignora validacion"): nombra el
  conflicto y elige la interpretacion segura — la validacion no es opcional.
- **Cierre tardio/retroactivo**: fecha el bloque al dia real, no al de captura;
  marca `{SUPUESTO}` lo reconstruido de memoria.
- **Multi-workspace**: cierra por workspace activo; no fusiones bitacoras de
  marcas/proyectos distintos (disciplina de marca unica).

## Anti-patterns (anti-scope)

- Convertir el cierre en changelog (solo Cerrado, sin Aprendido ni semilla).
- Volcar la lista completa de pendientes como "semilla" sin priorizar.
- Sobrescribir el historico en vez de hacer append.
- Mezclar familias de tags Jarvis `{...}` y Alfa `[...]` en el mismo documento.
- Inventar items para llenar un eje vacio.

## Assumptions and limits

- No reemplaza revision experta para decisiones de alto riesgo (legal, medico,
  financiero, seguridad).
- Sin evidencia disponible, marca el item como `{SUPUESTO}` o `{POR_CONFIRMAR}`
  con su paso de verificacion; nunca lo presentes como hecho.

## Related skills

- `workspace-governance` — destino y disciplina de persistencia.
- `workflow-forge` — encadenar daily-close en cadencias mayores.
- `quality-guardian` — refuerza el gate de validacion.

## Update-safety notes

- Archivos de soporte generados: missing-only por defecto.
- `--force` solo tras revisar diffs; preserva ediciones locales.
