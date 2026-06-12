# Ejemplo de entrada — context-window-engineering

## Escenario

Un agente de soporte en producción reensambla su contexto en cada turno así (orden actual):

```python
def build_context(turn_state, history):
    return [
        Block("header", f"Current time: {turn_state.timestamp}"),  # primera linea
        Block("role", ROLE_AND_TOOLS),
        Block("history", history),                                 # crece sin limite
        Block("rules", "Nunca cierres un ticket sin confirmacion del usuario."),
    ]
```

## Síntomas reportados

- El cache-hit rate del proveedor (que sí soporta prefix caching) es casi cero y la latencia por turno no baja.
- En conversaciones largas el agente cierra tickets sin pedir confirmación: la regla crítica deja de respetarse.
- El historial crece hasta acercarse al límite de ventana y no hay política de compactación.

## Datos del entorno

- Proveedor con prefix caching: sí.
- Límite de ventana objetivo: 200k tokens.
- Cambia por-turno: `turn_state.timestamp` y el último mensaje del historial.
- Regla irrenunciable: "Nunca cierres un ticket sin confirmación del usuario."

## Petición

Rediseña el ensamblado del contexto para habilitar el reuso de prefijo, proteger la regla crítica de la dilución y fijar una política de compactación, sin sobrescribir el resto del assembler.
