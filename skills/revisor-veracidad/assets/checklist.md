# Checklist del gate — revisor-veracidad

Lista operativa que corre el guardian antes de entregar. Todos los items deben quedar en [x].

## Procedencia
- [ ] Cada afirmacion no obvia tiene exactamente un tag.
- [ ] Una sola familia en todo el documento (Jarvis OS o Alfa core, no ambas).
- [ ] Ortografia de tags (ES vs EN) consistente.

## Correccion de tags
- [ ] Se aplico la regla del tag mas debil donde dos tags eran posibles.
- [ ] Ningun tag fue elevado por encima de lo justificado.
- [ ] Ningun `{WEB}` sin cita (degradado a `{CONOCIMIENTO}` o eliminado).
- [ ] Cita inverificable tratada como `{POR_CONFIRMAR}`, no `{WEB}`.

## Plan de cierre
- [ ] Cada `{SUPUESTO}`/`{POR_CONFIRMAR}` tiene paso concreto (que leer / a quien preguntar / que correr).
- [ ] Owner y artefacto/comando indicados cuando aplica.

## Higiene
- [ ] Sin sobre-tageo (auto-evidentes, input re-citado y estructura sin tag).
- [ ] Contenido no reescrito ni respaldo inventado.
- [ ] `{VACIO_CRITICO}` (si lo hay) detuvo la ejecucion, sin dato fabricado despues.

## Deterministas
- [ ] `scripts/check.sh` pasa sobre `scripts/fixtures/`.
