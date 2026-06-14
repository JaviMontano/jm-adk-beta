---
name: wbr-weekly-review
version: 0.2.0
description: "Cadencia WBR (P11): repaso semanal de avances, estancado y friccion; produce un acta accionable con dueno y proximo paso por item."
owner: "JM Labs"
last_updated: 2026-06-11
triggers:
  - wbr
  - weekly-review
  - repaso-semanal
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# WBR — Weekly Review

Ritual operativo P11. Cierra la semana en tres lentes — **avances**, **estancado**, **friccion** — y deja un acta corta donde cada item estancado o friccionado tiene dueno y proximo paso fechado. No es un reporte de estado pasivo: el output debe permitir actuar el lunes sin reabrir la semana. {CONOCIMIENTO}

## When to use / not use

- **Usar**: cierre semanal de una estacion, sector o proyecto; preparar handoff entre semanas; detectar estancamiento antes de que se vuelva bloqueo cronico.
- **No usar**: planificacion intradia → `dbr-daily-plan`; auditoria profunda de mes → `monthly-audit`; retro de equipo formal (usa el motor de retrospectiva del host). {INFERENCIA}
- Si no hay periodo ni alcance claro, NO inventes la semana: pregunta. {SUPUESTO}

## Inputs (lo que se necesita)

- **Periodo y alcance** (semana ISO + estacion/sector/proyecto). Sin esto → `{VACIO_CRITICO}`, detener y pedir.
- **Compromisos de la semana anterior** (que se prometio cerrar) para medir cumplimiento real, no percibido.
- **Senales de avance**: commits, entregables, decisiones, hitos — con artefacto verificable cuando exista. {ADJUNTO}
- **Items en curso** y desde cuando (para calcular antiguedad del estancamiento).
- Opcional: WBR de la semana previa para arrastrar items abiertos y evitar amnesia.

## Outputs (lo que se entrega)

Acta WBR en Markdown, escaneable, con estas secciones:

1. **Encabezado**: periodo ISO, alcance, fecha de corte.
2. **Avances** — bullets verbo-en-pasado + evidencia. Solo lo cerrado/movido de verdad.
3. **Estancado** — tabla `item | desde (dias) | causa raiz | dueno | proximo paso (fecha)`.
4. **Friccion** — lo que costo mas de lo debido; clasificar como *recurrente* o *puntual*.
5. **Compromisos proxima semana** — maximo 3-5, cada uno con dueno y criterio de hecho.
6. **Arrastres** — items abiertos heredados, con conteo de semanas abiertas.

Toda afirmacion no obvia lleva una tag de la familia Jarvis (`{...}`); ver `references/verification-tags.md`. No mezclar familias. {DOC}

Para puntuar el acta contra el gate, usar la rubrica y el checklist en `assets/` (ver `assets/README.md`). {CONFIG}

## Procedure

1. **Recolectar** — leer compromisos previos + senales de la semana; si falta periodo/alcance, parar y preguntar.
2. **Clasificar** — cada item a exactamente un lente (avance / estancado / friccion). Un item estancado NUNCA va tambien en avances.
3. **Diagnosticar estancado** — para cada uno: antiguedad, causa raiz (no sintoma), dueno nominal. Sin dueno, el item esta mal cerrado.
4. **Comprometer** — derivar 3-5 compromisos de la proxima semana desde estancado+friccion, no desde deseos nuevos. Cada uno con criterio de hecho.
5. **Validar** — correr el gate de abajo antes de entregar.

## Validation gate (acceptance criteria)

- [ ] Cada seccion presente; encabezado con periodo ISO y alcance. {DOC}
- [ ] Cada item estancado tiene **dueno + proximo paso fechado** (no "se revisara").
- [ ] Compromisos previos marcados cumplido / parcial / no-cumplido — sin omitir los fallidos.
- [ ] Cada friccion clasificada recurrente vs puntual; las recurrentes (≥2 semanas) escalan a accion.
- [ ] Compromisos proxima semana ≤ 5, cada uno con criterio de hecho.
- [ ] Tags de una sola familia; `{SUPUESTO}`/`{POR_CONFIRMAR}` con paso de verificacion. {DOC}

## Edge cases

- **Semana vacia / vacaciones**: registrar explicitamente "sin actividad" + razon; no fabricar avances. {SUPUESTO}
- **Todo verde, nada estancado**: sospechar subreporte — preguntar que NO se movio. El verde sin friccion suele ser falta de visibilidad, no exito.
- **Item arrastrado ≥3 semanas**: marcar `{POR_CONFIRMAR}` y escalar; deja de ser estancado y pasa a bloqueo.
- **Compromiso previo incumplido**: nombrarlo y heredarlo a la nueva semana; nunca borrarlo silenciosamente.
- **Conflicto de alcance** (varias estaciones en un WBR): separar por alcance o pedir foco; no promediar.

## Anti-patterns (no hacer)

- Reporte de estado sin dueno ni proximo paso — eso es un log, no un WBR.
- Pintar todo verde para evitar conversaciones incomodas (never green-as-success). {DOC}
- Mover un item estancado a "avances" porque "ya casi".
- Inflar avances con actividad (reuniones, lecturas) en vez de resultados.
- Generar >5 compromisos: dilucion garantiza incumplimiento.

## Update-safety

- Archivos de soporte generados: missing-only por defecto; preservar ediciones locales.
- Usar `--force` solo tras revisar diffs.

## Related skills

- `dbr-daily-plan` — cadencia diaria que alimenta este WBR. {CONFIG}
- `monthly-audit` — agrega varios WBR en una mirada mensual.
- `daily-close` — cierre de jornada cuyos arrastres entran al estancado semanal.
