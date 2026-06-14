# Example output — qbr-quarterly

# QBR — Q2 (abr-jun) → Q3 (jul-sep) · JM Labs

> Cadencia P13 · baseline: MEMORY.md · destino: bitacora/2026-Q2.md · append aditivo
> Trimestre destino Q3 no fue explicito → autocompletado al Q calendario siguiente. {AUTOCOMPLETADO}

## 1. Scorecard del Q cerrado

| OKR / meta | Objetivo | Observado | Estado | Fuente |
|---|---|---|---|---|
| KR1: cierres diarios registrados | 60 | 58 | parcial (gap: 2) | bitacora/2026-Q2.md {DOC} |
| KR2: cierres con evidencia tagueada | 90% | 91% | logrado | bitacora/2026-Q2.md {DOC} |
| KR3: skills pasando DoD gate | 12 | 9 | parcial (gap: 3) | validate-skill-dod.py 2026-06-28 {DOC} |
| KR4: skills con tags mezclados | 0 | sin medir | {POR_CONFIRMAR} → verificar: grep de `[...]` en skills/*/SKILL.md | — |

## 2. Lecciones (a causa raiz)

1. **El DoD gate avanzo mas lento de lo previsto (9/12).** Causa raiz: el bundle DoD
   por skill (agentes + evals + assets) es mas trabajo del estimado, no falta de
   esfuerzo. {INFERENCIA} → mapea a objetivo Q3 de capacidad de certificacion.
2. **KR4 quedo sin instrumentar.** Causa raiz: no habia check deterministico para
   detectar mezcla de familias de tags. {INFERENCIA} → mapea a riesgo cross-quarter.
3. **Los cierres diarios casi llegan (58/60) con alta calidad de tags (91%).** El
   habito quedo; el gap es de volumen, no de disciplina. {EXTRAIDO_HILO}

## 3. Plan del proximo Q (Q3) — objetivos priorizados

1. **Certificar 12 skills bajo DoD.** metrica: 12 skills con dod=pass · owner: JM ·
   dependencia: tiempo de bundle por skill · deriva de: leccion 1.
2. **Instrumentar el check de familias de tags.** metrica: script que falla ante
   `[...]` en docs operador-facing · owner: JM · dependencia: ninguna · deriva de: leccion 2.
3. **Sostener cierres diarios >= 60/trimestre.** metrica: 60 cierres con >=90%
   tagueados · owner: JM · dependencia: ninguna · deriva de: leccion 3.

> Capacidad del Q3 no especificada → priorizado a capacidad nominal. {SUPUESTO}

## 4. Riesgos y dependencias cross-quarter

- KR4 sin baseline medido cruza al Q3 {POR_CONFIRMAR} → paso: correr grep de `[...]` antes del 2026-07-15.
- El backlog de skills sin DoD (catalogo grande) puede exceder la capacidad nominal del Q3. {SUPUESTO}

## 5. Estado de validacion (Acceptance Gate)

- Cada meta con estado + evidencia tagueada (o `{POR_CONFIRMAR}`): si
- Toda lecion mapea a objetivo o riesgo (sin huerfanos): si
- Cada objetivo nuevo medible y con owner: si
- Riesgos cross-quarter listados: si
- Una sola familia de tags Jarvis `{...}`, sin `[...]`: si
- Cero precios inventados; persistencia aditiva: si
