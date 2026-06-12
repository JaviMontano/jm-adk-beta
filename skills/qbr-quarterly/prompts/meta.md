# Prompt — meta (qbr-quarterly self-check)

Meta-prompt para que el operador audite su propio QBR antes de entregarlo. No
produce el entregable; lo inspecciona contra el Acceptance Gate.

## Preguntas de control

1. **Baseline real.** ¿Audite contra el baseline registrado de OKRs, o reconstrui de
   memoria? Si es lo segundo sin baseline → `{VACIO_CRITICO}`, no entregues.
2. **Estado ganado.** ¿Cada meta marcada "logrado" tiene metrica observada >= objetivo
   con evidencia tagueada? ¿Alguna esta verde solo por optimismo? → corrige.
3. **Tags.** ¿Cada afirmacion no obvia lleva exactamente un tag Jarvis `{...}`? ¿Hay
   algun `[...]` colado (mezcla de familias)? → corrige.
4. **Lecciones conectadas.** ¿Toda lecion mapea a un objetivo o riesgo del proximo Q?
   ¿Hay huerfanas? → conecta o elimina.
5. **Objetivos medibles.** ¿Cada objetivo nuevo tiene metrica + owner + dependencia?
   ¿Alguno es deseo sin metrica? → recházalo.
6. **Continuidad.** ¿El plan del proximo Q deriva de las lecciones, o es copy del
   trimestre anterior? → re-deriva.
7. **Conflictos.** ¿Marque metricas en conflicto y preferi la conservadora?
8. **Gobernanza.** ¿Cero precios inventados? ¿Sin PII de cliente? ¿Marca unica?
   ¿Persistencia aditiva sin overwrite no revisado?

## Veredicto
Para cada pregunta: pass / conditional / fail / not-verified (segun
`assets/quality-rubric.json`). Un solo **fail** bloquea la entrega.
