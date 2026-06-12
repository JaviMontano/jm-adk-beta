# Body of Knowledge — qbr-quarterly (P13)

Conocimiento de dominio para la cadencia de cierre trimestral de Jarvis OS. Conceptos
estables, estandares y reglas de decision. {CONOCIMIENTO}

## 1. Que es un QBR en esta cadencia

Un Quarterly Business Review aqui es una **auditoria trazable de un trimestre cerrado
contra su baseline de OKRs, seguida de la planeacion del proximo Q en la misma
pasada**. No es un reporte de estado optimista ni una planeacion desde cero: su valor
es la continuidad atras→adelante con evidencia ligada a cada dato.

## 2. Conceptos clave

- **Baseline.** Los OKRs/metas tal como se definieron al inicio del Q. Sin baseline
  registrado no hay auditoria posible: es `{VACIO_CRITICO}` terminal, se pide, no se inventa.
- **OKR (Objective + Key Results).** El objetivo es cualitativo y direccional; los key
  results son las metricas que lo hacen verificable. El QBR audita los key results.
- **Estado de meta.** logrado / parcial / fallido / `{POR_CONFIRMAR}`. Sale de la
  evidencia (observado vs. objetivo), nunca del optimismo.
- **Lecion.** Aprendizaje a causa raiz derivado de un desvio (gap o sobre-cumplimiento).
- **Objetivo del proximo Q.** Compromiso medible con owner y dependencia. Sin metrica
  no es objetivo, es deseo.
- **Riesgo cross-quarter.** Dependencia o amenaza abierta que cruza el corte del trimestre.

## 3. Estandares y reglas de decision

| Regla | Enunciado |
|---|---|
| Sin baseline, no audites | Falta baseline → `{VACIO_CRITICO}`, parar y pedir originales. |
| Estado se gana | Una meta es "logrado" solo con metrica observada >= objetivo y evidencia tagueada. |
| Sin metrica no es objetivo | Todo objetivo nuevo lleva metrica medible + owner + dependencia. |
| Sin huerfanos | Toda lecion mapea a un objetivo o riesgo del proximo Q. |
| Conservador ante conflicto | Dos fuentes con dos numeros → muestra ambas, prefiere la menor, marca conflicto. |
| Sobre-cumplimiento es senal | Excederse indica mala estimacion o esfuerzo no planeado; tambien es lecion. |
| Una familia de tags | Solo Jarvis `{...}`; nunca mezclar con Alfa `[...]`. |
| No verde-como-exito | El estado deriva de evidencia, no del color por defecto. |

## 4. Procedimiento (resumen operable)

1. **Discover** — localizar baseline + evidencia; sin baseline, detenerse.
2. **Audit** — estado por meta, observado vs. objetivo, fuente tagueada.
3. **Learn** — lecciones a causa raiz desde los desvios.
4. **Plan** — 3-5 objetivos del proximo Q ligados a las lecciones.
5. **Validate** — correr el Acceptance Gate antes de entregar.

## 5. Anti-patrones

- Declarar metas "logradas" sin metrica (over-claim).
- Plan del proximo Q desconectado de las lecciones (copy del trimestre anterior).
- Promediar metricas en conflicto sin marcar el conflicto.
- Mezclar familias de tags en un mismo documento.

## 6. Limites

- No reemplaza revision experta en decisiones de alto riesgo (legal, financiero, seguridad). {DOC}
- Sin evidencia, una afirmacion va como `{SUPUESTO}` o `{POR_CONFIRMAR}`, nunca como hecho.
- Sin precios inventados; FTE-meses + disclaimers si se requiere dimensionar esfuerzo.

Taxonomia de evidencia completa: `references/verification-tags.md`.
