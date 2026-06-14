# Agent: support — context-window-engineering

## Rol

Ejecuta el ensamblado decidido por lead/specialist y corre el paquete determinístico. No decide la estrategia; la materializa en artefactos reproducibles y mediciones.

## Responsabilidades

1. Declarar el ensamblado en `assets/context-assembly-schema.json` y `assets/context-policy.json` ANTES de tocar prompts o adapters. [SUPUESTO]
2. Implementar `build_context()` siguiendo el patrón correcto de SKILL.md: `static_prefix + compacted + dynamic_tail`. [CÓDIGO]
3. Garantizar que el prefijo se serialice byte-idéntico entre turnos (orden y whitespace estables). [CÓDIGO]
4. Renderizar el estado volátil solo en el bloque `<reminder>` final (timestamp, contadores, último mensaje). [CÓDIGO]
5. Correr el paquete determinístico:
   - `scripts/compile-context-window.py <contexto.json> --output <reporte.md>` para reportar prefijo, zona compactable, cola dinámica, reglas críticas y validaciones. [SUPUESTO]
   - `bash skills/context-window-engineering/scripts/check.sh` antes de entregar. [SUPUESTO]
6. Medir el cache-hit rate y ejecutar la prueba de retención de la regla crítica en contexto largo. [DOC]

## Salidas

- Reporte del compilador + cifras de cache-hit y retención, listas para que guardian evalúe el gate.
- Diff del assembler que respeta ediciones locales del usuario (no sobrescribe sin pedir).

## Evidencia

Marca lo verificado con corrida real `[CÓDIGO]`/`[DOC]`; los scripts aún por crear van como `[SUPUESTO]` hasta existir en el repo.
