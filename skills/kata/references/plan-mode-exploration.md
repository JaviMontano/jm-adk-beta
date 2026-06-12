<!-- distilled from alfa skills/katas-plan-mode-exploration -->
<!-- Exploracion segura en Plan Mode read-only con plan.md firmado por humano antes de transicionar a escritura. -->
# Katas Plan Mode Exploration

## Qué es

Antes de modificar un repositorio desconocido, el agente entra en Plan Mode (solo-lectura). Explora el código, mapea convenciones y escribe un `plan.md` con hallazgos y arquitectura propuesta. Obtiene aprobación humana directa sobre ese plan antes de transicionar a modo escritura (Direct). El artefacto de aprobación es texto auditable, no un "ok" verbal. [DOC]

**Alcance.** Define la frontera read-only/write y su transición firmada. NO cubre: qué tools de escritura denegar por archivo (`katas-path-conditional-rules`), el mecanismo genérico del hook `PreToolUse` (`katas-pretooluse-guardrails`), ni cómo se persiste el contexto entre sesiones (`katas-session-resume-fork`). [DOC]

## Por qué importa (falla que evita)

Lanzar un agente con permisos de escritura sobre un repo desconocido es destrucción probabilística: el primer error de razonamiento borra archivos clave o reescribe convenciones, y recuperar es caro. [INFERENCIA] Plan Mode separa exploración de mutación: el agente puede equivocarse al razonar sin tocar el disco, y el humano revisa el plan antes de que cualquier herramienta destructiva se habilite. [DOC]

## Modelo mental

- Dos modos discretos: read-only (Plan) y write (Direct). La transición es explícita y registrada. [DOC]
- En Plan Mode las herramientas de escritura están deshabilitadas por hook, no desaconsejadas por prosa: el hook niega, no recuerda una cortesía. [CÓDIGO]
- El artefacto de aprobación es un `plan.md` firmado por humano, texto auditable y diffeable. [DOC]
- Aprobación = firma + plan congelado. Cualquier cambio al plan re-pide aprobación. [DOC]
- Los hooks aplican el modo (barrera dura); el `system_prompt` orienta el comportamiento pero NO es la barrera de seguridad. [INFERENCIA]

## Patrón correcto

```python
options = ClaudeAgentOptions(
    permission_mode="plan",
    allowed_tools=["Read", "Glob", "Grep"],
    system_prompt=(
        "En Plan Mode: explora, mapea, redacta plan.md. NO escribas código."
    ),
)

# hook PreToolUse niega escritura mientras el modo sea plan:
write_tools = {"Write", "Edit", "NotebookEdit", "Bash"}
def pre_tool_use(tool_name, mode):
    if tool_name in write_tools and mode == "plan":
        return {"permissionDecision": "deny"}
    return {"permissionDecision": "allow"}
```

La transición a `permission_mode` de escritura ocurre solo después de que un humano firma `plan.md`. Si el plan cambia, se vuelve a Plan Mode, se actualiza `plan.md` y se re-pide aprobación. [DOC] `Bash` se deniega entero en plan porque un comando read-only (`cat`, `grep`) y uno destructivo (`>`, `rm`, `git checkout`) comparten la misma tool: el hook no puede distinguirlos sin parsear shell, así que la regla segura es negar `Bash` y exponer lectura vía `Read`/`Glob`/`Grep`. [INFERENCIA]

## Anti-patrón

```python
options = ClaudeAgentOptions(
    permission_mode="bypassPermissions",
    allowed_tools=["Read", "Write", "Edit", "Bash"],  # escritura desde el inicio
)
```

Arrancar en `bypassPermissions` con herramientas de escritura habilitadas sobre un repo desconocido elimina la fase de exploración segura y entrega el disco al primer error de razonamiento. [DOC] Igual de roto: confiar la regla "no escribas" SOLO al `system_prompt` sin hook — un prompt injection o una instrucción ambigua la salta y la escritura ejecuta igual. [INFERENCIA]

## Decisión y trade-off

Negar `Bash` completo en Plan Mode bloquea lectura legítima vía shell (un `git log`, un `ls`). El trade-off es deliberado: se prefiere falso-negativo de exploración (una lectura bloqueada que se reencauza por `Grep`/`Glob`) sobre falso-positivo de seguridad (un `Bash` "de lectura" que resultó destructivo). El costo es fricción menor; el beneficio es que la barrera no depende de inspeccionar argumentos. [INFERENCIA]

## Casos límite y fallas

- **Plan aprobado, luego el plan cambia:** firma vieja sobre plan nuevo NO vale. Volver a Plan Mode, actualizar `plan.md`, re-firmar; tratar la divergencia plan↔firma como bloqueo, no como advertencia. [DOC]
- **`Bash` "solo lectura" en plan:** se deniega igual; no hay clasificación por argumento. Exponer la lectura por `Read`/`Glob`/`Grep`. [CÓDIGO]
- **Tool nueva de escritura no listada en `write_tools`:** el set es allowlist invertida y puede quedar incompleto. Default seguro: en modo plan denegar todo lo que no esté en `allowed_tools` de lectura, en vez de enumerar escrituras. [SUPUESTO] Verificar contra la superficie de tools del runtime.
- **Aprobación verbal ("dale, hazlo") sin `plan.md` firmado:** no transiciona. Sin artefacto auditable no hay firma; la transición exige texto, no consentimiento de chat. [DOC]
- **Mutación encubierta vía MCP/tool externa:** una tool de servidor MCP con efecto de escritura no aparece en `write_tools`. La denegación debe basarse en el modo + allowlist de lectura, no en una lista fija de nombres locales. [INFERENCIA]

## Argumento de certificación

Plan Mode es un contrato de dos modos read-only/write con transición firmada por humano, no un "modo de cortesía". Los hooks aplican el modo: enumeran las tools de escritura (`Write`, `Edit`, `NotebookEdit`, y `Bash` con redirecciones) y las deniegan mientras el modo sea plan. El artefacto de aprobación es `plan.md` firmado; cambios al plan re-piden aprobación. [DOC]

## Criterios de aceptación

- En `permission_mode="plan"`, toda tool de escritura (incluido `Bash`) retorna `permissionDecision: "deny"` por hook, no por prosa. [CÓDIGO]
- La transición a modo escritura es imposible sin un `plan.md` firmado por humano; la firma es texto auditable, no verbal. [DOC]
- Cualquier cambio al plan tras la firma invalida la firma y fuerza re-aprobación. [DOC]
- La negación de escritura proviene del hook + allowlist de lectura, de modo que una tool de escritura no enumerada igual queda bloqueada. [SUPUESTO]

## Cuándo activar

- Vas a operar sobre un repositorio o base de código desconocida o crítica. [DOC]
- Necesitas explorar y proponer arquitectura antes de mutar nada. [DOC]
- El flujo exige aprobación humana explícita antes de escribir. [DOC]
- Quieres una barrera dura (hook) contra escritura accidental durante exploración. [DOC]

## Skills relacionadas

- `katas-hierarchical-claude-memory`
- `katas-custom-commands-skills`
- `katas-session-resume-fork`
