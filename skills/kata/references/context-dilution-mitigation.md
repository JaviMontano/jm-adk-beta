<!-- distilled from alfa skills/katas-context-dilution-mitigation -->
<!-- Mitigacion de dilucion softmax: edge placement de reglas criticas y compactacion al cruzar 50-60 por ciento de contexto. -->
# Katas Context Dilution Mitigation

## Qué es

La curva de atención del transformer tiene forma de U: los bordes del prompt (inicio y fin) reciben atención alta, el centro se diluye — el fenómeno "lost in the middle". [DOC] Esta kata establece dos disciplinas complementarias: colocar reglas críticas en los bordes (edge placement) y compactar el historial antes de que esas reglas queden sepultadas en el valle de atención (cuando `usage_fraction(history) > 0.55`). [CONFIG]

## Por qué importa (falla que evita)

Un agente puede seguir una política al turno 5 y violarla al turno 30 sin haberla olvidado: dejó de atenderla porque la regla quedó en el medio del contexto. [INFERENCIA] La pérdida es silenciosa — no aparece en logs ni errores, solo en comportamiento degradado. En seguridad o compliance, una violación silenciosa de "nunca exponer PII" es indistinguible de un sistema correcto hasta que el daño ya ocurrió. [INFERENCIA]

## Modelo mental

- Bordes (inicio/fin) = atención alta. Centro = atención baja. Es la curva en U. [DOC]
- Reglas críticas (seguridad, compliance, invariantes) van al inicio Y se repiten al final como `<reminder>`. La doble colocación cubre ambas zonas de atención alta. [INFERENCIA]
- Los datos ricos y voluminosos van al centro, donde la atención baja importa menos. [INFERENCIA]
- Si `usage_fraction(history) > 0.55`, compactar: reescribir denso preservando reglas, decisiones y escaladas. Compactar es condensar, no borrar. [CONFIG]
- El umbral 50-60% balancea conservar contexto útil contra evitar que las reglas se hundan en el valle. [SUPUESTO] Verificar por dominio midiendo la tasa de violación silenciosa antes/después de mover el umbral.

## Supuestos y límites (anti-scope)

- Aplica a modelos con atención degradada en el centro; en modelos sin sesgo de posición medible la kata es inerte (no daña, pero no aporta). [SUPUESTO] Confirmar con un probe posicional antes de invertir esfuerzo.
- El umbral 0.55 es un default, no una constante universal: tareas con reglas muy numerosas pueden requerir compactar antes (0.45). [SUPUESTO]
- NO sustituye guardrails determinísticos (validación de salida, filtros de PII). Edge placement reduce probabilidad, no garantiza cumplimiento. [INFERENCIA]
- NO cubre dilución por contexto irrelevante recuperado (RAG ruidoso): eso es problema de retrieval, no de posición. [INFERENCIA]
- La repetición de reglas consume tokens; en prompts cortos (< ~2k tokens) el centro no es un valle real y el `<reminder>` final es overhead innecesario. [SUPUESTO]

## Activos determinísticos

Usa `assets/manifest.json` como índice de contratos offline. Los assets fijan la curva de atención, edge placement, umbral 50-60%, preservación de reglas/decisiones/escaladas y contrato JSON de salida. Si produces un reporte JSON de mitigación, valídalo con `bash skills/katas-context-dilution-mitigation/scripts/check.sh` antes de marcarlo como aceptado. [CONFIG]

## Patrón correcto

```python
SYSTEM:<rules>critical_policy</rules>
...
USER:question
...
REMINDER:<rules>critical_policy</rules>

if usage_fraction(history) > 0.55:
    history = compact(history, preserve=['rules', 'decisions', 'escalations'])
```

## Anti-patrón

```python
system_prompt = f"You are an assistant.\n{big_blob_of_context}\nIMPORTANT: never expose PII.\n...3000 more tokens..."
# La regla crítica queda enterrada en el valle de la U: alta probabilidad de violación silenciosa.
```

## Modos de falla (qué vigilar)

- **Reminder a la deriva**: el `<reminder>` final deja de ser el último bloque porque se appendió output después; vuelve al valle. Mantén el reminder como el sufijo invariante de cada turno. [INFERENCIA]
- **Compactación lossy**: `compact()` resume y descarta una escalada o decisión. La whitelist `preserve` es el contrato; toda compactación debe ser auditable contra ella. [INFERENCIA]
- **Deriva entre copias**: la regla del inicio y la del reminder divergen tras una edición. Deben derivar de una sola fuente, no copiarse a mano. [SUPUESTO]
- **Umbral nunca alcanzado**: historiales que crecen lento bajo el 0.55 jamás compactan y acumulan ruido; añade un disparador secundario por nº de turnos. [INFERENCIA]

## Casos límite

- Reglas que exceden el presupuesto de bordes: prioriza por severidad (PII/seguridad primero); las de menor criticidad pueden ir solo al inicio. [SUPUESTO]
- Multi-regla con conflictos: el reminder repite el conjunto resuelto, no las reglas crudas, para no reintroducir ambigüedad. [INFERENCIA]
- Ventanas con prompt caching: mover los bordes invalida el caché; ancla el prefijo estable y limita la repetición al sufijo. [SUPUESTO] Medir el coste de cache-miss antes de adoptar.

## Argumento de certificación

- Describir la curva en U de atención y el efecto "lost in the middle". [DOC]
- Enunciar la regla: bordes para reglas críticas, centro para datos. [DOC]
- Fijar un umbral concreto de compactación (50-60%) y justificar el balance entre conservar contexto y evitar dilución. [CONFIG]
- Explicar que compactar preserva reglas, decisiones y escaladas, no las elimina. [DOC]
- Validar el contrato offline con `scripts/check.sh` cuando el output sea JSON. [CONFIG]

## Criterios de aceptación

- La regla crítica aparece textualmente en el inicio Y en el sufijo del prompt, derivada de una sola fuente. [DOC]
- Existe un disparador de compactación explícito (por fracción y/o por turnos) y la whitelist `preserve` está declarada. [CONFIG]
- Tras compactar, toda regla/decisión/escalada previa sigue presente — verificable por diff contra `preserve`. [INFERENCIA]
- Reporte JSON (si existe) pasa `scripts/check.sh` sin errores. [CONFIG]
- Cada `[SUPUESTO]` de este diseño tiene un paso de verificación asociado. [DOC]

## Cuándo activar

- Diseño de system prompts o agentes con políticas de seguridad/compliance que deben sostenerse en conversaciones largas.
- Agentes multi-turno donde el historial crece y las reglas iniciales corren riesgo de diluirse.
- Cuando se observa que un agente respeta una política temprano pero la viola en turnos posteriores.
- Diseño de estrategias de compactación de contexto.

## Skills relacionadas

- `katas-multipass-prompt-chaining`
- `katas-persistent-scratchpad`
- `katas-provenance-preservation`
