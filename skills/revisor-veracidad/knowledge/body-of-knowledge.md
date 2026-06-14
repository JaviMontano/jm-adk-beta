# Body of Knowledge — revisor-veracidad

Cuerpo de conocimiento de dominio para auditar veracidad y marcar procedencia. La fuente canonica de la taxonomia es `references/verification-tags.md`; aqui se consolidan conceptos, estandares y reglas de decision que el skill aplica. [DOC]

## 1. Conceptos clave

- **Afirmacion (claim).** Enunciado que un lector no podria reproducir solo desde el prompt: hechos externos, numeros derivados, defaults elegidos, cualquier cosa que requiera validacion.
- **Procedencia.** El origen de un claim, codificado en un tag inline. La auditoria no juzga si el claim es verdadero, sino si su respaldo es reproducible **hoy**.
- **Familia de tags.** Dos conjuntos homologados: **Jarvis OS** (operador) y **Alfa core** (kit/repo). Se elige por audiencia, no por contenido. Nunca se mezclan en un documento. [DOC]
- **Plan de cierre.** Para cada claim no verificable hoy (`{SUPUESTO}`/`{POR_CONFIRMAR}`), el paso concreto que lo verificaria.
- **Bloqueo critico.** `{VACIO_CRITICO}`: falta dato esencial; la ejecucion se detiene y se pregunta. Es terminal: no se auto-rellena. [DOC]

## 2. Las dos familias (estandar)

### Jarvis OS (operador)
`{MEMORIA}` (MEMORY.md/contexto persistente), `{ADJUNTO}` (archivo adjunto/pegado), `{EXTRAIDO_HILO}` (conversacion actual), `{WEB}` (busqueda web con cita), `{CONOCIMIENTO}` (general pre-cutoff), `{SUPUESTO}` (asuncion explicita), `{INFERENCIA}` (razonamiento derivado), `{AUTOCOMPLETADO}` (default sin preguntar), `{POR_CONFIRMAR}` (necesita validacion humana), `{VACIO_CRITICO}` (falta dato; stop).

### Alfa core (kit)
`[CÓDIGO]`/`[CODE]` (codigo/config en repo), `[CONFIG]` (referencia de configuracion), `[DOC]` (documentacion/spec), `[INFERENCIA]`/`[INFERENCE]` (deduccion logica), `[SUPUESTO]`/`[ASSUMPTION]` (claim sin evidencia directa).

## 3. Mapping (homologacion)

Lossy por diseno; siempre Jarvis -> Alfa, nunca al reves (no se recupera la distincion fina). [INFERENCIA]

| Jarvis OS | Alfa core |
|---|---|
| `{CONOCIMIENTO}` / `{WEB}` | `[DOC]` |
| `{MEMORIA}` / `{ADJUNTO}` / `{EXTRAIDO_HILO}` | `[CONFIG]` / `[CÓDIGO]` |
| `{INFERENCIA}` | `[INFERENCIA]` |
| `{SUPUESTO}` / `{AUTOCOMPLETADO}` / `{POR_CONFIRMAR}` | `[SUPUESTO]` |
| `{VACIO_CRITICO}` | (stop + ask) |

Fila split: artefacto de archivo/repo -> `[CÓDIGO]`; valor de settings/config -> `[CONFIG]`. [SUPUESTO]

## 4. Reglas de decision

1. **Tag mas debil.** Si dos tags caben, elegir el menos cierto. El fallo que importa es subir el tag (`{SUPUESTO}` -> `{MEMORIA}`).
2. **`{WEB}` requiere cita.** Sin cita es invalido: degradar a `{CONOCIMIENTO}` o eliminar el claim.
3. **Cita inverificable.** Link muerto/fuente privada -> `{POR_CONFIRMAR}`, no `{WEB}`.
4. **No sobre-tagear.** Lo auto-evidente, el input re-citado y la estructura del output van sin tag.
5. **Una familia.** Elegir por audiencia y mantenerla en todo el documento; ortografia ES/EN consistente.
6. **`{SUPUESTO}`/`{POR_CONFIRMAR}` -> paso de cierre.** Sin el paso, es ruido, no verificacion.
7. **No inventar respaldo.** Si la evidencia no existe, se marca el riesgo; nunca se fabrica la fuente.

## 5. Criterios de aceptacion (gate)

- Cada afirmacion no obvia: exactamente un tag, una sola familia. [DOC]
- Ningun `{WEB}` sin cita; ningun `{VACIO_CRITICO}` seguido de dato fabricado.
- Cada `{SUPUESTO}`/`{POR_CONFIRMAR}` emparejado con paso concreto.
- Ortografia de tags consistente.

## 6. Limites

No reemplaza revision experta legal/medica/financiera/seguridad: ahi solo se marca el riesgo, no se decide. No genera ni reescribe contenido. No valida codigo en ejecucion (eso son los chequeos deterministas de `scripts/`). [DOC]
