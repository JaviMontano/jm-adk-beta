# Assets — context-window-engineering

Bundle de artefactos que materializan el ensamblado de la ventana de contexto y su validación. Todos son específicos de esta skill: declaran el prefijo cacheable, el edge placement y la política de compactación.

## Contenido

| Asset | Tipo | Para qué sirve | Usado por |
|---|---|---|---|
| `context-assembly-schema.json` | json-schema | Declara el ensamblado (bloques, zonas, compactación) antes de escribir prompts/adapters. Validable contra un `contexto.json`. | `SKILL.md` |
| `context-policy.json` | config | Política dura del ensamblado: tokens prohibidos en el prefijo, cola dinámica final, edge placement, umbral de compactación, reglas de rechazo. | `SKILL.md` |
| `quality-rubric.json` | rubric | Criterios de calidad y señales de fallo que aplica el guardian en el gate. | `agents/guardian.md` |
| `checklist.md` | checklist | Verificación operativa previa a marcar la skill como aplicada. | `agents/support.md` |

## Cómo se usan

1. `support` declara el ensamblado rellenando `context-assembly-schema.json` y fija las reglas con `context-policy.json`.
2. El paquete determinístico (`compile-context-window.py`) valida el contexto contra el schema y la policy; rechaza timestamps en prefijo, reglas críticas solo en el centro, falta de compactación, dynamic tail no final y compactación que toca bordes.
3. `guardian` aplica `quality-rubric.json` y `checklist.md` para el veredicto PASA/RECHAZA.

## Gobernanza

Evidencia con tags. Sin precios. Nunca verde sin cache-hit + retención medidos.
