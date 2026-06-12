# Bootstrap checklist — jarvis-bootstrap

Lista operativa que el guardian recorre antes de declarar `gate=pass`.

## Pre-ejecucion
- [ ] Ruta destino resuelta e inequivoca (si no ⇒ `{VACIO_CRITICO}`, detente).
- [ ] Inventario read-before-write completo de raiz, N0-N4 y semillas.
- [ ] Modo confirmado: `missing-only` (default) o `--force` con diffs revisados.

## Ejecucion
- [ ] Cada Write precedido de check de existencia.
- [ ] Solo se creo el delta; nada preexistente tocado sin `--force`.
- [ ] Ediciones locales, `.local` y `user-context` preservadas.
- [ ] `MEMORY.md` single-brand, sin datos de marca inventados.

## Post-ejecucion
- [ ] `CLAUDE.md` y `MEMORY.md` raiz existen y parsean.
- [ ] N0-N4 presentes; P00/P01/P02 con `CLAUDE.md` local.
- [ ] Reporte: estado + ruta absoluta + tag por artefacto.
- [ ] Idempotencia: segunda corrida missing-only ⇒ 0 creados.
- [ ] Toda afirmacion no trivial etiquetada (familia Jarvis OS).
