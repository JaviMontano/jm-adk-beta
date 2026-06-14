# qbr-quarterly (P13)

Cadencia de cierre trimestral para Jarvis OS: en una sola pasada auditable mira
atras (que se cumplio vs. lo prometido contra los OKRs) y mira adelante
(compromisos del proximo Q), con cada dato ligado a evidencia tagueada.

## Que hace

Convierte un trimestre cerrado + su baseline de OKRs en cuatro entregables
trazables: **scorecard** del Q cerrado (estado por OKR con metrica observada vs.
objetivo), **lecciones** con causa raiz, **plan del proximo Q** (3-5 objetivos
medibles con owner) y **riesgos/dependencias cross-quarter**.

## Cuando usarla

- Cierre del Q activo o arranque del siguiente; el usuario pide "QBR", "repaso
  trimestral" o nombra P13.
- Existe un trimestre con OKRs/metas definidos al inicio que ahora se cierran.

**No usar** para standups o repasos semanales (cadencia equivocada), planeacion
anual completa (mayor alcance), ni un trimestre sin baseline — sin metas base no
hay auditoria, solo planeacion: dilo y degrada el alcance.

## Como ejecuta

Procedimiento de cinco fases (ver `SKILL.md`): **Discover** (localiza baseline +
evidencia; sin baseline es `{VACIO_CRITICO}` terminal) → **Audit** (estado por
meta, observado vs. objetivo, fuente tagueada) → **Learn** (lecciones a causa
raiz) → **Plan** (3-5 objetivos del proximo Q ligados a lecciones) → **Validate**
(corre el Acceptance Gate antes de entregar).

## Como rutea los roles

| Rol | Archivo | Responsabilidad |
|---|---|---|
| Lead | `agents/lead.md` | Orquesta las cinco fases y resuelve inputs/baseline |
| Specialist | `agents/specialist.md` | Criterio de estado, causa raiz y diseno de objetivos |
| Support | `agents/support.md` | Lectura, ensamblado de evidencia y persistencia aditiva |
| Guardian | `agents/guardian.md` | Acceptance Gate y veredicto sobre evidencia/tags |

## Referencias

- `references/verification-tags.md` — familia de tags Jarvis OS `{...}` y su mapeo al gate.
- `knowledge/body-of-knowledge.md` — conceptos, estandares y reglas de decision del QBR.
- `knowledge/knowledge-graph.json` — grafo de conceptos clave de la cadencia.
- `templates/output.md` — scaffold del entregable QBR.
- `prompts/` — prompts primario, meta y variaciones quick/deep.
- `assets/` — rubrica de calidad y checklist del gate (ver `assets/README.md`).

## Gobernanza

Evidencia tagueada con **una sola familia** (`{...}`), sin precios inventados,
verde nunca como exito automatico, sin PII de cliente, marca unica por documento.
