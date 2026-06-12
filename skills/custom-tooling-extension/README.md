# custom-tooling-extension

## Qué hace

Decide **slash command vs skill** y escribe su frontmatter de producción con el
scope correcto: `context: fork` para economizar la ventana, `allowed-tools`
como whitelist mínima para acotar el blast radius, y `argument-hint` /
`description` como contrato de interfaz y de routing. La capacidad no es
"escribir un `.md`": es clasificar el artefacto por **tipo de disparo** y por
**ámbito de replicación**, sin contaminar la sesión ni romper la replicabilidad
del equipo.

## Cuándo usarla

- Disparador explícito invocado por nombre (`/comando arg`) → candidato a slash command.
- Activación por contexto/semántica, con ventana propia y herramientas acotadas → skill con `context: fork`.
- El artefacto debe replicarse a todo el equipo vía repo → scope **project** (`.claude/commands/`, `.claude/skills/`), nunca user.
- Una skill ejecuta operaciones que pueden mutar repo/sistema y hay que restringir el blast radius con `allowed-tools`.
- Mover convenciones permanentes (no condicionales) del proyecto fuera de la skill, hacia `CLAUDE.md`.

**No usarla cuando** el pedido es de dominio no-tooling (correos, análisis,
contenido); el input está vacío; o piden explícitamente violar las reglas (user
scope para artefacto de equipo, sin fork, sin `allowed-tools`) — ahí no actives:
explica el anti-patrón en vez de obedecerlo.

## Cómo enruta / ejecuta

1. Clasifica el artefacto: disparo explícito y predecible → command; activación por contexto + economía de ventana + herramientas acotadas → skill con `context: fork`.
2. Fija el scope: ¿se replica al equipo? → `.claude/` versionado (project). User scope solo para experimentos personales.
3. Declara la interfaz: `argument-hint` para el invocante; en skill, `description` como contrato de routing en una línea.
4. Aísla el contexto con `context: fork` en sub-tareas no triviales.
5. Whitelist de herramientas: `allowed-tools` con el mínimo; read-only salvo justificación explícita para `Bash`/mutaciones.
6. Separa convención de capacidad: reglas permanentes → `CLAUDE.md`; la skill solo capacidad condicional.
7. Valida contra el checklist-gate de `SKILL.md` (y la rúbrica de `assets/`) antes de mergear.

## Referencias

- `SKILL.md` — capacidad, disambiguador command vs skill, patrón/anti-patrón, checklist-gate, upgrade-safety.
- `knowledge/body-of-knowledge.md` — conceptos clave (command vs skill, scope, fork, blast radius), estándares de frontmatter y reglas de decisión.
- `knowledge/knowledge-graph.json` — grafo de los conceptos del dominio.
- `prompts/` — prompt primario, meta-prompt y variaciones quick/deep.
- `templates/output.md` — scaffold del entregable (decisión + frontmatter + checklist).
- `examples/` — ejemplo trabajado de entrada y salida.
- `assets/` — rúbrica de calidad, checklist de gate y manifest del bundle (ver `assets/README.md`).

## Taxonomía de evidencia

Cada afirmación se etiqueta: `[DOC]` regla documentada del modelo de extensiones,
`[CONFIG]` valor de frontmatter o ruta `.claude/`, `[CÓDIGO]` snippet de
frontmatter/command emitido, `[INFERENCIA]` deducción de diseño, `[SUPUESTO]`
dato faltante que obliga a preguntar antes de emitir.
