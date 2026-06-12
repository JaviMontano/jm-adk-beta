<!-- distilled from alfa skills/katas-builtin-tool-selection -->
<!-- Seleccion de built-in tools con estrategia Grep then Read then Edit, failure modes y sin Read masivo upfront. -->
# Katas Builtin Tool Selection

## Qué es

Claude Code expone built-in tools, cada una con un uso primario y un failure mode. Elegir la tool correcta es mecánica de examen y separa agentes eficientes de los que queman contexto cada turno. [DOC]

| Tool | Uso primario | Failure mode | Señal de selección |
|---|---|---|---|
| `Grep` | Buscar **contenido** por regex en el cuerpo de archivos | Regex mal escapado → 0 o demasiados hits | Conoces un símbolo/string, no el path |
| `Glob` | Buscar **paths** por patrón de nombre (no mira contenido) | Patrón muy amplio → ruido | Conoces el nombre/extensión, no el contenido |
| `Read` | Cargar **un** archivo concreto en contexto | Archivo enorme → tokens desperdiciados | Ya identificaste el path exacto |
| `Edit` | Modificación dirigida sobre un **anchor único** | Anchor no único o inexistente → falla | Cambio puntual y el anchor es inequívoco |
| `Write` | Sobrescribir un archivo **completo** | Pisa contenido no leído → pérdida de datos | Reescritura total o fallback de `Edit` |
| `Bash` | Ejecutar comandos de shell | Side effects no idempotentes | Acción del sistema, no exploración de código |

La estrategia incremental canónica es `Grep` → `Read` → `Edit`: localizar entry points por contenido, leer selectivamente siguiendo imports, y aplicar una modificación puntual. [DOC]

## Por qué importa (falla que evita)

`Read` sobre todo el repositorio carga miles de tokens inútiles y quema el presupuesto de contexto. [INFERENCIA] Un `Edit` con anchor no único (matchea varias líneas) o inexistente falla sin aplicar cambios. [DOC] Confundir `Grep` (contenido) con `Glob` (paths) hace que la búsqueda devuelva el conjunto equivocado y el agente lea archivos irrelevantes. [INFERENCIA]

## Modelo mental

- `Grep` = contenido · `Glob` = paths · `Read` = cargar archivo · `Edit` = mod puntual · `Write` = reescribir · `Bash` = shell. [DOC]
- Pipeline: `Grep` (entry points) → `Read` selectivo (seguir imports) → `Edit`/`Write` puntual. [DOC]
- Regla de decisión: ¿sé el **contenido** pero no el path? → `Grep`. ¿Sé el **nombre** pero no el contenido? → `Glob`. ¿Ya tengo el **path**? → `Read`. ¿Anchor inequívoco? → `Edit`; si no, `Read`+`Write`. [INFERENCIA]
- Failure de `Edit`: anchor no único/inexistente → falla. Fallback: `Read` entero + `Write` completo, con razón explícita. [DOC]
- Nunca "leer todo el repo upfront": anti-patrón que destruye el presupuesto de tokens. [DOC]

## Patrón correcto

```python
matches = grep(pattern="processRefund\\(", glob="**/*.py")
content = read(matches[0].path)
edit(
    path=matches[0].path,
    old_text="if amount > 1000:",
    new_text="if amount > MAX_REFUND:",
)
```

`Grep` acota a un único candidato; `Read` carga solo ese archivo; el anchor `if amount > 1000:` es único en el archivo, así que `Edit` aplica de forma determinística. [INFERENCIA]

## Anti-patrón

```python
all_files = glob("**/*")
for f in all_files:
    read(f)  # 200k tokens cargados sin necesidad

edit(old_text="if amount", ...)  # múltiples líneas matchean → falla
```

Dos errores: cargar el repo entero (presupuesto), y un anchor (`if amount`) que matchea varias líneas (no único → `Edit` falla). [INFERENCIA]

## Casos límite

- **Anchor no único** → no fuerces `Edit`. Amplía el anchor con contexto circundante hasta que sea único, o usa `replace_all` solo si **todas** las ocurrencias deben cambiar igual. [SUPUESTO]
- **Grep con 0 hits** → puede ser regex sobre-escapado o el símbolo no existe. Verifica el escape antes de concluir ausencia. [INFERENCIA]
- **Archivo no leído antes de `Write`** → `Write` ciego pisa contenido; el fallback exige `Read` completo previo + razón. [DOC]
- **`Glob` para encontrar texto** → error de tool-fit: `Glob` ignora el cuerpo del archivo; usa `Grep`. [DOC]
- **`Bash` para leer/editar código** (`cat`/`sed`) → preferir `Read`/`Edit`; `Bash` se reserva para acciones de sistema. [SUPUESTO]

## Anti-scope

- No cubre selección de **MCP tools** ni custom commands/skills (ver skills relacionadas). [DOC]
- No define cómo escribir regex de `Grep`; asume sintaxis válida. [SUPUESTO]
- No reemplaza la planificación de exploración (plan-mode); decide la tool, no el plan. [INFERENCIA]

## Argumento de certificación

- Escoger el tool correcto en una decisión rápida según uso primario. [DOC]
- Describir el failure mode de `Edit` (anchor no único/inexistente) y su fallback `Read` + `Write`. [DOC]
- Defender la estrategia `Grep` → `Read` → `Edit`. [DOC]
- Rechazar el `Read` masivo upfront sobre el repositorio. [DOC]

## Criterios de aceptación

- Cada paso de exploración elige la tool por su uso primario, no por hábito. [DOC]
- Ningún `Read` masivo upfront; toda lectura va precedida de `Grep`/`Glob` cuando el target es desconocido. [DOC]
- Todo `Edit` declara un anchor único (matchea exactamente una línea); si no, degrada a `Read`+`Write` con razón explícita. [INFERENCIA]

## Cuándo activar

- El agente debe explorar/modificar un codebase y elegir entre `Grep`, `Glob`, `Read`, `Edit`, `Write` o `Bash`. [DOC]
- Un `Edit` falla por anchor ambiguo y hay que decidir el fallback. [DOC]
- Un plan de exploración propone cargar el repositorio entero y hay que corregirlo. [DOC]

## Skills relacionadas

- `katas-plan-mode-exploration`
- `katas-custom-commands-skills`
- `katas-hierarchical-claude-memory`
