# Prompt — Quick (dbr-daily-plan)

Variante rapida: emite un **P09** minimo cuando el usuario solo da un backlog y
una nocion de horas. Optimiza por velocidad sin romper la cadencia.

## Flujo express
1. Si no hay backlog ⇒ `{VACIO_CRITICO}`, pide la agenda, para.
2. Toma las **3 candidatas de mayor impacto** en la restriccion. Si dudas entre
   urgencia e impacto, gana impacto.
3. Asigna **1 buffer agregado** (no por prioridad) si el tiempo aprieta; marcalo.
4. Escribe solo: tambor (<=3 con resultado verificable), no-hoy (1 linea), primer
   paso de la #1.
5. Salta la justificacion larga; conserva el gate de capacidad (suma + buffer <=
   horas reales).

## Salida
P09 compacto, <=8 lineas, accionable hoy. Tags solo donde un supuesto cambia la
decision (`{AUTOCOMPLETADO}` para horas estimadas).
