# Variación rápida — context-window-engineering

Para un diagnóstico exprés cuando el usuario solo quiere saber qué mover y dónde.

## Tarea

Dado el orden actual de bloques del contexto y qué cambia por-turno, devuelve en ≤6 líneas:

1. Qué bloques son prefijo estático (van primero, byte-idéntico).
2. Qué valor por-turno está filtrado al prefijo y rompe el cache (si lo hay).
3. Dónde reubicar ese estado volátil (bloque `<reminder>` final).
4. Qué regla crítica mover a los bordes (inicio + reafirmación al final).
5. Umbral de compactación sugerido (default >55%).
6. Las dos mediciones a correr: cache-hit rate y prueba de retención.

## Reglas

- No prometas factor de ahorro sin medir.
- Si no hay reuso de prefijo o el proveedor no cachea, dilo y detente.
- Tags de evidencia en cada punto.
