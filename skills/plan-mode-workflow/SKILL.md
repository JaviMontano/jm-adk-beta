---
name: plan-mode-workflow
version: 1.1.0
description: "Disenar un gate de dos modos: explorar un repo desconocido en Plan Mode read-only, firmar un plan.md por hash, y bloquear escritura via hook hasta que la firma habilite Execute Mode."
owner: "JM Labs"
triggers:
  - plan mode workflow
  - read-only exploration
  - plan approval gate
  - two-mode operation
  - signed plan before write
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Plan Mode Workflow

## Capacidad

Operar un repo o dominio desconocido en dos modos explícitos: un **Plan Mode read-only** (solo Read, Grep, Glob, Bash de inspección) que produce un `plan.md`, y un **Execute Mode** que se habilita únicamente tras la firma de ese plan. La transición no depende del modelo: la aplica un **hook** que enumera y bloquea las write-tools mientras el modo sea `plan`. [CONFIG] Lo construible es el **diseño del gate**: estado de modo, contrato del plan, evento de firma y enforcement por hook. No es una convención de prosa; es un dato que un hook puede leer y denegar. [INFERENCIA]

## Cuándo usarla

- Antes de la primera escritura en un repo desconocido cuyo blast radius no está acotado. [DOC]
- Cuando la organización exige aprobación auditable antes de mutar archivos (cambio gobernado, compliance, producción). [DOC]
- Cuando varios humanos o agentes comparten el workspace y un write prematuro pisa trabajo no commiteado. [DOC]
- Cuando el plan puede cambiar a mitad de camino y cada cambio debe re-disparar la firma, no colarse silenciosamente. [DOC]

**No usarla / anti-scope:** tareas sin escritura a repo (resúmenes, tablas, análisis de datos) no necesitan el gate; activar el skill ahí es ruido — degrada a no-activación. [INFERENCIA] Tampoco sustituye permisos de plataforma ni revisión de código: el gate autoriza *ejecutar el plan*, no garantiza que el plan sea correcto. [SUPUESTO]

## Inputs / Outputs

- **Input mínimo:** un repo/dominio objetivo + identidad de quien aprueba. Sin objetivo no hay `plan.md` que firmar → entrada vacía detiene la ejecución (`{VACIO_CRITICO}` → stop + ask), nunca auto-completa el plan. [INFERENCIA]
- **Outputs:** (1) estado de modo (`mode`, `signed_plan_hash`); (2) `plan.md` firmable; (3) evento de firma (`hash` + `approved_by` + `plan_signed_at`); (4) hook `PreToolUse`; (5) write-blocklist explícita; (6) diff final. El plan firmado + el diff son el rastro auditable. [CONFIG]

## Cómo construir

1. **Estado de modo como dato** (`mode: "plan" | "execute"`), no intención en prosa. Arranca en `plan`. [CÓDIGO]
2. **Enumera las write-tools** a bloquear en `plan` (`Write`, `Edit`, `MultiEdit`, `NotebookEdit`, Bash mutante, MCP de mutación). Allowlist de lectura; todo lo demás se bloquea — fail-closed, no fail-open. [INFERENCIA]
3. **Escribe `plan.md`** como artefacto: objetivo, archivos a tocar, orden de cambios, criterio de aceptación y riesgos. Es el objeto que se firma. [DOC]
4. **Modela la aprobación como evento auditable** (`plan_signed_at`, `approved_by`, hash del plan), no un "ok" conversacional. La firma referencia el hash exacto. [CÓDIGO]
5. **Hook `PreToolUse`** que lee el modo: si `mode == "plan"` y la tool está en la write-list, deniega con motivo. Solo `approve_plan(hash)` cambia `mode` a `execute`. [CÓDIGO]
6. **Re-dispara firma ante cambios**: si `plan.md` cambia (hash distinto al firmado), el modo vuelve a `plan` y exige nueva aprobación. [CÓDIGO]
7. **Cierra con evidencia**: plan firmado + diff resultante = rastro de qué se autorizó y qué se ejecutó. [DOC]

## Patrón correcto

