# Body of Knowledge — dbr-daily-plan

Dominio: planificacion diaria con **Drum-Buffer-Rope (DBR)**, la implementacion
operativa de la **Teoria de Restricciones (TOC)** de Eliyahu Goldratt aplicada al
horizonte de un (1) dia. El deliverable es el plan **P09**.

## 1. Conceptos clave

### Restriccion (constraint)
El recurso que limita el throughput del dia. En trabajo de conocimiento suele ser
**tiempo de foco profundo**, pero puede ser una persona, un permiso, una
aprobacion o una dependencia externa. Regla: todo lo demas se **subordina** a la
restriccion (Five Focusing Steps, paso 3).

### Tambor (drum)
La 1-3 prioridades que **marcan el ritmo** del dia. Se eligen por
**impacto-en-la-restriccion**, no por urgencia percibida. Un dia tiene un tambor
dominante; el resto se subordina.

### Buffer
Margen de tiempo/capacidad reservado para proteger al tambor del primer
imprevisto. **Heuristica**: a mayor incertidumbre de una prioridad, mayor buffer.
Un dia planificado al 100% no tiene buffer — es fragil por construccion.

### Cuerda (rope)
El mecanismo que limita el WIP admitido al ritmo que el tambor puede procesar. En
esta cadencia, la **cuerda son dos cosas**: el corte duro a **<=3 prioridades** y
la lista **no-hoy** explicita.

### P09
El identificador del artefacto: el plan del dia. No es una to-do list; es una
**decision de foco bajo restriccion** con tambor, buffer, no-hoy y primer paso.

## 2. Five Focusing Steps (adaptados al dia)
1. **Identificar** la restriccion del dia (¿cuanto foco real tengo?).
2. **Explotarla**: dedicar la restriccion al tambor de mayor impacto.
3. **Subordinar** todo lo demas a esa decision (no-hoy).
4. **Elevar** la restriccion si persiste (delegar, mover reuniones, pedir bloque).
5. **No dejar que la inercia** se vuelva la restriccion: revisar, no arrastrar el
   plan de ayer a ciegas.

## 3. Reglas de decision (decision rules)
- **R1 — Ranking por impacto, no urgencia.** Ordena candidatos por impacto en la
  restriccion; desempata por riesgo de incumplir un hard deadline.
- **R2 — Corte duro <=3.** Si >3 superan el corte, recorta. Decir "no" es el valor.
- **R3 — Capacidad respeta restriccion.** suma(estimados) + buffer <= horas reales.
  Si no cabe, recorta ANTES de planificar.
- **R4 — Resultado verificable.** Cada prioridad expresa un "hecho" observable.
- **R5 — Buffer obligatorio.** Cada prioridad nombra su riesgo principal y su
  mitigacion/margen.
- **R6 — No-hoy explicito.** Los descartes se escriben; protegen el foco.
- **R7 — Primer paso <15 min.** La #1 arranca con una accion concreta de hoy.

## 4. Estandares y referencias
- TOC / DBR: Goldratt, *The Goal* (1984) y *Critical Chain* (1997). [DOC]
- Five Focusing Steps como marco de subordinacion a la restriccion. [DOC]
- Familia de evidencia **Jarvis OS** (operador), no la familia Alfa. [DOC]

## 5. Taxonomia de evidencia (Jarvis OS)
`{MEMORIA}` (de MEMORY.md), `{ADJUNTO}`, `{EXTRAIDO_HILO}` (del hilo),
`{SUPUESTO}`, `{INFERENCIA}`, `{AUTOCOMPLETADO}`, `{POR_CONFIRMAR}`,
`{VACIO_CRITICO}` (terminal: detener y pedir). Tag solo en lo no trivial.

## 6. Anti-patterns (que NO es un P09)
- **To-do list disfrazada**: 8 items sin tambor ni buffer.
- **Falso buffer**: dia al 100% sin margen.
- **Urgencia = prioridad**: ordenar por lo que grita mas alto.
- **Recompromiso silencioso**: arrastrar el plan de ayer sin revalidar el tambor.
- **Sobre-tagueo**: tags en lo evidente, degrada escaneabilidad.

## 7. Edge cases
- **Backlog vacio** ⇒ `{VACIO_CRITICO}`, detener.
- **Todo es P0** ⇒ exponer contradiccion, forzar ranking.
- **Dia saturado de reuniones** ⇒ tambor = proteger 1 bloque de foco; declarar
  capacidad ejecutable minima `{SUPUESTO}`.
- **Personalizacion local** ⇒ preservar `.local`/`user-context`; cambios aditivos.
