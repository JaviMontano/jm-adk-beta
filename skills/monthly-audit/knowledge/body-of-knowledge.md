# Body of Knowledge — monthly-audit (P22)

Conocimiento de dominio para la auditoria mensual de salud del jarvis. Define
conceptos, escala, reglas de decision y estandares de evidencia.

## Conceptos clave

- **Cadencia P22**: ritmo mensual que mira el **sistema** (no el dia). Se distingue
  de P10 `daily-close`, que cierra la jornada, y de los retros de proyecto.
- **Eje de rubrica**: una de las 6 dimensiones de salud evaluadas. Cada eje es
  independiente y se puntua por separado.
- **Score 0-3**: 0 ausente · 1 fragil · 2 funcional · 3 solido. Es ordinal, no
  promediable a la ligera; el scorecard reporta los 6 numeros, no una media.
- **Delta**: comparacion del score de cada eje contra el mes previo: mejora /
  estable / regresion. Requiere baseline; en primera corrida es n/a.
- **Evidencia citable**: archivo, commit o entrada de bitacora que justifica un
  score. Un score sin evidencia no es un hecho, es `{POR_CONFIRMAR}`.
- **Riesgo x impacto**: criterio de priorizacion del Top 3 acciones. Riesgo = daño
  si no se atiende; impacto = cuanto mueve la salud del sistema.
- **Persistencia aditiva**: append a la bitacora destino; el historico de
  auditorias es inmutable salvo `--force` revisado.

## Los 6 ejes (rubrica P22)

| # | Eje | Pregunta nuclear | Fuente tipica |
|---|---|---|---|
| 1 | Memoria | ¿MEMORY/bitacora refleja el estado real y es recuperable en frio? | MEMORY.md, memory/_INDICE.md |
| 2 | Cadencias | ¿daily-close y demas ritmos corrieron con la frecuencia esperada? | bitacora diaria, logs P10 |
| 3 | Tareas | ¿el backlog esta vivo (sin huerfanos ni stale) y priorizado? | TAREAS.md, tasklog |
| 4 | Estructura/AI | ¿arquitectura de informacion, skills y rutas siguen coherentes? | _ESTRUCTURA.md, index-of-indexes |
| 5 | Guardrails | ¿disciplina de marca, evidencia y update-safety se respetaron? | commits, diffs, outputs del mes |
| 6 | Friccion/Deuda | ¿que fricciones recurrentes o deuda se acumularon sin atender? | retros, notas de friccion |

## Reglas de decision

1. **Read-before-write**: lee fuentes y auditoria previa antes de puntuar.
2. **Score conservador**: ante duda entre dos niveles, elige el menor y anota la
   evidencia que subiria el numero.
3. **Sin evidencia → `{POR_CONFIRMAR}`**, nunca un 2 inventado.
4. **Evidencia contradictoria**: gana lo verificable en codigo/config; marca la
   discrepancia.
5. **Top 3 duro**: solo 3 acciones derivadas de ejes 0-1 y regresiones; el resto a
   backlog.
6. **Una auditoria por workspace**: no fusionar salud de marcas o proyectos.

## Estandares de evidencia (taxonomia Jarvis OS)

Familia `{...}` exclusiva; ver `references/verification-tags.md`. Exactamente un
tag por afirmacion no obvia. `{WEB}` invalido sin cita. Nunca presentar
`{SUPUESTO}`/`{POR_CONFIRMAR}` como hecho. No verde-como-exito.

## Limites

- No reemplaza revision experta en decisiones de alto riesgo (legal, medico,
  financiero, seguridad).
- No inventa baseline: primera corrida deja deltas n/a y fija el baseline del mes
  siguiente.
