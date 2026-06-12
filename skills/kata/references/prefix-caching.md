<!-- distilled from alfa skills/katas-prefix-caching -->
<!-- Prefix caching: estatico-first y dinamico-last; interpretar cache_creation vs cache_read input tokens para estimar ahorro. -->
# Katas Prefix Caching

## Qué es

La API de Claude reusa el cache KV cuando el prefijo del prompt es idéntico byte a byte turno a turno. [DOC] Si organizas el contexto como estático primero y dinámico al final, el prefijo estable entra en cache y sus lecturas se facturan ~10x más barato que tokens de input normales. [DOC] El cache se activa marcando los bloques estables con `cache_control: {type: "ephemeral"}`, y la métrica de éxito vive en `usage`: `cache_creation_input_tokens` (lo escrito al cache) frente a `cache_read_input_tokens` (lo leído del cache). [CONFIG]

## Por qué importa (falla que evita)

Insertar la fecha actual o un `user_id` al inicio del prompt invalida el cache en cada llamada. [INFERENCIA] El contenido es el mismo, pero el costo de input se multiplica hasta ~10x sin que el log de la aplicación lo evidencie: no hay error, no hay excepción, solo una factura silenciosamente inflada. [INFERENCIA] Es una fuga de costo invisible que solo se detecta auditando los `usage` tokens. [INFERENCIA]

## Modelo mental

- **Estático** = system prompt, `CLAUDE.md`, tool definitions, contexto pesado del repo. Va arriba. [INFERENCIA]
- **Dinámico** = input del usuario, timestamps, estado efímero del turno. Va abajo. [INFERENCIA]
- **Regla:** estático arriba (prefix-first), dinámico abajo (suffix-last). [INFERENCIA]
- El borde dinámico se aísla con tags XML: `<reminder>now: ...</reminder>`. [INFERENCIA]
- **Invalidación encadenada:** cambiar UN solo carácter invalida el cache desde ese punto en adelante; por eso lo volátil nunca puede ir antes de lo estable. [DOC]
- **Granularidad:** el cache es por bloque marcado; el prefijo cacheado debe superar el mínimo de tokens del modelo o el `cache_control` es inerte (no escribe cache). [CONFIG] Verificar el umbral vigente por modelo antes de asumir hit.
- **TTL:** el cache ephemeral expira (~5 min de inactividad por defecto); tráfico intermitente puede pagar `cache_creation` repetido sin lograr `cache_read`. [DOC]
- **Métrica:** ahorro ≈ `cache_read_input_tokens` × (1 − 0.1) sobre el costo base; comparar contra `cache_creation_input_tokens` (escritura cuesta ~1.25x input) para saber si el reuso amortiza la escritura. [CONFIG]

## Patrón correcto

```python
messages = [
    {"role": "system", "content": SYSTEM_PROMPT_BIG_AND_STABLE},
    {"role": "user", "content": REPO_CONTEXT_BIG},
    *prior_turns,
    {"role": "user", "content": f"<reminder>now: {now}</reminder>\n{user_input}"},
]

client.messages.create(
    system=[{
        "type": "text",
        "text": SYSTEM_PROMPT_BIG_AND_STABLE,
        "cache_control": {"type": "ephemeral"},
    }],
    messages=messages,
)
```

## Anti-patrón

```python
# ANTI: fecha al inicio invalida el cache en cada llamada
system_content = f"Today is {datetime.now()}..." + SYSTEM_PROMPT
```

El timestamp al frente reescribe el prefijo cada turno: mismo contenido, ~10x más caro. [INFERENCIA]

## Supuestos y límites (anti-scope)

- Solo amortiza cuando el prefijo estable es grande y se reutiliza varias veces dentro del TTL; prompts cortos o de un solo turno no recuperan el sobrecosto de escritura. [SUPUESTO]
- El prefijo debe ser idéntico byte a byte: serialización no determinista de tools/JSON (orden de claves, espacios) rompe el hit aunque el contenido sea equivalente. [INFERENCIA] Fijar la serialización antes de medir.
- NO reduce tokens de output ni latencia de generación; solo abarata input cacheado. [DOC]
- Mover `prior_turns` o editar un mensaje histórico invalida desde ese punto; mantener el historial append-only para preservar el prefijo. [INFERENCIA]
- Precios y umbrales (mínimo de tokens, multiplicador de escritura, TTL) varían por modelo y cambian: tratarlos como parámetros a verificar, no como constantes. [SUPUESTO]

## Criterios de aceptación

- En tráfico estable, `cache_read_input_tokens > 0` y crece con cada turno; `cache_creation_input_tokens` ocurre una vez por prefijo, no por llamada. [CONFIG]
- Inyectar un timestamp al inicio del system y observar que `cache_read` cae a 0 — confirma que el dato dinámico migró correctamente al sufijo cuando el read se restaura. [INFERENCIA]
- El `<reminder>` dinámico queda estrictamente al final del último mensaje; nada volátil lo precede. [INFERENCIA]

## Modos de fallo

- **Hit silencioso a cero:** prefijo bajo el mínimo de tokens → `cache_control` no escribe; síntoma: `cache_creation` y `cache_read` ambos en 0. [CONFIG]
- **Thrash por TTL:** llamadas espaciadas > TTL → solo `cache_creation` repetido, nunca `cache_read`; el cache cuesta más que no usarlo. [INFERENCIA]
- **Invalidación por cola:** un middleware que reordena tools o reescribe el system por request rompe el prefijo sin aviso. [INFERENCIA] Auditar `usage` tras cada cambio de plataforma.

## Argumento de certificación

Para certificar esta kata hay que: enunciar la regla "estático-prefix-first, dynamic-suffix-last"; y saber interpretar `cache_creation_input_tokens` vs `cache_read_input_tokens` en `usage` para estimar el ahorro (~10x en lecturas). [CONFIG] Quien certifica explica por qué un valor dinámico al inicio (timestamp, `user_id`) rompe el prefix caching, por qué cambiar un carácter invalida desde ese punto en adelante, dónde se ubica el dato dinámico (al final, aislado en un tag `<reminder>`), y cuándo el caching NO amortiza (prefijo pequeño, un solo turno, tráfico fuera de TTL). [INFERENCIA]

## Cuándo activar

Activa esta skill cuando el trabajo toque organización del prompt para reuso de cache KV, `cache_control` ephemeral, prefijo estático vs sufijo dinámico, o interpretación de los tokens de cache en `usage`. Escenarios típicos: Customer Support y Developer Productivity con prompts grandes y estables reutilizados turno a turno. [INFERENCIA]

## Skills relacionadas

- `katas-context-dilution-mitigation`
- `katas-persistent-scratchpad`
- `katas-multipass-prompt-chaining`
