# Example input — jarvis-bootstrap

## Peticion del operador

> Completa el Jarvis OS en `/Users/jm/jarvis-os`. Ya edite a mano el `CLAUDE.md`
> raiz y no quiero perderlo. Modo seguro. Operador: Javier; marca activa: JM Labs;
> objetivo del OS: laboratorio de innovacion personal.

## Estado observado del destino (inventario)

```
/Users/jm/jarvis-os
├── CLAUDE.md            # existe, editado a mano por el operador
└── N0/                  # existe, vacio
```

Faltan: `MEMORY.md` raiz, contenido de N0, niveles N1-N4, semillas P00/P01/P02 y
sus `CLAUDE.md` locales.

## Parametros derivados

- **Destino**: `/Users/jm/jarvis-os` `{EXTRAIDO_HILO}`
- **Modo**: `missing-only` ("modo seguro") `{EXTRAIDO_HILO}`
- **Operador**: Javier `{EXTRAIDO_HILO}`
- **Marca activa**: JM Labs (single-brand) `{EXTRAIDO_HILO}`
- **Objetivo**: laboratorio de innovacion personal `{EXTRAIDO_HILO}`

## Expectativa

Omitir `CLAUDE.md` (ya existe), crear el resto del delta, sembrar `MEMORY.md` con
los datos reales del operador, y emitir el reporte de bootstrap. Cero
sobrescrituras.
