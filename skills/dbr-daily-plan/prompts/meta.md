# Prompt — Meta (dbr-daily-plan)

Meta-prompt para auto-revisar un plan **P09** antes de entregarlo. Aplicalo como
critico interno: no reescribe el plan, lo audita contra la cadencia DBR.

## Preguntas de auto-critica
1. **¿Hay tambor o solo lista?** ¿Las prioridades marcan el ritmo del dia o son 8
   items sin foco? Si es lista, falla por "to-do disfrazada".
2. **¿El ranking es por impacto en la restriccion** o por urgencia percibida? Si
   ordene por lo que grita mas alto, reordena.
3. **¿Hay <=3 tambores?** 4+ ⇒ recorta; nombra que se va a no-hoy.
4. **¿Cada prioridad tiene resultado verificable?** "avanzar en X" no es un
   resultado — reescribe a "hecho" observable.
5. **¿La capacidad respeta la restriccion?** suma + buffer <= horas reales. Si el
   dia esta al 100%, el buffer es falso.
6. **¿Hay buffer real** por prioridad (riesgo + mitigacion)?
7. **¿No-hoy explicito?** El foco se defiende descartando.
8. **¿Primer paso <15 min** para la #1, accionable hoy?
9. **¿Evidencia correcta?** Familia Jarvis OS, sin sobre-tagueo, `{VACIO_CRITICO}`
   tratado como terminal.
10. **¿Una pantalla?** Si se desborda, comprime — no agregues prioridades.

## Resolucion
Por cada "no", aplica la accion correctiva mas conservadora: **degradar el plan**
(menos prioridades, mas buffer) antes que inflarlo. Devuelve el veredicto
`PASS`/`FAIL` con la lista de casillas incumplidas.
