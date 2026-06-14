<!-- distilled from alfa skills/katas-path-conditional-rules -->
<!-- Reglas condicionales por glob de ruta; universales siempre cargadas, heuristicas de lenguaje on-demand. -->
# Katas Path Conditional Rules

## Qué es

Reglas heurísticas (estilo, lints, convenciones de lenguaje) que se cargan solo cuando el agente edita archivos que matchean un glob de ruta; las reglas universales (políticas de seguridad) permanecen siempre cargadas. La regla declara su glob de activación (`src/**/*.py`, `*.tf`): el agente la carga al entrar al archivo y la descarta al salir. [DOC]

## Por qué importa (falla que evita)

Un `CLAUDE.md` que carga 2000 líneas para todos los archivos paga ese costo en todas las sesiones, incluso cuando el agente solo edita un README. [INFERENCIA] Cargar reglas Python únicamente al tocar `*.py` libera contexto para el resto de la sesión. Sin esta clasificación, cada edición trivial arrastra heurísticas de lenguajes que no se usan, inflando el contexto y degradando la atención del modelo. [INFERENCIA]

## Modelo mental

- La regla declara su glob de activación: `src/**/*.py`, `*.tf`. [DOC]
- El agente carga la regla al entrar a un archivo que matchea y la descarta al salir. [DOC]
- Reglas grandes (heurísticas de lenguaje) → condicionales por glob. [INFERENCIA]
- Reglas universales (políticas de seguridad) → siempre cargadas, sin glob. [DOC]
- En conflictos puntuales por subpath, la regla más específica gana (precedencia por profundidad de ruta); ambas pueden coexistir cargadas. [SUPUESTO]
- El ahorro es medible: comparar `input_tokens` editando un README contra editar un `.py`. [INFERENCIA]

## Patrón correcto

```text
# <repo>/CLAUDE.md
@rules/security.md   # universal, siempre cargada

## When editing src/**/*.py:
@rules/python-style.md
@rules/python-testing.md

## When editing src/**/*.tf:
@rules/terraform.md
```

Resultado: `python-style.md` NO se carga al editar un README; `security.md` SÍ se carga siempre, en toda edición. [DOC]

## Anti-patrón

```text
# <repo>/CLAUDE.md  — monolítico
@rules/python-style.md
@rules/python-testing.md
@rules/terraform.md
@rules/go-conventions.md
@rules/testing.md
@rules/security.md
# Todas cargan siempre, aunque solo edites un README.
```

Un único `CLAUDE.md` con todas las reglas (Python + Terraform + Go + Testing + Security) cargando en cada sesión paga el costo completo de tokens incluso para ediciones triviales. [INFERENCIA]

## Decisión: universal vs condicional (trade-off)

| Eje | Universal (sin glob) | Condicional por glob |
|-----|----------------------|----------------------|
| Carga | siempre, todo archivo | solo al matchear el glob |
| Buen ajuste | seguridad, secretos, licencia, idioma de salida | estilo/lints/testing de UN lenguaje |
| Costo | tokens en cada sesión | regla ausente si el glob no matchea |
| Riesgo | infla contexto trivial | falso negativo de glob → regla no aplica |

Regla de decisión: si la convención debe regir SIEMPRE (correctness/seguridad), es universal aunque sea grande; el costo es el precio de no fallar. Si solo aplica a un tipo de archivo, condiciónala. [INFERENCIA] Ante la duda, condicional: una regla ausente por glob estrecho es menos dañina que una universal que diluye toda sesión. [SUPUESTO]

## Límites y anti-scope

