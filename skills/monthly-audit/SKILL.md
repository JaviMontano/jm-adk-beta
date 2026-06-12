---
name: monthly-audit
version: 0.2.0
description: "Auditoria mensual de salud del jarvis: rubrica de 6 preguntas (P22) que puntua, evidencia y prioriza acciones."
owner: "JM Labs"
triggers:
  - monthly-audit
  - auditoria-mensual
  - health-check
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# Monthly Audit

Cadencia P22 de salud mensual del jarvis. Pasa el sistema por una **rubrica de 6
preguntas**, puntua cada eje con evidencia, y deja una lista corta de acciones
priorizadas para el mes siguiente. Operador-facing: usa la familia de tags
Jarvis OS `{...}` (ver `references/verification-tags.md`). {MEMORIA}

## When to use

- Trigger explicito `monthly-audit` / `auditoria-mensual` / `health-check`, o al
  cierre de mes de un workspace en operacion. {EXTRAIDO_HILO}
- NO usar para: cierre diario (eso es `daily-close` P10), retro de un proyecto
  puntual, o revision de una sola tarea — la auditoria mira el sistema, no el
  dia. {INFERENCIA}

## Inputs

| Input | Obligatorio | Si falta |
|---|---|---|
| Mes auditado + workspace activo | si | autocompleta mes en curso `{AUTOCOMPLETADO}`, marca la suposicion |
| Fuentes de evidencia (MEMORY.md, TAREAS.md, bitacora, commits) | si | `{VACIO_CRITICO}`: pregunta que auditar antes de puntuar de memoria |
| Auditoria del mes previo (para delta) | no | primera corrida: sin baseline, marca scores como `{POR_CONFIRMAR}` |
| Destino donde persistir el informe | si | usa la bitacora del workspace activo |

## Outputs

- **Scorecard P22**: las 6 preguntas, cada una con score 0-3 y evidencia ligada.
- **Delta vs mes previo** por eje (mejora / estable / regresion), si hay baseline.
- **Top 3 acciones** priorizadas por riesgo x impacto, con primer paso ejecutable.
- **Notas de evidencia** con tags Jarvis OS en toda afirmacion no obvia.
- **Estado de validacion** y riesgos sistemicos abiertos que cruzan al mes siguiente.

## Rubrica P22 (6 preguntas)

Puntua cada eje **0-3**: 0 ausente · 1 fragil · 2 funcional · 3 solido. Todo
score debe colgar de evidencia citable, no de impresion. {INFERENCIA}

1. **Memoria** — ¿MEMORY/bitacora refleja el estado real y es recuperable en frio?
2. **Cadencias** — ¿daily-close y demas ritmos se ejecutaron con la frecuencia esperada?
3. **Tareas** — ¿el backlog esta vivo (sin huerfanos ni stale silenciosos) y priorizado?
4. **Estructura/AI** — ¿arquitectura de informacion, skills y rutas siguen coherentes?
5. **Guardrails** — ¿disciplina de marca, evidencia y update-safety se respetaron?
6. **Friccion/Deuda** — ¿que fricciones recurrentes o deuda se acumularon sin atender?

## Procedure

### 1. Discover
Lee las fuentes de evidencia y la auditoria del mes previo **antes** de puntuar.
Read-before-write obligatorio. {MEMORIA} Fija mes y workspace; si no son
explicitos, autocompleta y marca `{AUTOCOMPLETADO}`.

### 2. Score
Recorre las 6 preguntas en orden. Para cada una asigna **0-3** y liga la
evidencia concreta (archivo, commit, entrada de bitacora) que justifica el
numero. Un score sin evidencia es `{POR_CONFIRMAR}`, no un hecho. {EXTRAIDO_HILO}

### 3. Delta
Compara cada eje contra el mes previo: mejora / estable / regresion. Sin baseline
(primera corrida) marca el delta como n/a y los scores como `{POR_CONFIRMAR}`.

