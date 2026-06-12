---
name: tool-use-design
version: 1.2.0
description: "Design deterministic tool-description routing contracts with explicit input formats, examples, reciprocal boundaries, overload split decisions, Grep then Read then Edit repository strategy, Edit failure fallback, and offline validation."
owner: "JM Labs"
last_updated: 2026-06-11
triggers:
  - tool use design
  - tool description contract
  - builtin tool strategy
  - tool routing
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Tool Use Design

## Purpose

Design each tool description as a **deterministic routing contract** a planner can act on with zero hidden context. The contract fixes: purpose, input format, output shape, 1–2 examples, reciprocal boundary, overload split decision, `Grep → Read → Edit` repo strategy, and `Edit` fallback when the anchor is not unique. [DOC]

The unit of value is *decisión inmediata*: given the description alone, the model picks the right tool without guessing or asking. [INFERENCIA]

## Cuándo usarla (trigger)

Activa cuando se cumpla **al menos una**: [DOC]

- Defines/refactors un tool surface y dos tools se solapan en propósito (overloading).
- El agente elige el tool equivocado o pide aclaración cuando la decisión debería ser inmediata.
- Una descripción genérica (`"Analyzes content"`) no dice qué entrada espera ni dónde está su frontera.
- Vas a operar sobre un repo desconocido y falta un protocolo de lectura que evite el `read-all` masivo.
- `Edit` falla de forma intermitente (anchor no único) y no hay fallback documentado.

**Anti-scope — NO actives** para: redactar correos/prosa, ejecutar un único comando de shell, o tareas sin decisión de routing entre ≥2 tools. Esos casos son falsos positivos (ver `evals.json`: `false_positive_client_email`, `false_positive_single_shell_command`). [CONFIG]

## Inputs / Outputs

- **Input**: un tool surface (≥2 tools) — nombres + descripciones actuales — o el requisito de diseñarlo desde cero. [DOC]
- **Output**: un report JSON validable que cumple el contrato (ver Validation gate), más las descripciones reescritas como contratos. [DOC]

## Workflow

1. **Inventaria el tool surface** y detecta solapamientos: dos tools que un humano confundiría son dos tools que el modelo confundirá. [INFERENCIA]
2. **Escribe cada descripción como contrato**: propósito en una frase, **input format** explícito, **output shape**, 1–2 ejemplos de invocación, y la **frontera recíproca** ("usa X para A; para B usa Y", y Y referencia de vuelta a X). [DOC]
3. **Resuelve el overloading con rename + split**, no con prosa: un tool sobrecargado se divide en dos con nombres y fronteras recíprocas. Justificación: el modelo enruta por nombre+frontera, no por matices en un párrafo que puede ignorar bajo presión de contexto. [INFERENCIA]
4. **Documenta el failure mode de `Edit`**: `old_string` debe ser único; si no, `Edit` falla. Declara el **fallback Read+Write** (reescritura total) cuando el anchor no se puede aislar. [CÓDIGO]
5. **Codifica la estrategia built-in** `Grep → Read → Edit`: localizar con Grep/Glob, leer solo lo relevante con Read, mutar con Edit. **Nunca** `Glob("**/*") + Read all` upfront. [DOC]
6. **Valida con el gate** antes de cerrar (sección Validation gate).

## Decisiones y trade-offs

- **Split vs. prosa aclaratoria**: split gana. Coste: más superficie de tools; beneficio: routing determinista. El coste es lineal y barato; la ambigüedad de prosa es un fallo silencioso recurrente. [INFERENCIA]
- **`Grep → Read` selectivo vs. `read-all` upfront**: selectivo gana. `read-all` parece "más seguro" (todo el contexto) pero satura la ventana (~200k tokens en repos medianos) y degrada el reasoning. Carga solo lo que un hit de Grep justifique. [SUPUESTO] — confirmar midiendo tokens en el repo objetivo antes de adoptar read-all.
- **Edit con anchor único vs. Write full-rewrite**: prefiere Edit (mínimo blast radius). Cae a Write solo cuando el anchor no se puede aislar; nunca al revés por comodidad. [CÓDIGO]

## Output Rules (anti-patterns duros)

Nunca: [DOC]

- Aceptar descripciones genéricas (`"analyzes content"`, `"processes files"`).
- Permitir `Glob("**/*")` + read-all como estrategia de discovery upfront.
- Tratar un anchor de `Edit` ambiguo como seguro sin fallback.
- Resolver tools sobrecargados solo con prosa (split + rename, siempre).
- Mezclar familias de evidence tags en un mismo output (ver `references/verification-tags.md`). [CONFIG]

Referencia las policies del kit cuando existan: `assets/description-contract-policy.json`, `assets/boundary-policy.json`, `assets/repo-strategy-policy.json`, `assets/edit-safety-policy.json`, `assets/anti-pattern-policy.json`, y el contrato `assets/tool-use-contract.json`. [SUPUESTO] — estos assets son prescritos por esta skill; si faltan, créalos antes de validar (ver `evals.json: upgrade_safety_case`).

