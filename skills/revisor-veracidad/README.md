# revisor-veracidad

Audita un texto y devuelve el mismo contenido con un tag de procedencia inline por afirmacion no obvia, mas un plan de cierre para todo lo que hoy no es verificable. No genera contenido ni lo reescribe: solo lo audita y marca el riesgo. [DOC]

## Que hace

- Segmenta el texto en afirmaciones y separa los claims verificables de la estructura/opinion.
- Asigna a cada claim no obvio **exactamente un** tag de procedencia, de **una sola familia** (Jarvis OS para operador, Alfa core para kit/repo).
- Aplica la regla del tag mas debil: ante dos tags posibles, elige el menos cierto.
- Valida `{WEB}` (sin cita es invalido: degrada a `{CONOCIMIENTO}` o elimina).
- Empareja cada `{SUPUESTO}`/`{POR_CONFIRMAR}` con un paso de verificacion concreto.

## Cuando usar

- Antes de entregar texto cuyas afirmaciones podrian ser falsas, derivadas o asumidas (informes, specs, mensajes a cliente). [INFERENCIA]
- Cuando el orquestador exige tags de evidencia y hay que homologar un borrador sin ellos.
- Para convertir supuestos implicitos en `{POR_CONFIRMAR}` con accion de cierre.

**No usar para**: generar el contenido, validar codigo en ejecucion, ni reemplazar revision experta legal/medica/financiera/seguridad (ahi solo se marca el riesgo). [SUPUESTO]

## Como enruta y ejecuta

1. Detectar familia (por audiencia) y bloqueos (`{VACIO_CRITICO}` si no hay texto).
2. Segmentar en afirmaciones.
3. Asignar el tag mas debil aplicable, una sola familia.
4. Validar `{WEB}` (degradar o eliminar si no hay cita).
5. Generar plan de cierre por cada `{SUPUESTO}`/`{POR_CONFIRMAR}`.
6. Auto-chequear contra el gate antes de entregar.

La fuente canonica de tags es `references/verification-tags.md`; este skill la **aplica**, no la redefine. La homologacion es Jarvis -> Alfa, nunca al reves.

## Referencias

- `references/verification-tags.md` — taxonomia canonica, mapping y criterios de aceptacion.
- `SKILL.md` — contrato operativo, gate y self-correction triggers.
- `knowledge/body-of-knowledge.md` — conceptos, reglas de decision y estandares del dominio.
- `templates/output.md` — scaffold del entregable (texto tageado + plan + resumen).
- `prompts/` — prompts primario, meta y variaciones quick/deep.
- `assets/` — rubrica de calidad y checklist del gate (ver `assets/README.md`).
- `scripts/` — chequeos deterministas sobre fixtures (`scripts/check.sh`).

## Roles (agents/)

- `agents/lead.md` — orquesta el flujo de auditoria de extremo a extremo.
- `agents/specialist.md` — profundidad de dominio sobre la taxonomia de tags y la homologacion.
- `agents/support.md` — ejecucion: segmentacion, tageo y redaccion del plan.
- `agents/guardian.md` — gates de validacion antes de entregar.
