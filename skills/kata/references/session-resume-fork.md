<!-- distilled from alfa skills/katas-session-resume-fork -->
<!-- Gestion de sesiones: resume vs fork vs fresh con summary tipado; detectar cuando los tool results estan stale. -->
# Kata 25 · Gestión de Sesiones (Resume y Fork)

## Qué es

Tres patrones de preservación de contexto entre invocaciones del agente, y el criterio para elegir entre ellos:

- `--resume` continúa una sesión nombrada: el contexto previo sigue siendo válido y la conversación avanza lógicamente.
- `fork` crea ramas paralelas desde una baseline común: dos caminos independientes, cero interferencia entre ramas.
- Sesión nueva con summary tipado inyectado en el system prompt: preferible cuando los tool results previos pueden estar stale, porque el mundo cambió desde la última sesión.

El scratchpad estructurado (Kata 18) es la fuente natural del summary que se inyecta en la sesión fresh.

## Por qué importa (falla que evita)

Resumir una sesión vieja cuyos tool results están stale lleva al modelo a referenciar archivos que ya no son lo que cree que son: recuerda el código como estaba antes de un refactor masivo y alucina sobre estado obsoleto. Los forks sin disciplina se mezclan asumiendo contexto compatible cuando no lo es. Inyectar transcripts completos viejos infla el contexto y reintroduce ruido ya resuelto. El costo es trabajo basado en una realidad que ya no existe.

## Supuestos y límites (anti-scope)

- **Supone** que el runtime persiste las sesiones nombradas entre invocaciones (`--resume`/`--fork` resuelven un id existente). En runtimes efímeros sin store de sesión, solo `fresh + summary` es viable.
- **Supone** que la baseline del fork está congelada: si la baseline sigue mutando mientras las ramas avanzan, los forks no son independientes y vuelve el problema de staleness.
- **No** decide por edad de la sesión sino por validez del contexto. Una sesión de hace semanas sin cambios en el mundo es resumible; una de hace 10 minutos tras un refactor no lo es.
- **No** sustituye verificación: tras `--resume` el modelo debe re-confirmar el estado real antes de actuar sobre archivos que cree conocer (un `read`/`ls` barato contra la suposición).
- **No** es merge de ramas: `fork` abre caminos paralelos pero NO los reconcilia. Consolidar approach-A y approach-B es un paso manual posterior (vía summary curado), no un `--merge`.
- **Límite de summary:** el summary tipado debe ser conclusiones curadas, no transcript. Si crece hasta parecer la conversación entera, reintroduce el ruido que `fresh` debía eliminar.

## Modelo mental

- **Resume = contexto válido.** La conversación sigue lógicamente; nada del mundo cambió bajo los pies del modelo. Misma investigación, mismos archivos.
- **Fork = dos caminos desde la misma baseline.** Cada rama es independiente y nombrada; cero interferencia entre ellas. Sirve para explorar enfoques alternativos en paralelo.
- **Summary fresh = el mundo cambió.** Arranca limpio con un summary tipado en el system prompt, no con el transcript completo. Recarga las fuentes actualizadas.
- **Scratchpad estructurado (Kata 18) es la fuente del summary.** No se pega la conversación entera: se inyecta el resumen curado de hallazgos.
- **Señal de stale:** si hubo refactor, migración o edición masiva entre sesiones, los tool results previos están stale y resume es la elección incorrecta.

## Matriz de decisión

Recorre las preguntas en orden; el primer "sí" fija el patrón.

| # | Pregunta | Sí | Decisión |
|---|---|---|---|
| 1 | ¿Cambió el mundo desde la última sesión (refactor, deploy, migración, edición masiva)? | → | **fresh** + summary tipado (recarga fuentes actualizadas) |
| 2 | ¿Quieres explorar 2+ enfoques alternativos desde un mismo punto de partida? | → | **fork** a sesiones nombradas (1 por enfoque) |
| 3 | ¿El contexto sigue válido y la conversación avanza lógicamente? | → | **resume** |
| 4 | Ninguna de las anteriores / en duda | → | **fresh** (default seguro: nunca arrastra contexto stale) |

Trade-off central: `resume` maximiza continuidad pero arriesga staleness; `fresh` sacrifica continuidad por correctitud garantizada. Ante duda, **fresh gana**: re-cargar fuentes cuesta tokens, pero actuar sobre estado obsoleto cuesta retrabajo y alucinación.

