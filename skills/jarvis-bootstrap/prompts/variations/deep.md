# Deep variation — jarvis-bootstrap

Modo exhaustivo para un OS **parcial o sensible**, donde puede haber ediciones
locales valiosas y/o una peticion de `--force`.

## Uso
`jarvis-bootstrap <ruta-destino> [--force] [contexto: operador, marca, objetivo]`

## Pasos
1. **Discover completo** — inventario detallado con Read de cada `CLAUDE.md`
   local existente, `MEMORY.md`, niveles y semillas. Detecta `.local` y
   `user-context`. Si falta destino ⇒ `{VACIO_CRITICO}`.
2. **Delta + diffs** — calcula faltantes. Si se pide `--force`, genera y muestra
   el **diff** de cada archivo a sobrescribir y pide confirmacion explicita. Ante
   conflicto, prevalece `missing-only`.
3. **Siembra contextual** — si hay contexto de operador/marca, instruye al
   specialist para poblar `MEMORY.md` con datos reales (single-brand);
   lo no confirmado va con `{POR_CONFIRMAR}`.
4. **Execute** — Write/Edit del delta (+ sobrescrituras confirmadas), cada uno
   con check previo; aborta antes de escritura parcial si hay permisos/ruta no
   escribible.
5. **Validate exhaustivo** — re-inventario post-ejecucion, prueba de idempotencia
   (segunda corrida missing-only = 0 creados), single-brand, y el gate completo
   con evidencia por criterio.

## Reporte
Tabla por artefacto: `estado · ruta_absoluta · tag · (diff_id si --force)`.
