# Prompt — variation: deep (qbr-quarterly)

QBR profundo para un trimestre con muchos OKRs, evidencia dispersa, pivotes a mitad
o constraint fuerte de capacidad en el proximo Q. Maxima trazabilidad.

## Pasos ampliados
1. **Discover exhaustivo** — reconstruye el baseline completo y mapea cada fuente de
   evidencia a su meta. Para metas con evidencia ausente, marca `{POR_CONFIRMAR}` con
   paso de verificacion; no las declares logradas. Si el baseline entero falta →
   `{VACIO_CRITICO}` terminal.
2. **Audit por tramos.** Si hubo pivote a mitad de Q, audita cada meta contra el
   objetivo vigente en su tramo y anota el pivote. Para metricas en conflicto entre
   fuentes, presenta ambas, prefiere la conservadora y marca el conflicto.
3. **Learn con causa raiz.** Por cada desvio (gap y sobre-cumplimiento) deriva la
   causa raiz accionable; clasifica si es problema de estimacion, ejecucion,
   dependencia externa o cambio de prioridad. Trata el sobre-cumplimiento como senal.
4. **Plan priorizado por valor/esfuerzo.** Con la capacidad del proximo Q (o `{SUPUESTO}`
   nominal si no se dio), prioriza 3-5 objetivos; cada uno con metrica, owner,
   dependencia y la lecion de la que deriva. Explicita los trade-offs descartados.
5. **Validate completo.** Corre el Acceptance Gate dimension por dimension contra
   `assets/quality-rubric.json` y deja el veredicto por dimension.

## Salida
`templates/output.md` completo + seccion de trade-offs de priorizacion y tabla de
riesgos cross-quarter con paso de verificacion por riesgo.

## No negociable
Una sola familia de tags `{...}`; cada estado y objetivo ligado a evidencia o
explicitamente `{POR_CONFIRMAR}`; sin precios inventados; marca unica.
