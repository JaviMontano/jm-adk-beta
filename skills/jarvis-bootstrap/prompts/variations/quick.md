# Quick variation — jarvis-bootstrap

Modo rapido para un destino conocido y limpio (OS vacio o casi vacio), en
`missing-only`.

## Uso
`jarvis-bootstrap <ruta-destino>`

## Pasos comprimidos
1. Confirma destino. Si falta ⇒ `{VACIO_CRITICO}`, detente.
2. Inventario express (Bash `ls`/Read) de raiz + niveles + semillas.
3. Crea el delta: `CLAUDE.md`, `MEMORY.md`, N0-N4, P00/P01/P02 faltantes —
   cada Write con check previo.
4. Reporte de una linea por artefacto: `estado · ruta_absoluta · tag`.

## Limites
- No `--force` en quick. Si detectas archivos a sobrescribir, escala a `deep`.
- No siembres datos de marca inventados; deja `{AUTOCOMPLETADO}`/`{POR_CONFIRMAR}`.
- Single-brand siempre.
