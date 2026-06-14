---
name: persistent-memory-design
version: 1.1.0
last_updated: 2026-06-11
description: "Disena un scratchpad persistente en disco (Hypotheses/Decisions/Findings/Open) con solo conclusiones validadas que sobrevive a /compact y reset, se lee una vez y luego se referencia para no romper el prompt cache."
owner: "JM Labs"
status: stable
triggers:
  - persistent memory design
  - scratchpad file
  - durable agent memory
  - investigation notes
  - survives compact
  - prompt cache scratchpad
tags:
  - context-engineering
  - agent-memory
  - provenance
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Persistent Memory Design

## Capacidad

Disenar e implementar un scratchpad persistente en disco que actua como memoria duradera de un agente: un archivo estructurado (Hypotheses / Decisions / Findings / Open) que solo contiene conclusiones validadas, sobrevive a `/compact` o a un reset de sesion, se lee una sola vez al arrancar y despues se referencia en vez de releerse. Es ingenieria de contexto: separa la memoria de trabajo volatil (la conversacion) de la memoria persistente auditada (el archivo). [DOC]

## Cuando usarla

- Investigacion o tarea larga que no cabe en una ventana de contexto y debe sobrevivir a compactaciones. [DOC]
- Flujos multi-sesion donde manana hay que retomar sin re-derivar todo. [DOC]
- El agente repite trabajo porque "olvida" conclusiones ya validadas. [INFERENCE]
- El scratchpad existente se relee cada turno y rompe el prompt cache. [INFERENCE]

**No la uses** para apuntes efimeros de un solo turno, para volcar transcript crudo, ni como cola de tareas mutable de alta frecuencia (eso pertenece a un task store, no a memoria auditada). Eso no es conclusion validada. [INFERENCE]

## Entradas / Salidas

- **Entrada:** objetivo de la sesion, ruta destino del scratchpad, evidencia que el agente va produciendo (sources, fechas). [DOC]
- **Salida:** el archivo `.agent/scratchpad.md` con esquema fijo + un protocolo de lectura-unica/escritura-idempotente que el runtime del agente respeta. Opcional: reporte JSON de diseno validado por el checker. [DOC]
- **Invariante:** el esquema de secciones es fijo; solo evoluciona el contenido. [DOC]

## Como construir

1. **Define el contrato del archivo.** Ruta estable (p. ej. `.agent/scratchpad.md`) y esquema fijo: `## Hypotheses`, `## Decisions`, `## Findings`, `## Open`. El esquema es invariante. [DOC]
2. **Filtra que entra.** Solo conclusiones validadas con evidencia minima (source, fecha). Nada de razonamiento en bruto ni resultados de tools sin confirmar. [DOC]
3. **Escribe en append/update tipado (idempotente).** Cada hallazgo se anade o reemplaza su entrada por clave estable; nunca se reescribe el archivo entero por gusto (un rewrite total invalida el prompt cache de todo lo anterior). [INFERENCE]
4. **Lee una vez, referencia despues.** Al iniciar sesion, lee el scratchpad una sola vez hacia el contexto y cachea el estado parseado. En turnos posteriores referencia las secciones; no vuelvas a leer el archivo. [DOC]
5. **Verifica supervivencia.** Confirma que tras `/compact` o reset el agente reconstruye estado solo desde el archivo, sin la conversacion previa. [DOC]
6. **Resuelve concurrencia.** Si dos pasos/agentes escriben, define orden de escritura (upsert por clave) o un lock simple; el ultimo upsert por clave gana, nunca un merge ciego de texto. [INFERENCE]

### Decisiones y trade-offs

- **Markdown plano sobre JSON/DB.** Markdown es legible por humano y por el agente sin parser fragil, y diffea limpio en git; se paga perdiendo validacion de esquema estricta — se compensa con el checker de `assets/`. [INFERENCE]
- **Upsert por clave sobre append puro.** Append puro crece sin techo y duplica hallazgos corregidos; el upsert mantiene una sola verdad por entrada a costa de exigir una clave estable por hallazgo. [INFERENCE]
- **Lectura unica sobre relectura por turno.** Releer garantiza frescura pero rompe el cache y reintroduce ruido; la lectura unica asume que toda mutacion pasa por la capa de escritura del propio agente. [SUPUESTO]

## Activos determinísticos