## Casos borde

- **Cambio parcial:** solo cambió un módulo de muchos. `resume` con re-verificación explícita del módulo tocado, o `fresh` con summary que marque qué fuentes recargar. No asumas que "parcial" implica "seguro".
- **Fork de un fork:** legítimo para sub-ramificar, pero nombra de forma trazable (`approach-A`, `approach-A-variant`) y recuerda que cada nivel hereda la staleness de su baseline.
- **Resume tras `/compact`:** la sesión existe pero perdió detalle. Combina con el scratchpad (Kata 18): `resume` para el hilo, scratchpad para el detalle durable que la compactación borró.
- **Summary que excede su utilidad:** si el scratchpad creció demasiado, cúralo antes de inyectarlo; no pegues un scratchpad de 40k tokens "porque es resumen".

## Failure modes

- **Resume optimista:** asumir validez sin verificar → alucinación sobre estado obsoleto. Mitigación: un `read`/`ls` barato contra la suposición antes de editar.
- **Forks que se mezclan:** asumir contexto compatible entre ramas que divergieron → conclusiones cruzadas inválidas. Mitigación: aislamiento por sesión nombrada, cero referencias cruzadas.
- **Summary inflado:** pegar transcript crudo como "summary" → contexto inflado y ruido reintroducido. Mitigación: solo conclusiones curadas del scratchpad.
- **Fresh innecesario:** descartar contexto válido y recargar todo → quema tokens y latencia sin razón. Mitigación: aplica la matriz; no todo cambio justifica fresh.

## Criterios de aceptación

- La decisión `resume|fork|fresh` cita la señal concreta que la justifica (pregunta de la matriz), no inercia.
- Si elige `resume`, hay un paso de re-verificación del estado antes de actuar sobre archivos.
- Si elige `fork`, cada rama tiene nombre propio y cero referencias cruzadas.
- Si elige `fresh`, el summary inyectado es curado (del scratchpad), no transcript crudo.
- Todo reporte JSON valida contra `assets/` vía `scripts/check.sh` antes de aceptarse.

## Activos determinísticos

Usa `assets/manifest.json` como indice de contratos offline. Los assets fijan la matriz de decision `resume|fork|fresh`, senales de staleness, aislamiento de forks, summary tipado y contrato JSON de salida. Si produces un reporte JSON de la kata, validalo con `bash skills/katas-session-resume-fork/scripts/check.sh` antes de marcarlo como aceptado.

## Patrón correcto

```bash
# Misma investigación, contexto válido → resume
claude --resume codebase-audit-2025-04

# Dos enfoques en paralelo desde una baseline → fork a sesiones nombradas
claude --fork codebase-audit-2025-04 --new-name approach-A
claude --fork codebase-audit-2025-04 --new-name approach-B

# El mundo cambió → sesión fresh con summary tipado del scratchpad
SUMMARY=$(cat investigation-scratchpad.md)
claude -p "Continuamos. Hallazgos previos:\n$SUMMARY"
```

## Anti-patrón

```bash
# ANTI: resume después de un refactor masivo
# el modelo recuerda los archivos como eran y alucina sobre estado obsoleto
claude --resume codebase-audit-2025-04   # tras reescribir media base de código

# ANTI: inyectar el transcript completo viejo
# infla contexto y reintroduce ruido ya resuelto
SUMMARY=$(cat full-old-transcript.log)   # 40k tokens de conversación cruda
claude -p "Continuamos. Conversación previa:\n$SUMMARY"
```

## Argumento de certificación

- Decide entre resume, fork y fresh con criterio explícito, no por inercia.
- Identifica cuándo los tool results previos están stale (refactor, migración, edición masiva).
- Conecta el patrón con el scratchpad estructurado (Kata 18) como fuente del summary tipado.
- Rechaza pegar transcripts completos viejos; defiende el summary curado en su lugar.
- Valida reportes JSON con `scripts/check.sh` contra los contratos en `assets/`.

## Cuándo activar

Activa cuando el usuario pregunte por continuar una sesión previa, ramificar enfoques alternativos, o cuando haya señales de que el estado del proyecto cambió desde la última corrida (refactor, deploy, migración) y haya que decidir cómo reanudar el trabajo sin arrastrar contexto stale.

## Skills relacionadas

- `katas-structured-scratchpad`
- `katas-human-handoff`
- `katas-context-attention-budget`
