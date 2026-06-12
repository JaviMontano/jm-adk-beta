---
name: prompt-chaining-design
version: 1.0.0
description: "Descomponer tareas grandes en pase local tipado y pase de integracion sobre resumenes, con schemas de transicion entre pases."
owner: "JM Labs"
triggers:
  - prompt chaining design
  - multipass decomposition
  - transition schema
  - chained passes
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Prompt Chaining Design

## Capacidad

Diseñar e implementar el procesamiento de una tarea grande como una **cadena de pases** en lugar de un único mega-prompt. El patrón canónico tiene dos etapas: un **pase local tipado** que procesa cada unidad (archivo, ticket, registro) de forma aislada y emite un resumen estructurado contra un schema, y un **pase de integración** que solo consume esos resúmenes —nunca los datos crudos— para producir el resultado final. Entre pases existe un **schema de transición** explícito que define qué viaja, en qué forma, y cómo se representa el error por unidad. La capacidad sustituye saturación de atención y costo cuadrático por paralelización tipada y trazable. [DOC]

## Inputs y outputs

**Inputs requeridos** (sin ellos: `{VACIO_CRITICO}`, parar y pedir — ver eval `empty_input`): [DOC]
- El **lote de unidades** o su descriptor (qué son, cuántas, cómo enumerarlas).
- La **definición de unidad atómica** o evidencia suficiente para derivarla.
- El **objetivo del pase de integración** (qué decide/sintetiza/agrega el resultado final).

**Outputs producidos**: [DOC]
- Schema del pase local (campos + estado `ok`/`error` por unidad).
- Schema de transición (colección tipada que viaja al pase 2).
- Diseño de los dos pases + justificación explícita frente a single-pass.

## Cuándo usarla

- La tarea requiere consumir más unidades de las que caben con calidad en una sola ventana de atención (decenas de archivos, cientos de registros). [INFERENCIA]
- Las unidades son procesables de forma independiente y solo se integran al final (map → reduce). [INFERENCIA]
- Necesitas paralelizar el pase local y aislar fallos por unidad sin abortar todo el lote. [INFERENCIA]
- El resultado final depende de una síntesis sobre resúmenes, no de cada byte crudo. [INFERENCIA]

## Cuándo NO usarla (anti-scope)

- **Single-pass cabe holgado** y razona mejor con el contexto completo: el chaining añade overhead de schemas y debe justificarse (eval `single_pass_fits`). [INFERENCIA]
- **Las unidades no son independientes**: si la unidad N necesita el crudo de la unidad M para procesarse, el patrón map→reduce no aplica; busca otra descomposición. [SUPUESTO]
- **La tarea no es de procesamiento por lote** (p. ej. redactar un correo): no activar (eval `false_positive_unrelated`). [DOC]
- **Se exige meter crudos en el pase 2 o saltarse schemas**: Guardian bloquea, no es un atajo aceptable (evals `raws_in_integration_rejected`, `global_exception_rejected`). [DOC]

## Cómo construir

1. **Delimita la unidad atómica.** Define qué es "una unidad" del pase local (un archivo, un commit, un documento). El pase local nunca debe ver más de una unidad por invocación.
2. **Define el schema de salida del pase local.** Tipa el resumen que cada unidad produce: campos obligatorios, tipos, y un campo de estado (`ok` / `error`) con detalle del fallo. Sin schema no hay cadena, hay pegamento.
3. **Define el schema de transición.** Especifica el contrato que el pase de integración recibe: una colección tipada de resúmenes. El pase 2 jamás recibe los crudos.
4. **Implementa el pase local idempotente y aislado.** Cada unidad se procesa sin depender de otra; el error de una unidad se tipa y se propaga como dato, no como excepción que tumba el lote.
5. **Implementa el pase de integración sobre resúmenes.** Sintetiza, agrega o decide leyendo solo la colección tipada. Si necesita un crudo, eso indica que el schema del pase local está incompleto: corrígelo, no abras un atajo.
6. **Justifica vs single-pass.** Documenta por qué el chaining gana (volumen, paralelismo, aislamiento de error). Si no hay ganancia medible, colapsa a single-pass.

## Decisiones y trade-offs

