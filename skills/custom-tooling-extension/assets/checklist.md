# Checklist de gate — custom-tooling-extension

Marca cada ítem solo con evidencia (verde-con-evidencia, nunca verde-por-defecto).

- [ ] **Clasificación.** command (disparo explícito) vs skill (activación contextual) decidido por el tipo de trigger. [DOC]
- [ ] **Scope.** project (`.claude/` versionado) si se replica al equipo; user solo para experimentos personales. [DOC]
- [ ] **Economía de contexto.** `context: fork` en skills de trabajo no trivial. [DOC]
- [ ] **Blast radius.** `allowed-tools` whitelist mínima; read-only salvo `Bash`/mutaciones justificadas inline. [DOC]
- [ ] **Interfaz/routing.** `description` en una sola línea (contrato de routing) + `argument-hint` presente. [DOC]
- [ ] **Convención.** Reglas permanentes en `CLAUDE.md`, no incrustadas en la skill. [DOC]
- [ ] **Frontmatter.** YAML válido, `name` único, `description` en una línea. [INFERENCIA]
- [ ] **Upgrade-safe.** Modificaciones preservan `name`/id, no rompen rutas `.claude/`, minor-bump de `version`. [DOC]
- [ ] **Datos faltantes.** Si no se sabe equipo o mutación, se preguntó antes de emitir scope/whitelist. [SUPUESTO]
