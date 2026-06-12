<!-- distilled from alfa skills/katas-persistent-scratchpad -->
<!-- Scratchpad persistente en disco curado por el agente; sobrevive a compact y reinicios, leido una vez y referenciado despues. -->
# Katas Persistent Scratchpad

## Qué es

Un archivo externo a la conversación (`investigation-scratchpad.md`) donde el agente vuelca descubrimientos durables: hipótesis confirmadas, decisiones, hallazgos de archivos y pendientes. Sobrevive a `/compact` y a reinicios de sesión. Es memoria persistente en disco, curada por el propio agente, no un volcado del historial conversacional.

## Por qué importa (falla que evita)

Cuando el contexto se compacta (Kata 11 · compactación), se pierde detalle. Si un descubrimiento crítico vivía solo en el historial conversacional, desaparece sin dejar rastro. El scratchpad es la red de seguridad: memoria persistente curada por el agente que sobrevive a cualquier compactación o reset de sesión, de modo que las conclusiones validadas nunca dependen de la ventana de contexto.

## Supuestos y límites (anti-scope)

- **Supone** un filesystem persistente entre turnos/sesiones (la ruta sobrevive a `/compact` y reinicio). No aplica a runtimes efímeros sin disco escribible.
- **Supone** que el agente cura: filtra señal validada de ruido. Si no hay disciplina de curado, el scratchpad degenera en un segundo historial conversacional sucio.
- **No** es un log de auditoría ni un transcript: no captura cada turno, solo conclusiones durables. Para trazabilidad turn-by-turn usa otro mecanismo.
- **No** sustituye verificación: lo que se escribe ya debe estar validado (test que pasó, bug replicado, decisión cerrada), no una hipótesis viva.
- **No** es memoria compartida multi-agente por defecto: un único archivo append-only sin locking corrompe escrituras concurrentes (ver Failure modes).
- **Límite de tamaño:** si crece sin poda, releerlo entero al inicio infla el prefijo. Compactarlo periódicamente (fusionar pendientes resueltos) es parte del curado, no opcional.

## Modelo mental

- Conversación = memoria volátil: puede compactarse o resetearse en cualquier momento.
- Scratchpad = memoria persistente en disco: la fuente de verdad de lo que el agente ya validó.
- El agente escribe SOLO conclusiones validadas: hipótesis confirmadas, decisiones, hallazgos, pendientes. No vuelca monólogo interno, hipótesis sin confirmar ni dudas pasajeras.
- Estructura fija por secciones (`## Decisiones`, `## Hallazgos`, `## Pendientes`) para que sea anexable y legible.
- Al inicio de cada sesión el agente lee el scratchpad UNA vez; después referencia y anexa, no re-lee cada turno (preserva el prefijo de cache, Kata 10).

Gate **escribir vs descartar** (el más confundido):

| Candidato | ¿Validado y durable? | Acción |
|---|---|---|
| `pydantic v2` compatible (test T-19 pasó) | sí, decisión cerrada | append a `## Decisiones` |
| "creo que el bug está en el parser" | hipótesis sin confirmar | NO escribir; vive en conversación |
| bug replicado en `parser.py:142` | sí, hallazgo reproducible | append a `## Hallazgos` |
| "tal vez después revise los flags" | duda pasajera | NO escribir; si es acción real, va a `## Pendientes` como tarea concreta |

## Activos determinísticos

Usa `assets/manifest.json` como indice de contratos offline. Los assets fijan ruta, secciones, evidencia, lectura unica, escritura append-only y contrato JSON de salida. Si produces un reporte JSON de scratchpad persistente, validalo con `bash skills/katas-persistent-scratchpad/scripts/check.sh` antes de marcarlo como aceptado.

## Patrón correcto

```markdown
# Investigation Scratchpad
## Decisiones
- 2026-04-25: usar pydantic v2 (T-19 confirmó compat).
## Hallazgos
- src/legacy/parser.py bug offset línea 142 (replicado).
## Pendientes
- Verificar si --strict rompe tests integration
```

```python
def append_scratchpad(section, entry):
    """Anexa una conclusión validada a la sección indicada del scratchpad."""
    path = "investigation-scratchpad.md"
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(f"\n## {section}\n- {entry}\n")
```

## Anti-patrón

- Confiar en la conversación como memoria de largo plazo: tras `/compact` el hallazgo desaparece.
- Scratchpad sin estructura, o re-leído cada turno: rompe el cache de prefijo (Kata 10) y ensucia la señal.
- Volcar monólogo interno, hipótesis no confirmadas o dudas pasajeras al scratchpad: contamina la memoria persistente con ruido no validado.
- Sobrescribir (`open(path, "w")`) en vez de anexar: borra el historial durable que es justo el activo a proteger.

## Decisión de diseño: append-only vs reescritura curada

Append-only (`mode="a"`) es la elección por defecto porque es atómica a nivel de entrada y nunca pierde una conclusión ya escrita. **Trade-off:** acumula entradas obsoletas (pendientes ya resueltos) que inflan el archivo. Se acepta y se mitiga con poda periódica explícita (reescritura curada en un paso de mantenimiento consciente), NO con sobrescritura automática por turno —que reintroduce el riesgo de borrado accidental. Regla: escritura del turno = append; compactación del scratchpad = operación deliberada, separada y validada.

## Failure modes

- **Escritura concurrente:** dos agentes anexando al mismo archivo sin lock entrelazan líneas y corrompen secciones. Mitigación: un escritor por scratchpad, o un archivo por agente con merge explícito.
- **Drift de ruta:** el agente asume `investigation-scratchpad.md` relativo al cwd y el cwd cambia entre llamadas (los hilos de agente lo resetean). Mitigación: ruta absoluta fijada al inicio de sesión.
- **Cache invalidado al releer:** releer el scratchpad mutado a mitad de sesión lo coloca antes del borde dinámico e invalida el prefijo (Kata 10). Mitigación: leer una vez al inicio; después solo anexar.
- **Memoria envenenada:** una hipótesis falsa escrita como hallazgo se trata como verdad en sesiones futuras. Mitigación: el gate "validado y durable" es duro; ante duda, no se escribe.

## Argumento de certificación

- Describir la diferencia entre memoria conversacional (volátil) y persistente (scratchpad en disco).
- Enunciar qué se escribe (hipótesis confirmadas, decisiones, hallazgos, pendientes) y qué NO (monólogo, hipótesis sin confirmar, dudas pasajeras).
- Conectar con Kata 11 (compactación, que motiva la persistencia) y Kata 19 (investigación adaptativa, que consume y alimenta el scratchpad).
- Validar el contrato offline con `scripts/check.sh` cuando el output sea JSON.

## Cuándo activar

- Una investigación larga o multisesión donde el detalle no puede perderse al compactar.
- El usuario pide persistir hallazgos, retomar una investigación, o mantener memoria durable entre reinicios.
- Triggers: `persistent scratchpad`, `investigation scratchpad`, `durable memory`, `scratchpad file`.

## Skills relacionadas

- `katas-compaction-boundary`
- `katas-adaptive-investigation`
- `katas-cache-aware-context`
