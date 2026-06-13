# Validation Gate Checklist — frontload-prompt

Checklist operable del gate. El guardian lo recorre antes de declarar READY.
Marca cada ítem; un solo fallo fuerza **BLOCKED** (o degradación de tag).

## Completitud SPEC
- [ ] **S — Situation** presente, con fuente tagueada (`{ADJUNTO}`/`{EXTRAIDO_HILO}`/`{MEMORIA}`).
- [ ] **P — Purpose** presente y en una sola frase.
- [ ] **E — Expectations** presente (formato/límites/criterios).
- [ ] **C — Context** presente (archivos/audiencia/dependencias).
- [ ] Ningún eje vacío sin tag.

## Accionabilidad
- [ ] Purpose accionable: un ejecutor podría arrancar sin re-preguntar.
- [ ] Si Purpose no es inferible → marcado `{VACIO_CRITICO}` y veredicto BLOCKED.

## Disciplina de tags
- [ ] Cada campo derivado/rellenado lleva **exactamente un** tag Jarvis OS `{...}`.
- [ ] Ningún `{WEB}` sin cita (degradar a `{CONOCIMIENTO}` o eliminar).
- [ ] No hay mezcla con la familia Alfa `[...]`.
- [ ] Ante duda entre dos tags, se eligió el más débil.

## Huecos
- [ ] Cero `{VACIO_CRITICO}` pendientes para READY.
- [ ] Cada `{VACIO_CRITICO}` lleva su pregunta mínima de desbloqueo.
- [ ] No se autocompletó más allá de un `{VACIO_CRITICO}`.

## No-ejecución (invariante)
- [ ] No se ejecutó la tarea.
- [ ] No se creó ni sobrescribió ningún archivo del proyecto.

## Veredicto
- [ ] READY o BLOCKED emitido sin ambigüedad.
