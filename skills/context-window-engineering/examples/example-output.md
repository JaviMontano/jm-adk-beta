# Ejemplo de salida — context-window-engineering

Plan de ensamblado para el agente de soporte del escenario de entrada.

## Diagnóstico

- El `Block("header", "Current time: {timestamp}")` está en la **primera línea**, así que el prefijo cambia cada turno y rompe el prefix cache por completo → cache-hit ~0. [DOC]
- La regla crítica está al **final, después de un historial creciente**: queda en zona de baja atención y se diluye en contextos largos. [DOC]
- No hay umbral de compactación → al crecer el historial, las reglas se diluyen aún más. [DOC]

## Rediseño (patrón correcto)

```python
def build_context(turn_state, history):
    static_prefix = [
        Block("role", ROLE_AND_TOOLS),                 # estable byte a byte -> cacheable
        Block("policies", "Nunca cierres un ticket sin confirmacion del usuario."),  # borde inicial
        Block("schema", OUTPUT_SCHEMA),
    ]
    compacted = compact_if_over(history, threshold=0.55)   # umbral fijo, no toca bordes
    dynamic_tail = [
        Block("reminder", render_reminder(
            now=turn_state.timestamp,                  # volatil -> SOLO aqui, al final
            critical="Recordatorio: nunca cierres un ticket sin confirmacion.",  # reafirma en borde final
        )),
    ]
    return static_prefix + compacted + dynamic_tail
```

## Cambios aplicados

| # | Cambio | Por qué | Evidencia |
|---|---|---|---|
| 1 | Saqué el timestamp del prefijo al bloque `<reminder>` final | Restaura la byte-identidad del prefijo → habilita prefix cache | [DOC] |
| 2 | Moví la regla crítica al borde inicial (en `policies`) y la reafirmé al final | Edge placement contra la curva en U | [DOC] |
| 3 | Añadí `compact_if_over(history, threshold=0.55)` | Política de compactación fija que no toca los bordes | [CONFIG] |

## Auditoría del prefijo

`grep -nE 'timestamp|now|request_id|uuid|counter'` sobre `static_prefix` → sin coincidencias. [CÓDIGO]

## Plan de medición

- **Cache-hit rate:** comparar antes/después con la API del proveedor; se espera pasar de ~0 a alto al estabilizar el prefijo (factor exacto a medir, no asumido). [DOC] [SUPUESTO]
- **Prueba de retención:** simular una sesión que llene >55% de la ventana y confirmar que el agente sigue pidiendo confirmación antes de cerrar. [DOC]

## Veredicto del gate

- [x] Prefijo byte-idéntico sin valor por-turno
- [x] Estado dinámico en `<reminder>` final
- [x] Regla crítica en ambos bordes
- [x] Umbral de compactación explícito (>55%) que no toca bordes
- [ ] Cache-hit rate y retención medidos → pendiente de ejecutar las dos pruebas

Resultado: **RECHAZA hasta medir** — el diseño es correcto pero el guardian no marca verde sin las dos mediciones. [DOC]
