# Ejemplo de entrada — daily-close

Operador dispara `cierre-diario` al final de la jornada. Workspace activo:
`jm-claude-desktop-workspace`. Fecha no especificada (se autocompleta hoy).

## Fuente del dia (TAREAS.md, fragmento)

```
- [x] Migrar dashboard-serve.sh a ruta absoluta (commit 9f2a1c)
- [x] Revisar PR #214 del bridge de Claude Desktop — aprobado y mergeado
- [ ] Cablear notebooklm export al pipeline de cierre — frene: falta token de auth
- [ ] Redactar seccion "memory boundary" en jm-labs-runtime.md
- [ ] Probar doctor.sh end-to-end en macOS 15
```

## Notas sueltas del hilo

- Aprendi que `dashboard-serve.sh` fallaba por `cd` relativo cuando el cron lo
  invoca desde otro cwd; moverlo a ruta absoluta lo arregla. Aplica al resto de
  scripts del workspace.
- El export de NotebookLM necesita `nlm login` previo; el token expira en sesiones
  largas. Bloqueo real hasta re-autenticar.

## Destino de persistencia

`/Users/.../jm-claude-desktop-workspace/workspaces/tasks/MEMORY.md` (append).
