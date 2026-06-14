# Ejemplo — Entrada

Petición del equipo de plataforma:

> "Quiero que cualquiera del equipo pueda pedirle a Claude que genere las notas
> de versión leyendo el `git log` entre dos tags. Que no infle la sesión
> principal porque a veces el log es enorme, y que **no** pueda borrar ni
> modificar nada del repo: solo leer. Los dos tags se los paso yo como
> argumentos."

Contexto adicional capturado por la skill:

- **Disparo:** no se invoca por nombre fijo; se pide en lenguaje natural ("genera las release notes entre v1.2 y v1.3"). → activación contextual.
- **Replicación:** debe servir a todo el equipo. → project scope.
- **Operaciones:** lectura de `git log` (necesita `Bash` para `git`, pero solo lectura).
- **Argumentos:** dos tags (`<tag-desde> <tag-hasta>`).
- **Riesgo:** el log puede inflar la sesión principal. → necesita aislamiento.
