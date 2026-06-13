# Assets — wbr-weekly-review

Bundle de activos que respaldan el gate de aceptacion del acta WBR. Cada archivo
esta declarado en `manifest.json` con su consumidor (`used_by`).

## Contenido

- **`quality-rubric.json`** — rubrica por dimension (estructura, estancado
  accionable, cumplimiento honesto, friccion clasificada, compromisos acotados,
  arrastres escalados, evidencia ligada, una sola familia de tags) en escala
  fail / partial / pass. La consumen `SKILL.md`, `agents/guardian.md` y
  `prompts/meta.md` para puntuar un acta.
- **`gate-checklist.md`** — checklist operativo que el guardian recorre item por
  item antes de declarar el acta hecha. La consumen `agents/guardian.md` y el
  `README.md` del skill.

## Como se usa

El guardian carga la rubrica y el checklist al correr el gate; si alguna dimension
queda en `fail` o un item del checklist sin marcar, el acta se bloquea con la falla
concreta. No hay aprobacion parcial. {DOC}
