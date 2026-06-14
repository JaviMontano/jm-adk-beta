# Meta prompt — jarvis-bootstrap

Prompt de meta-razonamiento para auto-evaluar una corrida de **jarvis-bootstrap**
antes de declararla completa. Usalo como checklist reflexivo, no como ejecucion.

## Preguntas de control

1. **Destino** — ¿Resolvi una ruta destino inequivoca? Si no, ¿emiti
   `{VACIO_CRITICO}` y me detuve en vez de autocompletar?
2. **Read-before-write** — ¿Lei/inventarie cada archivo antes de plantear su
   Write? ¿Algun Write quedo sin check de existencia previo?
3. **Delta minimo** — ¿El plan es exactamente las piezas faltantes? ¿Toque algo
   que ya existia sin `--force` explicito?
4. **Idempotencia** — Si corriera de nuevo en `missing-only`, ¿daria 0 creados?
5. **Preservacion** — ¿Quedaron intactas ediciones locales, `.local` y
   `user-context`?
6. **Single-brand** — ¿`MEMORY.md` evita mezclar marcas e inventar datos?
7. **Reporte** — ¿Cada artefacto tiene estado correcto, ruta absoluta y tag?
   ¿Algun "creado" corresponde en realidad a una omision?
8. **Evidencia** — ¿Toda afirmacion no trivial usa la familia Jarvis OS y no la
   Alfa?

## Disparadores de correccion
- Cualquier "no" en 1-3 ⇒ detener y rehacer ese paso.
- "Creado" sobre archivo preexistente ⇒ corregir a "omitido".
- Afirmacion no reproducible desde contexto ⇒ etiquetar o eliminar.

## Salida del meta
Un veredicto `gate=pass|fail` con la lista de criterios y su evidencia. Verde sin
evidencia no es exito.
