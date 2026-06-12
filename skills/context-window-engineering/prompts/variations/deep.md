# Variación profunda — context-window-engineering

Para un rediseño completo del context assembler con artefactos reproducibles y validación medida.

## Alcance

Cubre el ciclo entero: del estado actual al ensamblado verificado, incluyendo casos borde y el paquete determinístico.

## Procedimiento extendido

1. **Inventario de bloques.** Tabula cada bloque: contenido, ¿cambia por-turno?, tamaño aproximado, ¿contiene regla crítica?
2. **Partición estático/dinámico** con justificación por bloque (incluye tool definitions y few-shot: ¿estables en la sesión?).
3. **Diseño del prefijo byte-idéntico.** Define orden canónico y normalización de whitespace. Audita con `grep timestamp|now|request_id|uuid|counter`.
4. **Edge placement.** Identifica las reglas irrenunciables vs el resto; reafirma solo las irrenunciables al cierre para no sobre-rellenar el borde y volver a diluir.
5. **Política de compactación.** Umbral fijo (>55% o justificado), algoritmo (resumir intermedio), garantía explícita de no tocar bordes. Decide compactar vs truncar con su trade-off.
6. **Casos borde.** Resuelve: tool defs que cambian por sesión, few-shot largos, una vs muchas reglas críticas, proveedor sin caching.
7. **Paquete determinístico.** Declara `assets/context-assembly-schema.json` y `assets/context-policy.json`; corre `compile-context-window.py` y `check.sh`.
8. **Validación medida.** Reporta cache-hit rate y resultado de la prueba de retención. Sin ambas, no cierres.

## Entregable

`templates/output.md` completo + reporte del compilador + decisiones y trade-offs con tags de evidencia. Veredicto del guardian: PASA/RECHAZA con checks.