- **Resumen sobre crudo en el pase 2.** Se gana acotamiento de atención y costo lineal; se paga el riesgo de que el resumen pierda señal. Mitigación: si el pase 2 "necesita un crudo", el schema local está incompleto — enriquécelo, no abras un atajo. [INFERENCIA]
- **Error tipado como dato vs excepción global.** El error por unidad viaja en el schema (`status="error"`) para que un fallo aislado no tumbe el lote ni contamine la síntesis; cuesta disciplina de tipado en cada pase local. [INFERENCIA]
- **Chaining vs single-pass.** El chaining añade overhead de schemas y orquestación; solo gana con volumen alto, paralelismo real o necesidad de aislar fallos. Por debajo de ese umbral, single-pass razona mejor. [INFERENCIA]

## Patrón correcto

```python
# GOOD: pase local tipado por unidad + integración solo sobre resúmenes.
from pydantic import BaseModel
from typing import Literal

class UnitSummary(BaseModel):
    unit_id: str
    status: Literal["ok", "error"]
    findings: list[str] = []
    error_detail: str | None = None

def local_pass(unit: SourceFile) -> UnitSummary:
    # Ve UNA sola unidad. El fallo se tipa, no se lanza.
    try:
        findings = analyze(unit.content)
        return UnitSummary(unit_id=unit.id, status="ok", findings=findings)
    except AnalysisError as exc:
        return UnitSummary(unit_id=unit.id, status="error", error_detail=str(exc))

# Schema de transición: colección tipada de resúmenes (nunca crudos).
summaries: list[UnitSummary] = [local_pass(u) for u in units]  # paralelizable

def integration_pass(summaries: list[UnitSummary]) -> Report:
    ok = [s for s in summaries if s.status == "ok"]
    failed = [s for s in summaries if s.status == "error"]
    # El pase 2 razona SOLO sobre resúmenes tipados.
    return synthesize(ok, failures=failed)
```

## Anti-patrón

```python
# ANTI: mega-prompt que concatena todos los crudos en una sola pasada.
# Satura la atención, no paraleliza, y un fallo en un archivo contamina todo.
blob = "\n\n".join(read(f) for f in fifty_files)   # 50 archivos crudos juntos
result = model(f"Analiza todo esto y dame el reporte:\n{blob}")
# Sin schema por pase, sin estado de error por unidad, sin transición tipada.
```

## Checklist de validación

- ¿El pase de integración nunca ve los datos crudos, solo resúmenes?
- ¿Cada pase tiene un schema de salida explícito y tipado?
- ¿El estado de error está tipado por unidad (no una excepción global)?
- ¿El pase local procesa una sola unidad y es paralelizable e idempotente?
- ¿Existe un schema de transición que define qué viaja entre pases?
- ¿Se justifica el chaining frente a un single-pass (volumen / paralelismo / aislamiento)?

Cualquier "no" es bloqueante: corrige el diseño antes de entregar, no lo marques completo. [DOC]

## Edge cases y auto-corrección

- **El pase 2 pide un crudo** → señal de schema local incompleto. Añade el campo al resumen; nunca pases el crudo. [INFERENCIA]
- **Una unidad falla** → tipa el error (`status="error"`, `error_detail`) y continúa; el pase 2 reporta los fallos sin abortar (eval `error_isolation`). [DOC]
- **Unidades con dependencia oculta** → el map→reduce no aplica; rediseña o degrada a single-pass. [SUPUESTO]
- **Schema de transición ausente o implícito** → no hay cadena, hay pegamento; defínelo antes de implementar. [INFERENCIA]
- **Upgrade de la skill** → completa solo los archivos faltantes; no sobrescribas ediciones locales ni toques otras skills (eval `upgrade_safety_case`). [DOC]
- **Input vacío o lote indefinido** → `{VACIO_CRITICO}`: para y pide, no auto-completes el lote (eval `empty_input`). [DOC]

## Assets y validación offline

- `assets/` define el contrato determinístico para justificación vs single-pass, unidad atómica, schema local, schema de transición, integración sobre resúmenes y errores tipados. [CÓDIGO]
- `scripts/check.sh` valida fixtures locales sin red, tiempo real ni aleatoriedad. [CÓDIGO]
- `scripts/validate_prompt_chaining_design.py` rechaza diseños donde el pase de integración consume crudos, falta schema, el pase local procesa varias unidades, no hay error tipado o Guardian aprueba un diseño bloqueado. [CÓDIGO]

## Katas y skills relacionadas

- `katas-multipass-prompt-chaining`
- `workflow-forge`
- `output-engineering`
