# Body of knowledge — daily-close

Conocimiento de dominio para la cadencia de cierre diario P10 de Jarvis OS.

## Conceptos clave

- **Cadencia P10.** Ritual de fin de jornada (no de fin de tarea). Su valor no es
  el registro sino la **continuidad**: cada cierre siembra el arranque siguiente.
- **Tres ejes.** Toda jornada se descompone en Cerrado / Pendiente / Aprendido.
  Es una particion: cada item cae en **exactamente un** eje.
  - *Cerrado* — completado y verificable hoy, con evidencia ligada.
  - *Pendiente* — abierto; lleva motivo de no-cierre + primer paso de manana.
  - *Aprendido* — insight/friccion/decision reusable. Sin este eje el cierre
    degrada a changelog.
- **Semilla del dia siguiente.** 1-3 pendientes priorizados, cada uno con su
  primer paso ejecutable **en frio** (sin recontexto). Sembrar todo = no sembrar.
- **Persistencia aditiva.** El cierre se hace **append** a la bitacora/MEMORY; el
  historico es inmutable salvo `--force` tras revisar diff.
- **Read-before-write.** Leer fuente y destino antes de escribir; ontology-first.

## Estandares

- **Familia de tags Jarvis OS `{...}`** (operador-facing). Una sola familia por
  documento; nunca mezclar con Alfa `[...]`. Detalle en
  `references/verification-tags.md`.
- **Evidencia obligatoria** en toda afirmacion no obvia: `{DOC}`, `{EXTRAIDO_HILO}`,
  `{MEMORIA}`, `{INFERENCIA}`, `{SUPUESTO}`, `{AUTOCOMPLETADO}`, `{VACIO_CRITICO}`,
  `{POR_CONFIRMAR}`, `{WEB}` (solo con cita).
- **No verde-como-exito.** Un eje/check no se declara ok sin evidencia.
- **Marca unica.** Un cierre cubre un workspace; no fusiona marcas/proyectos.

## Reglas de decision

| Situacion | Regla |
|---|---|
| Item ambiguo Cerrado/Pendiente | Es Pendiente (el cierre se gana, no se asume) |
| Eje Aprendido aparenta vacio | Releer la jornada por fricciones antes de declararlo |
| Semilla con > 3 items | Re-priorizar a top 1-3 por impacto-en-arranque |
| Fecha no explicita | Autocompletar hoy + `{AUTOCOMPLETADO}` |
| Fuente o destino ausente | `{VACIO_CRITICO}`: detener y preguntar |
| Cierre retroactivo | Fechar al dia real; `{SUPUESTO}` lo reconstruido |
| Bloqueo cruza al manana | `{POR_CONFIRMAR}` + paso de verificacion |
| Dia sin actividad | Registrar igual con "sin avances" explicito |
| Conflicto "cierra pero salta validacion" | Nombrar conflicto; validacion no es opcional |

## Anti-patrones

- Cierre = solo Cerrado (changelog sin Aprendido ni semilla).
- Volcar la lista entera de pendientes como "semilla" sin priorizar.
- Sobrescribir historico en vez de append.
- Mezclar familias de tags `{...}` y `[...]`.
- Inventar items para llenar un eje vacio.

## Limites

- No reemplaza revision experta para decisiones de alto riesgo (legal, medico,
  financiero, seguridad).
- Sin evidencia disponible, el item se marca `{SUPUESTO}`/`{POR_CONFIRMAR}` con su
  paso de verificacion; nunca se presenta como hecho.
