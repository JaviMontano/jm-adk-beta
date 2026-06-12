# Prompt — Deep (monthly-audit)

Variante exhaustiva de la auditoria P22 para cierres trimestrales, post-incidente,
o cuando hay regresiones que cruzan varios meses.

## Instruccion
Audita los **6 ejes** con triangulacion de evidencia: por cada score cruza al
menos dos fuentes (p.ej. MEMORY.md vs commits) y resuelve discrepancias.

## Profundidad adicional
- **Delta multi-mes**: traza la tendencia de cada eje sobre 2-3 baselines, no solo
  el mes previo; nombra ejes en deriva lenta.
- **Causa raiz** por cada eje 0-1: por que esta fragil, no solo que lo esta.
- **Riesgos sistemicos**: lista los que cruzan al mes siguiente con `{POR_CONFIRMAR}`
  y su paso de verificacion.
- **Top 3 con secuencia**: ademas de priorizar por riesgo x impacto, ordena por
  dependencia (que accion desbloquea a las otras).

## No negociable
- Evidencia contradictoria → gana lo verificable en codigo/config; marca la discrepancia.
- Sigue siendo **maximo 3 acciones** en el plan; el resto a backlog.
- Un tag por afirmacion, una sola familia; `{WEB}` invalido sin cita.
- Persistencia aditiva; revisa diff antes de cualquier `--force`.
