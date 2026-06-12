# Acceptance Gate checklist — qbr-quarterly

Espejo del Acceptance Gate de `SKILL.md`. El guardian bloquea "hecho" hasta marcar
cada casilla con evidencia.

## Mirar atras (auditoria)
- [ ] Baseline de OKRs localizado y citado (sin baseline → `{VACIO_CRITICO}`, parar).
- [ ] Cada meta del Q cerrado tiene estado: logrado / parcial / fallido / `{POR_CONFIRMAR}`.
- [ ] Cada estado cuelga de metrica observada vs. objetivo con fuente tagueada.
- [ ] Ninguna meta declarada "logrado" sin metrica observada (no verde por defecto).
- [ ] Metricas en conflicto: ambas mostradas, conservadora preferida, conflicto marcado.

## Lecciones
- [ ] 2-5 lecciones, cada una a causa raiz (no sintoma).
- [ ] Toda lecion mapea a un objetivo o riesgo del proximo Q (sin huerfanos).

## Mirar adelante (plan)
- [ ] 3-5 objetivos del proximo Q.
- [ ] Cada objetivo es medible y tiene owner + dependencia.
- [ ] Plan derivado de las lecciones (no copy del trimestre anterior).
- [ ] Riesgos y dependencias cross-quarter listados explicitamente.

## Gobernanza
- [ ] Una sola familia de tags Jarvis `{...}`, sin `[...]`.
- [ ] Cero precios inventados; sin PII de cliente; marca unica.
- [ ] Persistencia aditiva; `--force` solo tras revisar diffs.
