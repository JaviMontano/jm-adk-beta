---
name: official-source-verifier
version: 1.1.0
last_updated: 2026-06-11
description: "Verify a decision against official sources (ADK, Agent Skills spec, GitHub/Git, framework/SDK/API/cloud docs) before changing code, docs or architecture criteria; ranks official over secondary, cites URL+access date, records the change each finding justifies, and never elevates a secondary source to authority."
owner: "JM Labs (Javier Montaño)"
triggers:
  - official source
  - verify docs
  - adk spec
  - authoritative reference
  - source priority
allowed-tools:
  - Read
  - Grep
  - Glob
  - WebFetch
  - WebSearch
---

# Official Source Verifier

## Capacidad

Verifica decisiones técnicas contra fuentes oficiales antes de modificar código, documentación o criterios de arquitectura. Prioriza documentación oficial sobre blogs, issues, respuestas de foro, snippets o resúmenes generados. Una fuente secundaria puede usarse como pista de descubrimiento (ruta, vocabulario) pero nunca como autoridad. [DOC]

## Cuándo usarla

- Una decisión depende de documentación vigente de ADK, Agent Skills spec, GitHub/Git, frameworks, SDKs, APIs o servicios cloud.
- Una propuesta cita una fuente secundaria y hay que confirmar si una fuente oficial la respalda o la contradice.
- Un cambio de repo necesita registrar qué fuente oficial justifica el hallazgo.
- Hay contradicción entre fuentes y se requiere priorización explícita.

**No la uses** para hechos triviales del código local verificables con Read/Grep/Glob, ni para opiniones de diseño sin documento de autoridad detrás. Para esos casos no hay "fuente oficial" que consultar y el guardian no aporta valor. [INFERENCIA]

## Inputs / Outputs

- **Input mínimo**: la `question` (decisión concreta que depende de autoridad externa) y, si existe, la fuente secundaria que la disparó.
- **Output**: reporte con `source_registry`, `claims` (cada uno con estado `verified|unverified`), `decision` y `blocking_gaps`. JSON cuando el contrato lo exige; tabla legible cuando el consumidor es humano. [DOC]
- **Forma de fecha**: `accessed_date` en ISO `YYYY-MM-DD`; sin ella, el claim no puede pasar a `verified`. [CONFIG]

## Contrato determinístico

Usa los assets de `assets/` para certificar reportes:

- `assets/official-source-verifier-contract.json`: campos obligatorios del reporte.
- `assets/source-priority-policy.json`: jerarquía oficial > vendor > spec > repo > secondary.
- `assets/claim-evidence-policy.json`: cada claim mapea a fuente oficial o queda `unverified`.
- `assets/citation-policy.json`: URL, fecha de consulta y extracto/paráfrasis breve.
- `assets/decision-policy.json`: cambios autorizados sólo por evidencia oficial.
- `assets/evidence-policy.json`: evidencia mínima aceptada.

Cuando el entregable sea JSON, valida offline con `scripts/validate_official_source_verifier.py`. Para la smoke determinística completa ejecuta `scripts/check.sh`, que acepta fixtures válidos y rechaza mutaciones inválidas. [CONFIG]

## Procedimiento

1. Define la `question`: la decisión concreta que depende de autoridad externa. Si no la depende, detente: esta skill no aplica.
2. Registra fuentes en `source_registry` con `source_id`, `source_type`, `url`, `accessed_date`, `publisher`, `official`, y `role`.
3. Busca primero fuentes oficiales (WebSearch → WebFetch del doc canónico). Usa secundarias sólo para descubrir rutas o vocabulario, marcadas `role=lead`.
4. Para cada claim, exige `source_ids` y `official_source_ids`; si no hay fuente oficial, marca `status=unverified` y no autorices cambios.
5. Verifica vigencia: si la doc tiene versión o fecha, confirma que aplica a la versión usada por el repo; doc de otra major es `unverified`. [INFERENCIA]
6. Si fuentes oficiales se contradicen, prioriza spec o docs oficiales del proveedor más cercano al producto afectado, registra el conflicto en `blocking_gaps` y no resuelvas por cuenta propia.
7. La `decision` debe declarar `change_authorized`, `justified_change`, `scope`, y `blocking_gaps`.
8. Guardian bloquea si una fuente secundaria actúa como autoridad, si falta fecha de consulta, si hay claim sin fuente oficial, o si el cambio no está justificado.

## Gate de validación (acceptance criteria)

El reporte solo puede marcarse `pass` cuando TODO se cumple. Si una falla, el estado es `fail` o `blocked`. [DOC]

- Cada fuente tiene URL, publisher, `accessed_date` (ISO) y `source_type`.
- Cada claim tiene `official_source_ids` no vacío, o está marcado `unverified`.
- Ninguna fuente con `official=false` aparece como única evidencia de un claim `verified`.
- `decision.change_authorized=true` solo si todos los claims que lo sostienen son `verified`.
- `blocking_gaps` no vacío fuerza estado distinto de `pass`.
- Si se exige evidencia offline, el reporte pasa `scripts/check.sh`.

## Disparadores de autocorrección

Detente y corrige el reporte —no lo entregues— si detectas: [INFERENCIA]

- Un claim `verified` cuya URL apunta a blog, foro, issue, gist o resumen de IA → degradar a `unverified`.
- Una fecha de consulta ausente o futura → exigir `accessed_date` real antes de continuar.
- Un `change_authorized=true` sin claim oficial que lo respalde → revertir a `false` y abrir gap.
- Una sola fuente sosteniendo una decisión de alto impacto → buscar corroboración oficial adicional.
- Doc consultada de una versión distinta a la del repo → marcar conflicto de versión.

## Anti-patrones / fuera de alcance

- NO elevar una secundaria a autoridad "porque coincide con la oficial"; cítala oficial directamente o no la cites. [SUPUESTO]
- NO inferir la postura de una doc que no leíste: sin WebFetch del texto, el claim es `unverified`.
- NO resolver contradicciones entre fuentes oficiales silenciosamente; regístralas como gap.
- NO usar esta skill para validar lógica de negocio local, estilo de código u opiniones de arquitectura sin documento de autoridad.
- NO marcar `pass` con gaps abiertos por presión de avanzar — verde no es éxito por defecto.

## Decisiones y trade-offs

- **Oficial > vendor > spec > repo > secondary** como orden fijo: prioriza el documento más cercano al producto afectado. Trade-off: a veces la spec genérica es más correcta que la doc de vendor; por eso el paso 6 permite priorizar spec ante conflicto. [INFERENCIA]
- **`unverified` por defecto** ante duda: prefiere bloquear un cambio correcto que autorizar uno falso. Coste asumido: fricción extra en hallazgos legítimos. [SUPUESTO]
- **Fecha de consulta obligatoria**: la doc viva cambia; sin fecha el claim no es reproducible. [DOC]

## Ejemplo

`question`: "¿`gh pr merge` borra la rama por defecto?" Un blog dice que sí.
- `source_registry`: blog (`official=false`, `role=lead`) + GitHub CLI manual (`official=true`).
- WebFetch del manual oficial → el flag de borrado no es default.
- claim: `status=verified`, `official_source_ids=[gh-cli-manual]`, blog descartado como autoridad.
- `decision`: `change_authorized=false` (el workflow no necesita el cambio que el blog sugería); `justified_change` documenta el hallazgo. [DOC]

## Related Skills

- `workspace-governance`
- `quality-gatekeeper`
- `repo-sync-auditor`
