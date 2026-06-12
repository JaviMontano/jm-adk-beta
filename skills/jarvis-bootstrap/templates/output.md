# Reporte de bootstrap — Jarvis OS

> Plantilla del entregable de `jarvis-bootstrap`. Rellena cada campo; toda
> afirmacion no trivial lleva su tag de la familia Jarvis OS.

## Resumen de ejecucion

- **Destino**: `<ruta absoluta del Jarvis OS>`
- **Modo**: `missing-only` | `--force`
- **Operador**: `<nombre>` `{POR_CONFIRMAR}`
- **Marca activa**: `<marca>` (single-brand) `{EXTRAIDO_HILO}`
- **Fecha**: `<YYYY-MM-DD>`
- **Veredicto del gate**: `pass` | `fail`

## Conteo

| Estado | Total |
|--------|-------|
| creado | `<n>` |
| omitido (ya existe) | `<n>` |
| sobrescrito (--force) | `<n>` |

## Detalle por artefacto

| Artefacto | Ruta absoluta | Estado | Tag |
|-----------|---------------|--------|-----|
| CLAUDE.md raiz | `<ruta>` | creado / omitido / sobrescrito | `{INFERENCIA}` |
| MEMORY.md raiz | `<ruta>` | ... | `{MEMORIA}` |
| N0 | `<ruta>` | ... | ... |
| N1 | `<ruta>` | ... | ... |
| N2 | `<ruta>` | ... | ... |
| N3 | `<ruta>` | ... | ... |
| N4 | `<ruta>` | ... | ... |
| P00/CLAUDE.md | `<ruta>` | ... | `{AUTOCOMPLETADO}` |
| P01/CLAUDE.md | `<ruta>` | ... | `{AUTOCOMPLETADO}` |
| P02/CLAUDE.md | `<ruta>` | ... | `{AUTOCOMPLETADO}` |

## Gate de aceptacion

- [ ] `CLAUDE.md` y `MEMORY.md` raiz existen y son parseables.
- [ ] Niveles N0-N4 presentes; semillas P00/P01/P02 con `CLAUDE.md` local.
- [ ] Cero sobrescrituras salvo `--force` explicito.
- [ ] Reporte enumera cada artefacto con estado y ruta absoluta.
- [ ] Cada afirmacion no trivial etiquetada.

## Diffs (solo si --force)

- `<diff_id>`: `<artefacto>` — resumen de cambios y justificacion.

## Preservado intacto

- Ediciones locales / `.local` / `user-context`: `<lista>` `{MEMORIA}`

## Pendientes y vacios criticos

- `{POR_CONFIRMAR}`: `<dato>`
- `{VACIO_CRITICO}`: `<dato terminal, si lo hubo>`
