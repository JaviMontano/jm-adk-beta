# Ejemplo de entrada — revisor-veracidad

## Encargo

Audita el siguiente borrador antes de enviarlo. Audiencia: operador (usa el set Jarvis OS). Marca procedencia y propon el cierre de lo no verificable.

## Audiencia

operador -> familia Jarvis OS.

## Fuentes disponibles

- Hilo de la conversacion actual (donde el lead "aprobo ayer").
- Acceso al repo del servicio de pagos y a `scripts/check.sh`.
- Sin acceso a metricas de produccion en este momento.

## Texto a auditar

> El endpoint `/pagos` responde en 40ms y el equipo lo aprobo ayer. Migramos a Postgres 16
> el mes pasado y desde entonces el throughput subio un 30%. Segun un estudio reciente, la
> mayoria de los equipos del sector ya usa colas asincronas. Asumimos que el pico de Black
> Friday sera similar al del ano pasado.

## Resultado esperado (resumen)

- `40ms` -> `{POR_CONFIRMAR}` (no hay metrica de produccion a mano; cierre: benchmark/p50).
- `el equipo lo aprobo ayer` -> `{EXTRAIDO_HILO}` (esta en el hilo).
- `Migramos a Postgres 16 el mes pasado` -> `{POR_CONFIRMAR}` (verificable en repo/changelog).
- `throughput subio 30%` -> `{POR_CONFIRMAR}` (numero derivado sin fuente a mano).
- `Segun un estudio reciente...` -> `{WEB}` sin cita -> degradar a `{CONOCIMIENTO}` o eliminar.
- `Asumimos que el pico...` -> `{SUPUESTO}` (asuncion explicita; cierre: comparar con datos del ano anterior).
