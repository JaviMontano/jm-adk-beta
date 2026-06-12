---
name: qbr-quarterly
version: 0.2.0
description: "Cadencia QBR (P13): audita el trimestre cerrado contra OKRs y planifica el proximo con evidencia trazable."
owner: "JM Labs"
triggers:
  - qbr
  - quarterly-review
  - repaso-trimestral
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# QBR Quarterly (P13)

Cadencia de cierre trimestral: mira atras (que se cumplio vs. lo prometido) y
mira adelante (compromisos del proximo trimestre) en una sola pasada auditable.
Tags Jarvis OS (operador): ver `references/verification-tags.md`. {CONOCIMIENTO}

## When To Use

- Cierre de Q activo o arranque del siguiente — el usuario pide "QBR", "repaso
  trimestral" o nombra P13. {EXTRAIDO_HILO}
- Hay un trimestre con OKRs/metas definidos al inicio que ahora se cierran. {SUPUESTO}

**No usar** para: standups o repasos semanales (cadencia equivocada), planeacion
anual completa (mayor alcance), o un trimestre sin metas base — sin baseline no
hay auditoria, solo planeacion; dilo y degrada el alcance. {INFERENCIA}

## Inputs Expected

| Input | Obligatorio | Si falta |
|---|---|---|
| OKRs/metas del trimestre que cierra | Si | `{VACIO_CRITICO}`: parar, pedir baseline |
| Evidencia de resultados (metricas, entregables, logs) | Si | Marcar metas sin medir como `{POR_CONFIRMAR}` |
| Trimestre destino y horizonte | Si | Asumir el Q calendario siguiente, marcar `{AUTOCOMPLETADO}` |
| Capacidad/constraints del proximo Q | No | Planear a capacidad nominal, marcar `{SUPUESTO}` |

## Outputs Expected

1. **Scorecard del Q cerrado** — cada OKR con estado (logrado / parcial / fallido),
   metrica observada vs. objetivo, y tag de fuente por dato. {CONOCIMIENTO}
2. **Lecciones** — 2-5 aprendizajes con causa raiz, no sintomas.
3. **Plan del proximo Q** — 3-5 objetivos priorizados, cada uno con metrica
   medible y owner. Sin metrica no es objetivo, es deseo. {INFERENCIA}
4. **Riesgos y dependencias abiertas** que cruzan el corte de trimestre.

## Procedure

### 1. Discover
Localiza el baseline del Q (OKRs originales) y la evidencia de cierre. Si no
existe baseline registrado, detente: es `{VACIO_CRITICO}`, no lo inventes.

### 2. Audit (mirar atras)
Por cada meta: compara observado vs. objetivo, asigna estado, etiqueta la fuente
del dato. Una meta sin evidencia medible se marca `{POR_CONFIRMAR}`, nunca se
declara lograda por defecto. {CONOCIMIENTO}

### 3. Learn
Destila lecciones desde los desvios (gaps y sobre-cumplimientos). Apunta a causa
raiz; descarta observaciones sin accion derivable.

### 4. Plan (mirar adelante)
Deriva 3-5 objetivos del proximo Q ligados a las lecciones. Cada uno: metrica,
owner, dependencia. Prioriza por valor/esfuerzo cuando haya constraint de capacidad.

### 5. Validate
Corre el gate de aceptacion antes de entregar.

## Acceptance Gate

- [ ] Cada meta del Q cerrado tiene estado + evidencia tagueada (o `{POR_CONFIRMAR}`).
- [ ] Toda lecion mapea a un objetivo o riesgo del proximo Q (sin huerfanos).
- [ ] Cada objetivo nuevo es medible y tiene owner.
- [ ] Riesgos cross-quarter listados explicitamente.
- [ ] Cero precios inventados; sin overwrite de ediciones locales sin `--force`.

## Edge Cases

- **Sin baseline**: terminal (`{VACIO_CRITICO}`) — pide los OKRs originales, no audites de memoria.
- **Q parcial / pivote a mitad**: audita contra las metas que estaban vigentes en cada tramo; nota el pivote.
- **Metricas en conflicto** (dos fuentes, dos numeros): muestra ambas, prefiere la mas conservadora, marca el conflicto.
- **Sobre-cumplimiento**: trata como senal — sub-estimacion o esfuerzo no planeado; tambien es lecion.

## Anti-Patterns

- Declarar metas "logradas" sin metrica — over-claim, prohibido.
- Verde como exito automatico: el estado sale de la evidencia, no del optimismo.
- Plan del proximo Q desconectado de las lecciones (copy del trimestre anterior).
- Mezclar familias de tags en un mismo documento. {CONOCIMIENTO}

## Self-Correction Triggers

- Estado de meta sin tag de fuente -> regresa a Audit.
- Objetivo nuevo sin metrica u owner -> regresa a Plan.
- Lecion sin objetivo/riesgo asociado -> elimina o conectala.

## Related Skills

- `workspace-governance` — donde viven OKRs y baselines.
- `workflow-forge` — para operacionalizar el plan del proximo Q.
- `quality-guardian` — gate de evidencia y tagueo.

## Assumptions and Limits

- No reemplaza revision experta en decisiones de alto riesgo (legal, financiero, seguridad). {DOC}
- Sin evidencia, una afirmacion va como `{SUPUESTO}` o `{POR_CONFIRMAR}`, nunca como hecho.

## Assets

- Rubrica de calidad y checklist del gate viven en `assets/` (ver `assets/README.md`).

## Update-Safety Notes

- Archivos de soporte generados son missing-only por defecto.
- Usa `--force` solo tras revisar diffs.
