# Assets — frontload-prompt

Bundle de soporte para el gate y la calidad del bloque SPEC. Estos archivos son
consumidos por la skill al validar; no son entregables al usuario.

## Contenido

- **`checklist.md`** — checklist operable del Validation Gate. El guardian
  (`agents/guardian.md`) lo recorre antes de declarar READY; un solo fallo fuerza
  BLOCKED. Referenciado desde `SKILL.md`.
- **`quality-rubric.json`** — rúbrica ponderada (0/1/2) para puntuar un bloque
  SPEC en cinco criterios: completitud, Purpose accionable, disciplina de tags,
  honestidad de huecos y no-ejecución. Consumida por `SKILL.md` y por
  `agents/guardian.md` como umbral de READY.

## Cómo se usan

1. `support` ensambla el SPEC con `templates/output.md`.
2. `guardian` recorre `checklist.md` ítem por ítem.
3. Si se requiere puntuación (p. ej. comparar dos SPEC), se aplica
   `quality-rubric.json`; READY exige todos los criterios en 2 y cero
   `{VACIO_CRITICO}`.

## Manifest

`manifest.json` lista cada asset con su tipo, propósito y los archivos que lo
consumen. Todo `used_by` apunta a un archivo existente del skill.
