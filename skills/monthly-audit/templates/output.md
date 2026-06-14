# Auditoria mensual P22 — <Workspace> — <Mes AAAA-MM>

> Generado por `monthly-audit`. Append aditivo a la bitacora. No sobrescribe historico.

## Contexto
- **Workspace**: <nombre>
- **Mes auditado**: <AAAA-MM>  <!-- {AUTOCOMPLETADO} si se rellena por defecto -->
- **Baseline**: <mes previo o "n/a — primera corrida">
- **Fuentes leidas**: MEMORY.md, TAREAS.md, bitacora, commits  <!-- {MEMORIA} -->

## Scorecard P22

| # | Eje | Score (0-3) | Evidencia ligada | Tag | Delta vs mes previo |
|---|---|---|---|---|---|
| 1 | Memoria | <0-3> | <archivo/commit/entrada> | {DOC} | mejora / estable / regresion / n/a |
| 2 | Cadencias | <0-3> | <ref> | {DOC} | <delta> |
| 3 | Tareas | <0-3> | <ref> | {DOC} | <delta> |
| 4 | Estructura/AI | <0-3> | <ref> | {DOC} | <delta> |
| 5 | Guardrails | <0-3> | <ref> | {DOC} | <delta> |
| 6 | Friccion/Deuda | <0-3> | <ref> | {DOC} | <delta> |

> Escala: 0 ausente · 1 fragil · 2 funcional · 3 solido.
> Score sin evidencia → marcar `{POR_CONFIRMAR}`, no como hecho.

## Notas de evidencia
- <Eje>: <observacion con su tag Jarvis OS>

## Top 3 acciones (riesgo x impacto)
1. **<accion>** — eje <#>, riesgo <alto/medio/bajo>, impacto <alto/medio/bajo>.
   Primer paso: <ejecutable en frio>.  <!-- {INFERENCIA} -->
2. **<accion>** — ...
3. **<accion>** — ...

## Riesgos sistemicos abiertos (cruzan al mes siguiente)
- <riesgo> — `{POR_CONFIRMAR}` + paso de verificacion.

## Estado de validacion (gate P22)
- [ ] 6 ejes puntuados 0-3
- [ ] Cada score con evidencia ligada (o `{POR_CONFIRMAR}`)
- [ ] Delta calculado o n/a explicito
- [ ] Top 3 (no mas), priorizadas, con primer paso
- [ ] Un tag por afirmacion; una sola familia; `{WEB}` con cita
- [ ] Persistencia aditiva; historico intacto

**Veredicto**: <pass / fail — corregir>