```python
# GOOD: el modo es estado; el hook bloquea writes hasta firma del hash exacto.
STATE = {"mode": "plan", "signed_plan_hash": None}
WRITE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
MUTATING_BASH = ("rm ", "sed -i", "mv ", "git commit", "git push", ">", ">>")

def pre_tool_use(tool_name: str, plan_hash_now: str, bash_cmd: str = "") -> dict:
    # plan.md changed after signing -> revert before allowing anything
    if STATE["signed_plan_hash"] and plan_hash_now != STATE["signed_plan_hash"]:
        STATE["mode"] = "plan"
        return {"decision": "deny", "reason": "plan.md changed; re-approval required."}
    if STATE["mode"] == "plan":
        if tool_name in WRITE_TOOLS:
            return {"decision": "deny",
                    "reason": "Plan Mode is read-only. Sign plan.md to enter execute."}
        if tool_name == "Bash" and any(m in bash_cmd for m in MUTATING_BASH):
            return {"decision": "deny",
                    "reason": "Mutating Bash (rm/sed -i/redirects) blocked in Plan Mode."}
    return {"decision": "allow"}

def approve_plan(plan_hash: str, approver: str) -> None:
    STATE["signed_plan_hash"] = plan_hash      # auditable artifact
    STATE["mode"] = "execute"                   # only path into write mode
```

## Anti-patrón

```python
# ANTI: bypassPermissions + escritura desde el primer turno, sin plan ni firma.
settings = {"permissionMode": "bypassPermissions"}   # no read-only gate
def run(repo):
    edit_file(repo / "main.py", patch)   # writes before exploration
    edit_file(repo / "config.yaml", patch)
    # no plan.md, no signed hash, no hook; el modelo decide solo.
```

Otros anti-patrones: aprobar un plan *sin* hash (un "ok" en el chat no es firma); whitelist de writes en vez de blocklist (fail-open); permitir Bash mutante (`rm -rf`, `sed -i`, redirecciones `>`) en `plan` por considerarlo "preparación". [INFERENCIA]

## Edge cases

- **Bash mutante en Plan Mode** (`rm -rf tmp`, `sed -i`): es escritura disfrazada de inspección → el hook debe denegar por patrón de comando, no solo por nombre de tool. [CÓDIGO]
- **Entrada vacía / sin objetivo**: no hay plan que firmar → detener y pedir, no fabricar un plan. [INFERENCIA]
- **`bypassPermissions`**: anula el gate; el validador lo rechaza como caso bloqueado, Guardian no lo aprueba. [CONFIG]
- **Upgrade / completar archivos faltantes**: no sobreescribir ediciones locales ni tocar otras skills — la operación es idempotente y acotada al skill. [SUPUESTO]
- **Firma con hash desactualizado**: si el firmante firma un hash viejo tras un cambio, el chequeo de hash-mismatch revierte a `plan` antes de permitir cualquier write. [CÓDIGO]

## Self-correction triggers

Re-abre el diseño si: ejecutaste un write sin un `signed_plan_hash` que coincida; la aprobación vive en la conversación y no como evento con hash; el hook bloquea por convención y no por enumeración explícita; un cambio de `plan.md` no revirtió a `plan`; o un Bash mutante pasó en modo `plan`. Cualquiera de estos invalida el gate. [INFERENCIA]

## Checklist de validación (acceptance gate)

- ¿La escritura está deshabilitada en modo `plan` por **hook**, no por convención? [DOC]
- ¿La aprobación es artefacto auditable (hash + aprobador + timestamp), no un "ok" en chat? [DOC]
- ¿Un cambio a `plan.md` tras firmado revierte a `plan` y re-pide firma? [DOC]
- ¿El hook enumera explícitamente las write-tools **y** los patrones de Bash mutante? [DOC]
- ¿Se rechaza `bypassPermissions` y la entrada vacía no fabrica plan? [DOC]
- ¿El plan firmado y el diff final quedan como rastro de lo autorizado? [DOC]

## Assets y validación offline

- `assets/` define el contrato determinístico de modo, plan firmado, aprobación, hook, write-tools y decisión de ejecución. [CÓDIGO]
- `scripts/check.sh` valida fixtures locales sin red, tiempo real ni aleatoriedad. [CÓDIGO]
- `scripts/validate_plan_mode_workflow.py` rechaza: write en `plan`, firma faltante, hash que no coincide, hook que no bloquea, Bash mutante en `plan`, `bypassPermissions`, o Guardian aprobando un caso bloqueado. [CÓDIGO]
- `evals.json` cubre happy path, gate de aprobación, workspace compartido, re-firma, Bash mutante bloqueado, falso positivo, entrada vacía y upgrade seguro. [CÓDIGO]

## Katas y skills relacionadas

- Kata 07 cubre el diseño del gate de aprobación read-only. [DOC]
- Relacionadas: `katas-plan-mode-exploration`, `custom-tooling-extension`, `human-escalation-design`. [DOC]