Usa `assets/manifest.json` como indice de contratos offline. Los contratos en `assets/` fijan la ruta permitida, secciones, evidencia minima, politica de lectura unica, escritura idempotente y reconstruccion tras compact/reset. Si produces un reporte JSON de diseno, validalo con `bash skills/persistent-memory-design/scripts/check.sh` antes de marcarlo como aceptado. [CONFIG] Si `assets/` o `scripts/` aun no existen en el repo, generalos a partir del esquema de este SKILL antes de cerrar la tarea — el gate de validacion los exige. [SUPUESTO]

## Patrón correcto

```python
# GOOD: scratchpad estructurado, solo conclusiones validadas, lectura unica.
SCRATCHPAD = ".agent/scratchpad.md"

def bootstrap(ctx):
    # Read once at session start; cache the parsed state.
    if ctx.scratchpad_loaded:
        return ctx.memory  # reference, do not re-read
    ctx.memory = parse_sections(read_file(SCRATCHPAD))
    ctx.scratchpad_loaded = True
    return ctx.memory

def record_finding(finding):
    # Append only validated conclusions, each with provenance; upsert by key.
    assert finding.validated and finding.source
    upsert_section(SCRATCHPAD, "Findings", key=finding.id,
                   line=f"- {finding.text} [src:{finding.source} @ {finding.date}]")
```

## Anti-patrón

```python
# ANTI: la "memoria" vive en la conversacion y el archivo se relee cada turno.
def step(ctx):
    notes = read_file(".agent/notes.txt")   # re-read every turn -> breaks cache
    ctx.history.append(notes)               # state lives in volatile chat
    notes += "\n" + raw_tool_dump           # unstructured, unvalidated noise
    write_file(".agent/notes.txt", notes)   # full rewrite, no schema
    # After /compact: state is gone, agent re-derives everything.
```

**Otros anti-patrones:** secciones de esquema variable entre sesiones (rompe el parser de bootstrap); guardar hipotesis sin marcar como no-validadas mezcladas con findings (contamina el estado de verdad); meter la cola de tareas pendientes con churn alto en el mismo archivo cacheado. [INFERENCE]

## Triggers de auto-correccion

- Si te encuentras leyendo el scratchpad mas de una vez por sesion -> el estado no se esta cacheando; arregla el bootstrap. [INFERENCE]
- Si un `record_*` reescribe el archivo completo -> cambia a upsert por clave. [INFERENCE]
- Si una entrada no tiene `[src:... @ ...]` -> no es conclusion validada; va a Hypotheses/Open, no a Findings/Decisions. [DOC]
- Si tras `/compact` el agente pide datos que estaban en la conversacion -> esos datos nunca se persistieron; el filtro de "que entra" esta mal. [INFERENCE]

## Checklist de validación (gate de aceptacion)

Acepta solo si TODO se cumple:

- ¿El archivo contiene solo conclusiones validadas (no razonamiento crudo ni tool dumps)? [DOC]
- ¿Tiene un esquema de secciones fijo (Hypotheses / Decisions / Findings / Open)? [DOC]
- ¿Se lee una sola vez y luego se referencia, sin relectura por turno? [DOC]
- ¿La escritura es idempotente (upsert por clave), sin rewrite total del archivo? [INFERENCE]
- ¿El estado sobrevive a `/compact` y a un reset de sesion, reconstruible solo desde el archivo? [DOC]
- ¿Cada hallazgo lleva su evidencia minima (source, fecha)? [DOC]
- ¿Esta resuelta la concurrencia si hay multiples escritores? [INFERENCE]
- ¿El reporte JSON pasa `scripts/check.sh` contra los contratos en `assets/`? [CONFIG]

## Edge cases

- **Archivo ausente en bootstrap:** trata como estado vacio, no como error; crea el esqueleto de secciones. [INFERENCE]
- **Scratchpad corrupto / esquema roto:** falla ruidoso y para; nunca sobrescribas a ciegas un archivo que no parsea. [SUPUESTO]
- **Hallazgo contradicho mas tarde:** upsert reemplaza la entrada por su clave y registra el cambio en Decisions, no acumula ambas versiones. [INFERENCE]
- **Crecimiento ilimitado:** poda Open resueltos y colapsa Findings obsoletos por clave; el archivo es estado, no log. [INFERENCE]

## Katas y skills relacionadas

- Katas: `18`. [CONFIG]
- Relacionadas: `katas-persistent-scratchpad`, `adaptive-investigation-method`, `provenance-engineering`, `session-lifecycle-management`. [CONFIG]
