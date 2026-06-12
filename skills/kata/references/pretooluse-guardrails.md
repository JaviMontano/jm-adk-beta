<!-- distilled from alfa skills/katas-pretooluse-guardrails -->
<!-- Guardarrailes deterministas en hook PreToolUse con permissionDecision deny desde politica recargable, no en el system prompt. -->
# Kata 02 · Guardarrailes deterministas con PreToolUse

## Qué es

Un hook `PreToolUse` registrado en `ClaudeAgentOptions.hooks` inspecciona `tool_name` y `tool_input` ANTES de que la tool se ejecute, y emite `permissionDecision: 'deny'` cuando una política externa (un `dict` o un JSON recargable) lo dicta. La política de negocio vive en código, no en el prompt, y el SDK garantiza que la tool denegada nunca corre. [CÓDIGO]

Escenarios canónicos: Customer Support (reembolsos por encima de un umbral) y Financial Compliance (límites monetarios, dominios prohibidos, paths protegidos). [DOC]

**Alcance.** Define el contrato de un guardarraíl *pre-ejecución*: inspeccionar entrada, decidir `allow`/`deny`/`ask`, garantizar cero side-effects en `deny`. [DOC]
**Anti-alcance.** NO normaliza outputs (eso es Kata 03 `PostToolUse`), NO controla el bucle de turnos (Kata 01 `stop_reason`), NO valida el *resultado* de la tool ni redacta PII de la respuesta. El hook no puede inspeccionar lo que la tool aún no produjo. [INFERENCIA]

## Por qué importa (falla que evita)

Pedir en el `system_prompt` "no aprueben reembolsos mayores a $1000" es solo una sugerencia. Un prompt injection o un usuario insistente la rompe y la tool ejecuta el reembolso de todas formas. El guardarraíl en system prompt no es determinista: depende de que el modelo elija obedecer. El hook `PreToolUse` convierte esa intención en un control estructurado que el SDK aplica fuera del alcance del modelo. [INFERENCIA]

## Modelo mental

- La política vive en código (un `dict` recargable o un JSON en disco), no en el prompt. [CÓDIGO]
- El SDK garantiza que la tool NO corre si el hook retorna `deny`: cero side-effects. [DOC]
- El modelo recibe el `permissionDecisionReason` y replanea con esa información. [DOC]
- `permissionDecision` es estructurado: `allow` / `deny` / `ask`, no texto libre. `ask` delega en un aprobador humano; `allow` explícito corta-circuita hooks posteriores del mismo evento. [CÓDIGO]
- Complementa al `stop_reason` del Kata 01: ese controla el bucle, este controla cada llamada a tool. [INFERENCIA]
- Recarga en caliente: modificar el `dict` o releer el JSON cambia la política sin reiniciar el agente. La relectura debe ocurrir DENTRO del hook, no al import, o la "recarga" nunca surte efecto. [SUPUESTO] Verificar: confirmar que el hook lee el archivo en cada invocación, no una sola vez al cargar el módulo.
- Default-deny vs default-allow: un hook que solo niega casos conocidos deja pasar todo lo demás. Para límites duros, parsear la entrada y negar ante cualquier dato faltante o malformado. [INFERENCIA]

## Patrón correcto

```python
POLICY = {"max_amount": 1000.0}

async def policy_gate(input, tool_use_id, ctx):
    if input["tool_name"] == "process_refund":
        amount = input["tool_input"].get("amount", 0)
        if amount > POLICY["max_amount"]:
            return {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": (
                        f"Refund {amount} exceeds policy limit {POLICY['max_amount']}"
                    ),
                }
            }
    return {}

options = ClaudeAgentOptions(
    hooks={"PreToolUse": [HookMatcher(matcher="*", hooks=[policy_gate])]},
)
```

El `matcher="*"` cubre todas las tools; el `if tool_name` interno discrimina. Devolver `{}` significa "sin opinión" (no es `allow` explícito): otros hooks del evento aún pueden negar. [CÓDIGO]

