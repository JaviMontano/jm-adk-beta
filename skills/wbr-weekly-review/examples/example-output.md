# Acta WBR — Jarvis-OS — 2026-W24

- **Periodo**: 2026-W24
- **Alcance**: estacion Jarvis-OS
- **Fecha de corte**: 2026-06-12
- **Tags**: familia Jarvis OS `{...}`

## 1. Avances

- Mergeado el refactor del router de cadencias en 3 PRs — commits a1b2c3, d4e5f6,
  7g8h9i {ADJUNTO}
- Documentada la familia de tags Jarvis en `references/verification-tags.md` {DOC}

## 2. Estancado

| item | desde (dias) | causa raiz | dueno | proximo paso (fecha) |
|---|---|---|---|---|
| Deploy de la API de bitacora a produccion | 5 | Ambiente de QA sin aprovisionar; no paso de staging {INFERENCIA} | Javier | Aprovisionar QA y promover a prod — 2026-06-16 |
| Migracion de datos de la bitacora vieja | 9 | Decision de esquema pendiente, no es trabajo tecnico bloqueado {INFERENCIA} | Javier | Cerrar decision de esquema en revision del lunes — 2026-06-15 |

## 3. Friccion

- Pipeline de CI falla por flaky tests — **recurrente** (3 semanas seguidas) →
  escala a: aislar y cuarentenar los tests inestables como tarea propia {INFERENCIA}

## 4. Cumplimiento de compromisos previos

- Mergear el refactor del router de cadencias — **cumplido** {ADJUNTO}
- Dejar el deploy de la API de bitacora en produccion — **no-cumplido** (quedo en
  staging; hereda a estancado)
- Documentar la familia de tags Jarvis en references — **cumplido** {DOC}

## 5. Compromisos proxima semana

1. Aprovisionar QA y promover la API de bitacora a produccion — dueno: Javier —
   hecho cuando: la API responde en el dominio de prod con healthcheck verde.
2. Cerrar la decision de esquema de la migracion — dueno: Javier — hecho cuando:
   esquema aprobado y registrado en el ADR de bitacora.
3. Cuarentenar los flaky tests del CI — dueno: Javier — hecho cuando: el pipeline
   pasa 3 corridas seguidas sin reintentos.

## 6. Arrastres

- Definir politica de retencion de bitacora — 3 semanas abierto (desde 2026-W22) —
  escalado a bloqueo; ya no es estancado {POR_CONFIRMAR}

---
**Notas**: el deploy no se declaro verde porque solo llego a staging
(never green-as-success). El arrastre de retencion cruzo el umbral de 3 semanas y
pasa a bloqueo.
