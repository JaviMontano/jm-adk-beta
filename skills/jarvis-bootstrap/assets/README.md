# Assets — jarvis-bootstrap

Recursos deterministas que respaldan el gate de calidad del skill. No contienen
contenido de negocio; solo soportan la validacion del andamiaje del Jarvis OS.

## Contenido

- **`checklist.md`** — lista operativa que el guardian recorre (pre-ejecucion,
  ejecucion, post-ejecucion) antes de declarar `gate=pass`. Consumida por el
  `guardian` y por el procedimiento de `SKILL.md`.
- **`quality-rubric.json`** — rubrica ponderada de criterios de aceptacion
  (contrato raiz parseable, esqueleto completo, cero sobrescrituras no
  autorizadas, reporte trazable, evidencia etiquetada, idempotencia). Consumida
  por el `guardian` para puntuar la corrida.
- **`manifest.json`** — indice declarativo de estos activos y sus consumidores.

## Uso

El guardian carga `quality-rubric.json` para evaluar la corrida y `checklist.md`
para no omitir pasos. Cada activo declara su `used_by` en `manifest.json`.