- Asume un runtime que resuelve globs y carga/descarta reglas por archivo en edición; donde el runtime solo lee un `CLAUDE.md` plano, la condicionalidad es inerte — verificar soporte antes de diseñar. [SUPUESTO]
- NO es retrieval semántico: el match es por patrón de ruta, no por contenido o intención. Un archivo fuera del glob NO activa la regla aunque sea conceptualmente del mismo lenguaje (script `.py` sin extensión, notebook, archivo generado). [INFERENCIA]
- NO sustituye guardrails determinísticos (hooks, validación de salida): una regla cargada es guía atendida probabilísticamente, no un control que bloquea. La seguridad crítica va también en hook. [INFERENCIA]
- Resuelve "qué regla según el archivo en edición"; NO "qué memoria según el dueño" (usuario/equipo/módulo) — eso es `katas-hierarchical-claude-memory`. Las dos katas se componen. [INFERENCIA]
- Glob demasiado amplio (`**/*`) anula el beneficio: equivale a universal con pasos extra. [INFERENCIA]

## Modos de falla

- **Glob estrecho de más:** `src/**/*.py` no matchea `scripts/*.py` ni `tests/*.py`; la regla calla justo donde más importa. Anclar globs a la estructura real del repo. [INFERENCIA]
- **Glob amplio de más:** `**/*.md` carga estilo de prosa al editar un changelog autogenerado; ruido sin valor. [INFERENCIA]
- **Universal mal clasificada como condicional:** seguridad puesta tras un glob `*.py` → editar `*.tf` omite la política. Seguridad SIEMPRE sin glob. [DOC]
- **Solapamiento ambiguo:** dos globs matchean el mismo archivo con reglas contradictorias y sin orden claro; el agente aplica una no determinista. Hacer explícita la precedencia (subpath más profundo gana). [SUPUESTO]
- **Regla huérfana:** `@rules/go.md` movido/borrado; el bloque condicional degrada en silencio a "sin regla". Verificar que cada import resuelve. [INFERENCIA]

## Casos límite

- **Archivo políglota** (`.vue`, `.ipynb`, `.md` con bloques de código): puede matchear varios globs; cargar las reglas relevantes y aceptar coexistencia. [SUPUESTO]
- **Edición multi-archivo en un turno** (README + `.py`): la unión de globs activos es la suma de sus reglas; el contexto crece con la diversidad de tipos tocados. [INFERENCIA]
- **Misma regla en dos globs:** preferir un glob más general que cubra ambos antes que duplicar el bloque. [INFERENCIA]
- **Repo de un solo lenguaje:** la ganancia es marginal; mantener universal puede ser más simple que condicionar todo. [SUPUESTO]

## Verificación

- Editar un README NO carga `python-style.md` (ausente en el contexto resuelto). [INFERENCIA]
- Editar un `.py` carga estilo + testing de Python Y la regla universal de seguridad. [INFERENCIA]
- Editar un `.tf` carga `terraform.md` pero NO reglas de Python. [INFERENCIA]
- `input_tokens` al editar un README < `input_tokens` al editar un `.py`; el delta cuantifica el ahorro. [INFERENCIA]
- Cada `@rules/*` referenciado en un bloque condicional resuelve a un archivo versionado existente. [INFERENCIA]

## Argumento de certificación

Clasificar explícitamente cada regla como universal (siempre cargada, sin glob) o condicional por glob de ruta, y estimar el ahorro de tokens de forma medible: [DOC]

- P1: una regla universal (seguridad) se carga directamente en el `CLAUDE.md` raíz, sin glob. [DOC]
- P2: cuando dos reglas aplican, ambas se cargan y la más específica gana en conflictos puntuales (precedencia por subpath). [SUPUESTO]
- P3: el ahorro se mide comparando `input_tokens` al editar un README frente a editar un `.py`. [INFERENCIA]

## Cuándo activar

- Diseñar o auditar la estructura de reglas/memoria de un repo (`CLAUDE.md`, `@rules/*`).
- Decidir si una convención debe ser universal o condicional por glob.
- Reducir el costo de contexto de sesiones que editan archivos de un solo tipo.
- Justificar con números el ahorro de tokens de un esquema condicional por ruta.

## Skills relacionadas

- `katas-custom-commands-skills`
- `katas-session-resume-fork`
- `katas-fewshot-edge-calibration`
- `katas-hierarchical-claude-memory`