### 4. Prioritize
De los ejes 0-1 y las regresiones, deriva **maximo 3 acciones**, ordenadas por
riesgo x impacto, cada una con primer paso ejecutable en frio. Mas de 3 no es un
plan, es una lista de deseos. {INFERENCIA}

### 5. Persist
Aplica el informe de forma **aditiva** (append) a la bitacora destino con
Write/Edit. Nunca sobrescribas historico ni ediciones locales sin `--force` tras
revisar el diff. {SUPUESTO}

### 6. Validate
Corre el gate de aceptacion antes de declarar la auditoria cerrada.

## Validation gate (acceptance criteria)

- [ ] Las 6 preguntas puntuadas 0-3; ninguna omitida ni dejada en blanco. {DOC}
- [ ] Cada score cuelga de evidencia ligada y verificable; los sin evidencia van `{POR_CONFIRMAR}`.
- [ ] Delta calculado vs mes previo, o marcado n/a explicito en primera corrida.
- [ ] Top 3 acciones (no mas), priorizadas, cada una con primer paso ejecutable.
- [ ] Toda afirmacion no obvia lleva exactamente un tag Jarvis OS; sin mezclar
      familias; `{WEB}` sin cita es invalido. {DOC}
- [ ] Persistencia aditiva; historico y ediciones locales intactos.

Si algun check falla, corrige y reevalua — no entregues una auditoria parcial.

## Self-correction triggers

- Score dudoso entre dos niveles → elige el **menor** (la salud se demuestra, no
  se asume) y anota la evidencia que subiria el numero. {INFERENCIA}
- Eje sin evidencia disponible → no inventes un 2 "razonable"; marca
  `{POR_CONFIRMAR}` con el paso que lo verificaria.
- Acciones > 3 → re-prioriza por riesgo x impacto; lo demas va a backlog, no al plan.
- Mes o fuente ausente → `{VACIO_CRITICO}`, detente y pregunta antes de puntuar.

## Edge cases

- **Primera auditoria (sin baseline)**: corre igual, marca deltas n/a y scores
  `{POR_CONFIRMAR}`; deja el scorecard como baseline del proximo mes.
- **Mes con poca actividad**: audita igual (mantiene la cadencia) y registra la
  baja actividad como hallazgo, no como hueco omitido.
- **Evidencia contradictoria** (MEMORY dice una cosa, commits otra): puntua por
  lo verificable en codigo/config y marca la discrepancia `{POR_CONFIRMAR}`.
- **Requisitos en conflicto** (p.ej. "audita pero ignora evidencia"): nombra el
  conflicto y elige la interpretacion segura — la evidencia no es opcional.
- **Multi-workspace**: una auditoria por workspace; no fusiones salud de marcas o
  proyectos distintos (disciplina de marca unica).

## Anti-patterns (anti-scope)

- Puntuar de impresion sin ligar evidencia (auditoria de sentimiento).
- Inflar scores para evitar el delta incomodo de una regresion.
- Derivar 10 acciones "para no olvidar" en vez de las 3 que mueven la aguja.
- Sobrescribir el historico de auditorias en vez de hacer append.
- Mezclar familias de tags Jarvis `{...}` y Alfa `[...]` en el mismo documento.
- Convertir P22 en cierre diario o retro de proyecto (es otra cadencia).

## Assumptions and limits

- No reemplaza revision experta para decisiones de alto riesgo (legal, medico,
  financiero, seguridad).
- Sin evidencia disponible, marca el eje como `{SUPUESTO}` o `{POR_CONFIRMAR}`
  con su paso de verificacion; nunca lo presentes como hecho.

## Related skills

- `daily-close` — cadencia P10 cuyo historico alimenta la evidencia mensual.
- `workspace-governance` — destino y disciplina de persistencia del informe.
- `quality-guardian` — refuerza el gate de validacion.

## Update-safety notes

- Bundle de soporte: `assets/` (rubrica P22 y checklist del gate, ver `assets/README.md`).
- Archivos de soporte generados: missing-only por defecto.
- `--force` solo tras revisar diffs; preserva ediciones locales.
