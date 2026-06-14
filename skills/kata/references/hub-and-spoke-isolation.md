<!-- distilled from alfa skills/katas-hub-and-spoke-isolation -->
<!-- Aislamiento multi-agente con AgentDefinition y built-in Task; cada subagente arranca con contexto vacio y modelo propio. -->
# Katas Hub And Spoke Isolation

## Qué es

Registrar subagentes como `AgentDefinition` dentro de `ClaudeAgentOptions.agents` y despacharlos a través del built-in Task tool. Cada invocación de Task abre una sesión nueva con su propio `system_prompt`, su propio set de `tools` y su propio `model`. El coordinador (hub) recibe SOLO el último mensaje del subagente como `tool_result`, no su historial interno. [CÓDIGO] Aplica directamente a los escenarios Multi-Agent Research y Code Audit Pipeline.

## Por qué importa (falla que evita)

Pasar todo el historial del coordinador a cada subagente diluye la atención del modelo, filtra políticas y contexto que el subagente no debería ver, multiplica el costo (todo corre con el modelo caro) y aumenta el blast radius de un prompt injection: si un documento envenenado entra a un subagente sin aislamiento, contamina la sesión completa. [INFERENCIA] El aislamiento estructural acota ese radio a una sola tarea. [DOC]

## Supuestos y límites (anti-scope)

- **Supone** un runtime que crea sesión nueva por Task (Claude Agent SDK con `agents` + Task tool); sin ese contrato, el aislamiento es solo convencional vía system prompt y NO se sostiene. [SUPUESTO]
- **No** comparte estado entre spokes: si dos subagentes deben coordinarse, lo hacen vía el hub (su `tool_result`), nunca por memoria compartida. El estado cruzado es responsabilidad del coordinador. [INFERENCIA]
- **No** elimina el prompt injection; acota su radio a una tarea. Un spoke comprometido aún puede devolver un `tool_result` envenenado al hub; el hub debe tratar toda salida de spoke como no confiable. [SUPUESTO]
- **No** es para tareas de un solo paso sin paralelismo ni separación de privilegios: ahí el fan-out por Task añade latencia y turnos sin valor (ver "Cuándo activar").
- **Supone** que el último mensaje del subagente es resumen suficiente; si la síntesis requiere el razonamiento intermedio, el spoke debe emitirlo explícitamente en su mensaje final, no asumir que el hub lo verá. [INFERENCIA]

## Modelo mental

- Topología hub-and-spoke: el coordinador despacha, los especialistas ejecutan con contexto vacío.
- Cada Task es una sesión nueva: el aislamiento es estructural por construcción del runtime, no convencional vía system prompt. [DOC]
- Cada subagente puede tener `tools`, `system_prompt` y `model` distintos (por ejemplo `haiku`, barato, para extracción de hechos). [CÓDIGO]
- El coordinador agrega solo el último mensaje de cada subagente, nunca su historial interno.
- Menos tools y menos contexto por subagente = menor superficie de ataque y menor costo. [INFERENCIA]

Distinción clave **aislamiento estructural vs convencional** (el punto que más se confunde):

| Mecanismo | Garantía | Falla cuando |
|---|---|---|
| Estructural: sesión nueva por Task | el subagente NO puede ver el historial; es físico | nunca, mientras se use Task + `agents` [DOC] |
| Convencional: "no mires el contexto" en system prompt | depende de que el modelo obedezca | un prompt injection lo anula [SUPUESTO] |

## Patrón correcto

```python
extractor = AgentDefinition(
    description="Extrae hechos de UN documento",
    prompt="...",
    tools=[],
    model="haiku",
)
options = ClaudeAgentOptions(
    agents={"extractor": extractor},
    allowed_tools=["Task"],
    max_turns=15,
)
```

`tools=[]` da al spoke cero capacidad de side-effect: solo razona sobre lo que el hub le pasa. Asignar `tools` mínimas por subagente es el control de menor privilegio. [INFERENCIA]

## Anti-patrón

```python
# Un solo agente con TODO el contexto concatenado:
# sin agents, sin Task -> contexto diluido, politicas cruzadas, modelo unico caro.
single_agent(prompt=coordinator_history + all_documents_concatenated)
```

## Modos de fallo (y detección)

- **Aislamiento de mentira**: se declaran `agents` pero el hub concatena su propio historial dentro del `prompt` del Task. Síntoma: el spoke conoce contexto que no se le pasó por parámetro. Detector: el `prompt` del Task no debe incluir historial del coordinador. [SUPUESTO]
- **Fuga por tool_result**: el hub trata la salida del spoke como confiable y la ejecuta sin validar. Un spoke envenenado escala al hub. Tratar todo `tool_result` como entrada no confiable. [INFERENCIA]
- **Modelo caro uniforme**: todos los spokes corren `opus`/`sonnet` aunque la tarea sea extracción trivial. Mata el ahorro que justifica la kata; asignar `haiku` a extracción. [CÓDIGO]
- **Spoke mudo**: el subagente razona bien pero su mensaje final omite el hallazgo; el hub agrega solo ese último mensaje y pierde la señal. El cierre del spoke debe contener el resultado, no el proceso. [INFERENCIA]
- **Fan-out sin límite**: despachar un Task por ítem sin tope agota `max_turns`/presupuesto. Acotar el batch o paginar. [SUPUESTO]

## Argumento de certificación

El aislamiento entre tareas multi-agente es estructural vía `AgentDefinition` + Task, no convencional vía system prompt. Cada Task es una sesión nueva por construcción del SDK: el subagente no hereda el historial del coordinador, el blast radius queda acotado a una tarea, y cada subagente puede asignar un modelo distinto (haiku para extracción, sonnet/opus para síntesis) precisamente porque `AgentDefinition` lo permite. [DOC] Respuestas del quiz: B · B · B.

## Criterios de aceptación

- Cada subagente está declarado como `AgentDefinition` en `ClaudeAgentOptions.agents` y se despacha por Task; ningún spoke recibe el historial del hub en su `prompt`. [CÓDIGO]
- Cada `AgentDefinition` declara `tools` mínimas (idealmente `[]` para extracción) y un `model` proporcional a la tarea (no `opus` por defecto). [CÓDIGO]
- El hub agrega solo el `tool_result` (último mensaje) de cada spoke y lo trata como entrada no confiable. [INFERENCIA]
- El fan-out tiene un tope (`max_turns` o batch acotado); ningún diseño despacha Tasks ilimitados. [SUPUESTO]
- La separación es estructural: el aislamiento no depende de instrucciones en el system prompt. [DOC]

## Cuándo activar

- Multi-Agent Research: coordinador que despacha extracción de hechos por documento.
- Code Audit Pipeline: auditoría con subagentes especializados por dominio (seguridad, estilo, dependencias).
- Cualquier diseño donde se quiera contexto vacío por tarea, modelo distinto por subagente o acotar el blast radius de un prompt injection.
- NO activar para tareas de un solo paso sin paralelismo ni separación de privilegios: el fan-out por Task solo añade latencia.

## Skills relacionadas

- `katas-adaptive-investigation`
- `katas-multiagent-error-propagation`
- `katas-headless-code-review`