## Pattern

```python
# GOOD — descripciones como contrato con frontera recíproca + estrategia Grep→Read→Edit
TOOLS = [
    {
        "name": "search_code",
        "description": (
            "Find files or symbols by pattern across the repo. "
            "Input: a regex or literal string. Returns matching paths + line numbers. "
            "Use this FIRST to locate. To read a known file's contents, use read_file instead."
        ),
    },
    {
        "name": "read_file",
        "description": (
            "Read the full contents of ONE known file path. "
            "Input: an absolute path. Use after search_code has located the file. "
            "Do NOT use to discover files — that is search_code's job."
        ),
    },
    {
        "name": "edit_file",
        "description": (
            "Replace an exact, UNIQUE anchor string in a file. "
            "Input: path, old_string (must be unique), new_string. "
            "FAILS if old_string is not unique. Fallback: read_file then write_file for a full rewrite."
        ),
    },
]

# Workflow the descriptions enforce: locate cheaply, read selectively, mutate precisely.
hits = search_code(pattern="def handle_payment")   # Grep
src = read_file(path=hits[0].path)                  # Read only the relevant file
edit_file(path=hits[0].path, old_string=unique_anchor, new_string=patched)  # Edit
```

## Anti-Pattern

```python
# ANTI — descripciones genéricas + read masivo upfront
TOOLS = [
    {"name": "analyze", "description": "Analyzes content."},        # no input, no frontera
    {"name": "process", "description": "Processes the file."},      # solapa con analyze
]

# El agente, sin frontera, no sabe cuál elegir → pide aclaración o adivina.
# Y para "entender el repo" carga todo en contexto:
all_files = glob("**/*")
context = "".join(read_file(p) for p in all_files)  # ~200k tokens, satura la ventana
# Edit sin fallback documentado: si el anchor no es único, falla en silencio.
```

## Edge cases y self-correction

- **Anchor no único detectado tarde**: si Edit ya falló, no reintentes con el mismo `old_string`; expande el anchor con contexto adyacente o cae a Write full-rewrite. [CÓDIGO]
- **Tres+ tools se solapan**: split por pares no escala a prosa; redefine el eje de responsabilidad (p. ej. discover / read / mutate) y reasigna. [INFERENCIA]
- **Frontera unidireccional**: si X menciona a Y pero Y no menciona a X, la frontera NO es recíproca → falla el gate. Corrige ambas descripciones. [DOC]
- **Repo gigante donde Grep devuelve cientos de hits**: estrecha el patrón antes de leer; nunca leas todos los hits "por si acaso". [SUPUESTO] — el límite seguro depende del repo; mídelo.
- **Disparador en idioma del usuario distinto al de la skill**: el routing es semántico, no léxico; activa igual.

## Validation gate (acceptance criteria)

Un report válido cumple **todo** lo siguiente (verificable offline, sin red): [DOC]

- ≥2 tool contracts; cada uno con purpose, input format, examples y boundary.
- Delegación **recíproca** entre tools que compiten (bidireccional).
- Overload resuelto como `rename_split` cuando un tool tiene >1 responsabilidad.
- Secuencia de repo strategy = `grep`, `read`, `edit`.
- `read_all_upfront=false` y `glob_all_then_read_all=false`.
- Edit safety: `unique_anchor_required=true` y fallback `read_write_full_rewrite`.
- Flags: `offline=true`, `network_required=false`, `deterministic=true`.

Ejecuta (cuando los scripts existan en el kit): [SUPUESTO]

```bash
python3 skills/tool-use-design/scripts/validate_tool_use_design.py --input <report.json>
bash skills/tool-use-design/scripts/check.sh
```

El validador es offline y rechaza: descripciones genéricas, ejemplos faltantes, fronteras no recíprocas, overload sin resolver, read-all upfront, fallback de Edit ausente, y flags de validación no deterministas. [DOC]

## Checklist rápido (pre-cierre)

- ¿Cada descripción declara input format + output shape + 1–2 ejemplos + frontera recíproca? [DOC]
- ¿El overloading se resolvió con rename + split, no con un párrafo? [DOC]
- ¿El modelo elige el tool correcto por decisión rápida, sin pedir aclaración? [INFERENCIA]
- ¿Está documentado el failure mode de `Edit` (anchor no único) y su fallback Read+Write? [CÓDIGO]
- ¿La estrategia es `Grep → Read → Edit`, sin `Glob("**/*") + Read all` upfront? [DOC]
- ¿Todos los evidence tags son de una sola familia (Alfa core)? [CONFIG]

## Katas y skills relacionadas

- Katas: `katas-21`, `katas-23`.
- Skills: `katas-tool-description-quality`, `katas-builtin-tool-selection`.
