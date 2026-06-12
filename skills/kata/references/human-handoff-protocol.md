<!-- distilled from alfa skills/katas-human-handoff-protocol -->
<!-- Handoff a humano con payload tipado autocontenido (customer_id, issue_summary, actions_taken); end-state del bucle, no pausa. -->
# Katas Human Handoff Protocol

## Qué es

Cuando el agente toca una política que no puede resolver por sí mismo (un límite excedido, una decisión irreversible o un conflicto de datos), invoca la tool `escalate_to_human`, suspende la generación de prosa y emite un payload JSON estricto y autocontenido. El payload contiene exactamente los campos que el operador humano necesita para decidir sin leer la conversación: `customer_id`, `issue_summary`, `actions_taken`, `escalation_reason`, `recommended_action`.

El handoff es un **end-state del bucle**, no una pausa: el agente no continúa generando ni avanza hasta que el humano resuelve.

**Anti-scope.** Este kata cubre el *contrato* del handoff (cuándo escalar, qué payload emitir, cómo cerrar el bucle). NO cubre: el enrutamiento del caso a una cola humana, la UI del operador, SLAs de resolución, ni el retorno del humano al agente (re-entry) — son responsabilidad del sistema de tickets aguas abajo. [SUPUESTO]

**Supuestos del contrato.** Existe una tool `escalate_to_human` registrada cuya invocación el runtime trata como terminal; los cinco campos del payload están definidos en el esquema de la tool y son obligatorios; el operador tiene acceso a los sistemas que `recommended_action` referencia. Si alguno no se cumple, el handoff degrada a transcript crudo — la falla que este kata evita. [SUPUESTO]

## Por qué importa (falla que evita)

Pasar al humano un transcript crudo es un desastre operacional: el operador tiene que leer toda la conversación, adivinar el contexto y decidir bajo presión. Un payload tipado y autocontenido reduce el tiempo de resolución y elimina la ambigüedad. El operador recibe un caso listo para actuar, no una conversación que descifrar.

## Modelo mental

- **Detectar la precondición de escalada**: límite excedido, irreversibilidad o conflicto de datos.
- Al cumplirse, llamar la tool `escalate_to_human` y **cortar la generación de texto**.
- El payload es **autocontenido**: el humano NO debe necesitar leer la conversación previa para decidir.
- Es un **end-state del bucle, no una pausa**: el agente no continúa hasta que el humano resuelve.
- El payload es **tipado**: campos fijos (`customer_id`, `issue_summary`, `actions_taken`, `escalation_reason`, `recommended_action`), no prosa libre.

## Patrón correcto

```python
if refund_amount > tier2_limit:
    return tool_call('escalate_to_human', {
        'customer_id': customer_id,
        'issue_summary': issue_summary,
        'actions_taken': actions_taken,
        'escalation_reason': escalation_reason,
        'recommended_action': recommended_action,
    })
```

La llamada a la tool corta la generación: el agente no añade prosa después.

**Decisión: campos fijos vs payload abierto.** Se elige un esquema cerrado de cinco campos en lugar de un dict libre. Trade-off: pierde flexibilidad para casos atípicos, pero gana validación en el límite de la tool (un campo faltante falla rápido y visible) y un caso uniforme que el operador lee sin reaprender el formato. La flexibilidad perdida se recupera dejando `recommended_action` como texto libre dentro del esquema, no abriendo el esquema. [INFERENCIA]

**Edge cases.**
- *Datos incompletos para llenar el payload* (p.ej. falta `customer_id`): no inventar ni dejar el campo vacío silenciosamente — escalar marcando el hueco como crítico, porque un payload con un campo fabricado es peor que uno que declara su laguna. [INFERENCIA]
- *Escalada a mitad de streaming*: si ya se emitió prosa parcial, la llamada a la tool debe seguir cerrando el bucle; el hook que termina la sesión es la red de seguridad, no la prosa previa. [SUPUESTO]
- *Doble disparo* (dos precondiciones se cumplen en el mismo turno): un solo `escalate_to_human`, con el `escalation_reason` que mejor describa el bloqueo; no encadenar escaladas. [INFERENCIA]

## Anti-patrón

```python
return 'Lo siento, ese reembolso supera mi límite. Voy a hablar con mi supervisor...'
# ...y sigue generando prosa, sin payload tipado, sin terminar el bucle
```

Devolver prosa tranquilizadora y continuar la conversación deja al operador sin un caso accionable y mantiene el bucle abierto cuando debía terminar.

**Otros modos de falla** (más allá de la prosa que no termina):
- *Payload-shaped pero sin tool call*: emitir el JSON como texto en la respuesta. No cierra el bucle ni dispara el hook; el caso nunca llega a la cola. [INFERENCIA]
- *Transcript embebido en `issue_summary`*: volcar la conversación entera en un campo derrota el objetivo autocontenido — el campo es un resumen tipado, no un dump. [INFERENCIA]
- *Escalar sin precondición real* (sobre-escalada): convierte el handoff en ruido y entrena al operador a ignorarlo; escalar solo ante límite, irreversibilidad o conflicto. [SUPUESTO]

## Argumento de certificación

- Enumerar las **precondiciones de escalada**: límite excedido, irreversibilidad, conflicto de datos.
- La **salida del handoff es tipada y autocontenida**: campos fijos, sin necesidad de leer la conversación previa.
- El handoff es **end-state, no pausa**: un hook `PostToolUse` puede terminar la sesión tras `escalate_to_human`.
- Conecta con `katas-hook-driven-policy-enforcement` (un hook puede forzar `ask_human`) y con `katas-numeric-cross-validation` (un mismatch numérico dispara el handoff).

## Criterios de aceptación

Un handoff pasa certificación si y solo si:
- Se dispara **solo** ante una de las tres precondiciones (límite, irreversibilidad, conflicto), nunca por defecto. [DOC]
- Emite **una** llamada a `escalate_to_human` con los cinco campos presentes y no vacíos; un campo faltante hace fallar la tool, no degrada a default silencioso. [INFERENCIA]
- **No** hay tokens de prosa después de la llamada a la tool en el mismo turno. [DOC]
- El payload es legible sin la conversación: dado solo el JSON, un operador decide. (Prueba: tapar el transcript y verificar que la decisión sigue siendo posible.) [INFERENCIA]
- Un hook `PostToolUse` cierra la sesión tras `escalate_to_human` — el end-state no depende de que el modelo "se detenga" voluntariamente. [SUPUESTO]

## Cuándo activar

- El agente alcanza un límite de política que no puede resolver (p.ej. reembolso sobre el tope de su tier).
- La acción solicitada es irreversible y requiere aprobación humana.
- Hay un conflicto de datos que el agente no puede arbitrar.
- Se necesita diseñar el contrato del payload de escalada o el hook que cierra la sesión.

## Skills relacionadas

- `katas-hook-driven-policy-enforcement`
- `katas-numeric-cross-validation`
- `katas-mcp-structured-errors`
