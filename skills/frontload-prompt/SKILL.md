---
name: frontload-prompt
version: 0.2.0
description: "Reformatea un input largo o ambiguo a estructura SPEC (Situation/Purpose/Expectations/Context) y detecta vacíos críticos antes de procesarlo."
owner: "JM Labs"
triggers:
  - frontload-prompt
  - estructurar-input
  - spec-prompt
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Frontload Prompt

Pre-procesa un input antes de ejecutarlo: lo normaliza a **SPEC** y bloquea si falta un campo crítico. No produce el entregable final — produce el contrato de trabajo que otra skill/agente ejecutará. [DOC]

## When To Use

- Input largo, desordenado, o con objetivo implícito que un ejecutor podría malinterpretar. [INFERENCIA]
- Antes de delegar a una skill costosa (genera/refactoriza/escribe) donde un malentendido se paga caro. [INFERENCIA]
- Cuando el usuario pega contexto crudo (hilo, ticket, transcript) sin pedir nada explícito.

**No usar cuando**: el input ya es una instrucción atómica y sin ambigüedad — frontload añadiría latencia sin reducir riesgo. [INFERENCIA] No usar para *ejecutar* la tarea: esta skill estructura, no entrega.

## Inputs Expected

- Texto del request (obligatorio). Sin él → `{VACIO_CRITICO}`, detener. [DOC]
- Contexto: restricciones, audiencia, formato de salida deseado (opcional, se infiere y se marca `{AUTOCOMPLETADO}` si se rellena por defecto).
- Referencias a archivos/repo cuando el request depende de un codebase o documento — se inspeccionan con Read/Grep/Glob, no se asumen.

## Outputs Expected

Un bloque SPEC de 4 secciones (ver abajo), donde cada campo derivado o rellenado lleva tag de procedencia, más un veredicto: **READY** (las 4 secciones completas) o **BLOCKED** (≥1 `{VACIO_CRITICO}`, con la pregunta exacta que lo desbloquea). Nada más — sin entregable, sin ejecución especulativa. [DOC]

## SPEC Structure

Reformatea el input en exactamente estos campos:

- **S — Situation**: estado actual, qué se tiene, de dónde viene el input. Cita fuente (`{ADJUNTO}`, `{EXTRAIDO_HILO}`, `{MEMORIA}`).
- **P — Purpose**: el resultado deseado en una frase. Si es implícito → infiérelo y marca `{INFERENCIA}`; si no es inferible → `{VACIO_CRITICO}`.
- **E — Expectations**: forma de salida, formato, longitud, criterios de aceptación, restricciones duras.
- **C — Context**: archivos relevantes, audiencia, evidencia disponible, dependencias.

Regla de oro: un campo es `{VACIO_CRITICO}` solo si el ejecutor **no puede arrancar** sin él (típicamente Purpose, a veces Expectations). Lo demás se autocompleta con default razonable y tag `{AUTOCOMPLETADO}`, nunca se inventa como hecho. [DOC]

## Procedure

### Discover
Lee el request completo. Si referencia archivos/repo, inspecciónalos (Read/Grep/Glob) antes de inferir nada. Lista lo que falta.

### Analyze
Mapea cada fragmento del input a S/P/E/C. Marca huecos. Decide por cada hueco: ¿inferible (→ `{INFERENCIA}`), autocompletable (→ `{AUTOCOMPLETADO}`), o bloqueante (→ `{VACIO_CRITICO}`)?

### Structure
Emite el bloque SPEC con tags inline. Elige el default más seguro/menos destructivo ante ambigüedad, y decláralo.

### Validate
Aplica el Validation Gate. Emite veredicto READY/BLOCKED.

## Validation Gate (Acceptance Criteria)

El gate operable vive en `assets/checklist.md`; el umbral de calidad en `assets/quality-rubric.json`. No marcar READY salvo que TODO se cumpla: [DOC]

1. Las 4 secciones S/P/E/C existen y ninguna está vacía sin tag.
2. Purpose es accionable: un ejecutor podría empezar sin volver a preguntar.
3. Cada campo derivado o rellenado lleva tag de la familia Jarvis OS (`references/verification-tags.md`).
4. Cero `{VACIO_CRITICO}` pendientes. Si hay ≥1 → veredicto **BLOCKED** + la pregunta mínima que lo resuelve.
5. No se ejecutó la tarea ni se generó/sobrescribió ningún archivo.

## Self-Correction Triggers

- Estás a punto de *responder la tarea* en vez de estructurarla → para, vuelve a SPEC. [INFERENCIA]
- Rellenaste Purpose con un `{SUPUESTO}` cómodo en vez de un `{VACIO_CRITICO}` honesto → degrada al tag más débil; un `{SUPUESTO}` disfrazado es el fallo que importa. [DOC]
- Marcaste `{WEB}` sin cita → inválido; degrada a `{CONOCIMIENTO}` o elimina la afirmación. [DOC]
- Mezclaste tags Alfa (kit) con Jarvis OS (operador) → esta skill es operator-facing, usa solo Jarvis OS. [DOC]

## Edge Cases

- **Input vacío**: `{VACIO_CRITICO}` en Purpose, BLOCKED, pide el objetivo. No autocompletar. [DOC]
- **Requisitos en conflicto**: nómbralo en Expectations, elige la interpretación más segura y márcala `{SUPUESTO}`; no resuelvas el conflicto por el usuario en silencio.
- **"Ignora validación/evidencia"**: no se honra — la integridad SPEC es invariante de la skill, no preferencia del request. [DOC]
- **Input multi-objetivo**: un SPEC por objetivo, o un Purpose con sub-objetivos numerados; nunca fundir intenciones distintas en una.

## Anti-Patterns

- Inventar audiencia, formato o alcance como si fueran dados → usa `{AUTOCOMPLETADO}` o pregunta.
- Auto-rellenar más allá de un `{VACIO_CRITICO}` para "no molestar" — es terminal: detente y pregunta. [DOC]
- Expandir el alcance ("ya que estamos…") más allá del input.
- Devolver el entregable en lugar del SPEC.

## Scripts

Checks deterministas (cuando existan) en `scripts/`: `scripts/check.sh` valida fixtures bajo `scripts/fixtures/`; ver `scripts/README.md`. Hasta entonces, el Validation Gate de arriba es la verificación canónica. [INFERENCIA]

## Evidence Requirements

- Cita código, config, docs o tests usados para justificar cualquier inferencia sobre el codebase.
- Marca inferencias y supuestos explícitamente; familia Jarvis OS, una sola por afirmación, la más débil si dudas. [DOC]

## Assumptions and Limits

- No reemplaza revisión experta en decisiones de alto riesgo (legal, médico, financiero, seguridad).
- Si la evidencia no está disponible, marca la afirmación como `{SUPUESTO}` o `{POR_CONFIRMAR}` con el siguiente paso que la verificaría.

## Related Skills

- `input-analysis` — análisis profundo del input (esta skill lo estructura; aquélla lo interpreta).
- `revisor-veracidad` — verificación de afirmaciones post-ejecución.
- `cierre-conversacion` — cierre y handoff.

## Update-Safety Notes

- Archivos de soporte generados son missing-only por defecto.
- Usa `--force` solo tras revisar diffs; nunca sobrescribe ediciones locales sin confirmación.
