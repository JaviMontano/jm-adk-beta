# Assets — monthly-audit

Bundle de soporte para la cadencia P22. Estos assets son datos/checklists
deterministas que las fases del skill consumen; no son prosa de relleno.

## Contenido

- **`quality-rubric.json`** — la rubrica P22 en forma estructurada: escala 0-3,
  los 6 ejes con su pregunta nuclear, reglas de puntuacion, valores de delta y la
  restriccion del Top 3. Consumida por `SKILL.md` (rubrica) y los prompts al
  puntuar cada eje.
- **`gate-checklist.md`** — checklist de aceptacion que ejecuta el guardian en la
  fase Validate. Espeja el "Validation gate" de `SKILL.md`.

## Manifiesto

`manifest.json` declara cada asset con su `type`, `purpose` y `used_by`. Todo
`used_by` apunta a un archivo existente del skill.

## Reglas

- Assets de soporte: **missing-only** por defecto; `--force` solo tras revisar diff.
- Mantener `quality-rubric.json` en sincronia con la rubrica de `SKILL.md`: si
  cambia un eje o la escala, actualiza ambos.
