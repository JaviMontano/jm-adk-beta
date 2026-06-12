# Ejemplo de salida — revisor-veracidad

- **Familia usada**: Jarvis OS
- **Audiencia**: operador
- **Fecha**: 2026-06-11
- **Estado**: COMPLETO

## 1. Texto auditado

> El endpoint `/pagos` responde en 40ms `{POR_CONFIRMAR}` y el equipo lo aprobo ayer `{EXTRAIDO_HILO}`.
> Migramos a Postgres 16 el mes pasado `{POR_CONFIRMAR}` y desde entonces el throughput subio un 30% `{POR_CONFIRMAR}`.
> La mayoria de los equipos del sector ya usa colas asincronas `{CONOCIMIENTO}`. Asumimos que el pico de Black
> Friday sera similar al del ano pasado `{SUPUESTO}`.

Nota: la frase original "Segun un estudio reciente..." era `{WEB}` sin cita; al no haber link verificable se degrado a `{CONOCIMIENTO}` y se reformulo sin atribuir el estudio. No se invento la fuente.

## 2. Plan de verificacion

| # | Claim (extracto) | Tag | Paso de cierre concreto | Owner | Artefacto/comando |
|---|---|---|---|---|---|
| 1 | responde en 40ms | `{POR_CONFIRMAR}` | Correr benchmark contra `/pagos` y registrar el p50 real | Backend | `scripts/check.sh` / herramienta de load test |
| 2 | Migramos a Postgres 16 el mes pasado | `{POR_CONFIRMAR}` | Verificar fecha en el changelog/migracion del repo | Backend | repo: `db/migrations/` |
| 3 | throughput subio un 30% | `{POR_CONFIRMAR}` | Comparar metricas pre/post migracion en el dashboard | SRE | panel de observabilidad |
| 4 | pico Black Friday similar al ano pasado | `{SUPUESTO}` | Contrastar con el trafico real del Black Friday anterior | Producto | dataset historico de trafico |

## 3. Resumen

- **Conteo por tag**:
  - `{EXTRAIDO_HILO}`: 1
  - `{POR_CONFIRMAR}`: 3
  - `{CONOCIMIENTO}`: 1
  - `{SUPUESTO}`: 1
  - resto: 0
- **Familia**: Jarvis OS (una sola, ortografia consistente)
- **Bloqueos `{VACIO_CRITICO}`**: ninguno
- **Limites declarados**: ninguno legal/medico/financiero/seguridad en este texto.

## 4. Gate (auto-chequeo)

- [x] Un tag por afirmacion no obvia, una sola familia.
- [x] Ningun `{WEB}` sin cita (el unico se degrado a `{CONOCIMIENTO}`); ningun `{VACIO_CRITICO}` con dato fabricado.
- [x] Cada `{SUPUESTO}`/`{POR_CONFIRMAR}` con paso concreto.
- [x] Ortografia de tags consistente.
- [x] Sin sobre-tageo; contenido no reescrito (solo se elimino la atribucion al estudio sin cita).
