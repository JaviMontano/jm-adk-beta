# Prompt — Meta (monthly-audit)

Meta-prompt para configurar/afinar una corrida de la auditoria P22 antes de
ejecutar el prompt primario.

## Decisiones a resolver
1. **Alcance temporal**: ¿mes calendario completo o ventana parcial? Si el mes no
   es explicito, autocompleta el mes en curso y marca `{AUTOCOMPLETADO}`.
2. **Workspace objetivo**: uno solo. Si hay varios candidatos, pide eleccion; no
   fusiones salud de marcas/proyectos (disciplina de marca unica).
3. **Disponibilidad de baseline**: ¿existe auditoria del mes previo? Determina si
   habra delta o n/a.
4. **Fuentes de evidencia**: confirma que MEMORY.md, TAREAS.md, bitacora y commits
   son accesibles. Si falta una obligatoria → `{VACIO_CRITICO}`.
5. **Destino de persistencia**: bitacora del workspace; modo append, missing-only.

## Auto-chequeo de calidad del prompt
- ¿El prompt fuerza evidencia ligada por score? (debe).
- ¿Limita acciones a 3? (debe).
- ¿Exige un tag por afirmacion y una sola familia? (debe).
- ¿Prohibe sobrescribir historico? (debe).

## Salida del meta
Una configuracion explicita (mes, workspace, baseline si/no, fuentes, destino)
que alimenta `prompts/primary.md`. Marca cada supuesto con su tag.
