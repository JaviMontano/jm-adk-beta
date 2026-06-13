# Acta WBR — {alcance} — {semana ISO}

- **Periodo**: {semana ISO, p.ej. 2026-W24}
- **Alcance**: {estacion / sector / proyecto unico}
- **Fecha de corte**: {AAAA-MM-DD}
- **Tags**: familia Jarvis OS `{...}` (una sola familia)

## 1. Avances
> Solo lo cerrado o movido de verdad, con evidencia. Bullets verbo-en-pasado.

- {Verbo-en-pasado} {resultado} — {evidencia: commit / entregable / decision} {ADJUNTO}
- ...

## 2. Estancado
> Cada item con dueno y proximo paso fechado. Causa raiz, no sintoma.

| item | desde (dias) | causa raiz | dueno | proximo paso (fecha) |
|---|---|---|---|---|
| {item} | {n} | {causa} | {dueno} | {accion — AAAA-MM-DD} |

## 3. Friccion
> Lo que costo mas de lo debido. Clasificar recurrente vs puntual.

- {friccion} — **recurrente** (≥2 semanas) → escala a: {accion} {INFERENCIA}
- {friccion} — **puntual**

## 4. Cumplimiento de compromisos previos
> Marcar cada uno; no omitir los fallidos.

- {compromiso} — **cumplido** / **parcial** / **no-cumplido** {DOC}
- ...

## 5. Compromisos proxima semana
> Maximo 3-5, derivados de estancado+friccion. Cada uno con criterio de hecho.

1. {compromiso} — dueno: {dueno} — hecho cuando: {criterio observable}
2. ...

## 6. Arrastres
> Items abiertos heredados, con conteo de semanas abiertas.

- {item} — {n} semanas abierto — {estado} {POR_CONFIRMAR si ≥3 semanas}
- ...

---
**Notas**: items vacios se declaran "sin actividad" + razon, no se fabrican.
Never green-as-success.