**Trade-off.** Parsear `amount` con `.get(..., 0)` hace que un payload sin monto pase como `0` y se apruebe. Para un límite duro, el default seguro es `deny` ante campo ausente o no numérico: prefiere bloquear una llamada legítima mal formada antes que aprobar una maliciosa. El costo es algún falso `deny` que el modelo debe corregir reenviando bien la entrada. [INFERENCIA]

## Anti-patrón

```python
# La política vive SOLO en el system prompt, sin hooks.
options = ClaudeAgentOptions(
    system_prompt="No apruebes reembolsos mayores a $1000.",
    # hooks ausentes
)
# Un prompt injection o un usuario insistente rompe la regla
# y process_refund ejecuta de todas formas.
```

Segundo anti-patrón: hook que niega devolviendo prosa o `raise` en vez de `permissionDecision: deny`. Una excepción aborta el turno entero (no es un `deny` limpio que el modelo pueda replanear), y la prosa no es un control estructurado. [INFERENCIA]

## Argumento de certificación

Las políticas críticas (límites monetarios, dominios prohibidos, paths protegidos) viven en hooks `PreToolUse` con `permissionDecision` estructurado, no en system prompts. Un guardarraíl es determinista solo si el SDK puede aplicarlo sin depender de que el modelo elija obedecer. [DOC]

## Casos límite

- **Campo ausente o malformado** (`amount` no numérico, falta la clave): para un límite duro, default `deny` con razón explícita, nunca aprobar por omisión. [INFERENCIA]
- **Tool fuera de la política** (`tool_name` no contemplado): el hook devuelve `{}` y la tool corre; si el riesgo lo exige, usar matcher acotado + allowlist en vez de `*`. [SUPUESTO] Verificar: contrastar contra `assets/permission-decision-policy.json`.
- **Múltiples hooks en el mismo evento:** un `deny` de cualquiera gana; no asumas que el primer `allow` cierra la decisión. [SUPUESTO] Verificar contra el orden de evaluación real del SDK.
- **Recarga en caliente con JSON corrupto:** releer un archivo a medio escribir puede lanzar; envolver en try/except y caer a la última política válida o a `deny`, nunca a sin-política. [INFERENCIA]
- **`ask` sin aprobador conectado:** si no hay canal de aprobación humana, `ask` cuelga o degrada; en headless tratar `ask` como `deny`. [SUPUESTO] Verificar: comportamiento de `ask` en modo no interactivo.

## Contrato determinístico

- La política debe vivir en `dict` o JSON recargable, nunca sólo en `system_prompt`. [DOC]
- El hook debe declarar `event_name: PreToolUse`, estar registrado y bloquear antes de ejecutar la tool. [CÓDIGO]
- Todo `deny` debe incluir `permissionDecisionReason` y evidencia de cero side-effects. [DOC]
- Todo reporte debe incluir al menos un caso `deny` y un caso `allow`. [DOC]
- La validación offline usa `assets/pretooluse-guardrail-contract.json`, `assets/permission-decision-policy.json`, `assets/policy-source-policy.json`, `assets/side-effect-policy.json` y `assets/evidence-policy.json`. [CONFIG]
- Comando local: `bash skills/katas-pretooluse-guardrails/scripts/check.sh`. [CÓDIGO]

## Acceptance criteria

- La política es recargable y externa al prompt; cambiarla no requiere reiniciar el agente. [DOC]
- Cada `deny` lleva `permissionDecisionReason` y la tool no produjo side-effect alguno (verificable en el log). [DOC]
- Entradas ausentes o malformadas resuelven a `deny`, no a `allow` por omisión. [INFERENCIA]
- El reporte cubre al menos un `deny` y un `allow`; el hook discrimina por `tool_name`. [DOC]
- Cero ramas de control que dependan de prosa del modelo o del system prompt. [DOC]

## Cuándo activar

- Hay un límite duro de negocio (montos, dominios, rutas) que NO puede romperse. [DOC]
- Se necesita bloquear una tool ANTES de que produzca side-effects. [DOC]
- Una política debe recargarse en caliente sin reiniciar el agente. [DOC]
- Se audita un agente cuya seguridad descansa solo en el prompt. [DOC]

## Skills relacionadas

- `katas-deterministic-agentic-loop`
- `katas-posttooluse-normalization`
- `katas-mcp-structured-errors`
