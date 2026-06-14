# plan-mode-workflow

## Qué hace

Diseña un **gate de dos modos** para operar un repo o dominio desconocido sin
escritura prematura. En **Plan Mode** solo se permiten herramientas de lectura
(`Read`, `Grep`, `Glob`, `Bash` de inspección) y el resultado es un `plan.md`.
En **Execute Mode** se habilita la escritura, pero únicamente tras **firmar el
plan por hash**. La transición no la decide el modelo: la aplica un **hook
`PreToolUse`** que enumera y bloquea las write-tools mientras el modo sea `plan`.

El entregable no es prosa: es el **contrato determinístico del gate** —estado de
modo, plan firmado, evento de aprobación, hook y write-blocklist— que un proceso
externo puede leer y hacer cumplir (fail-closed).

## Cuándo usarla

- Antes de la **primera escritura** en un repo desconocido con blast radius no acotado.
- Cuando la organización exige **aprobación auditable** (hash + aprobador + timestamp) antes de mutar archivos.
- Cuando un **workspace compartido** corre riesgo de pisar trabajo no commiteado.
- Cuando el `plan.md` puede cambiar a mitad de camino y cada cambio debe **re-disparar la firma**.

**No usarla:** tareas sin escritura a repo (resúmenes, tablas, análisis). El gate
autoriza *ejecutar el plan*, no garantiza que el plan sea correcto, ni sustituye
permisos de plataforma o revisión de código.

## Cómo enruta y ejecuta

1. **Lead** encuadra el scope (¿hay escritura a repo? ¿hay objetivo?) y secuencia contrato-primero.
2. **Specialist** define la taxonomía de modos, señales y patrones de Bash mutante.
3. **Support** genera el esqueleto del hook y los fixtures de `scripts/check.sh`.
4. **Guardian** corre el gate de aceptación contra `assets/quality-rubric.json`: ningún caso bloqueado pasa en verde.

Estado inicial: `mode = "plan"`. Único camino a `execute`: `approve_plan(hash, approver)`.
Cambio de `plan.md` tras firmado → revierte a `plan` y re-pide firma.

## Evidencia

Cada afirmación lleva tag: `[CÓDIGO]` (hook/estado), `[CONFIG]` (policy/blocklist),
`[DOC]` (plan, aprobación), `[INFERENCIA]` / `[SUPUESTO]`. Sin precios. Single-brand (JM Labs).

## Referencias

- `SKILL.md` — capacidad, patrón correcto, anti-patrón, edge cases, checklist de aceptación.
- `knowledge/body-of-knowledge.md` — conceptos, estándares y reglas de decisión del gate.
- `knowledge/knowledge-graph.json` — grafo de los conceptos clave del gate.
- `prompts/` — prompt primario, meta y variaciones (quick / deep).
- `templates/output.md` — scaffold del entregable (contrato del gate).
- `examples/` — un caso trabajado (repo de pagos) entrada → salida.
- `assets/` — contrato determinístico (estado, plan, aprobación, hook, blocklist) y rúbrica de calidad.
- `evals/evals.json` — casos de activación, bloqueo y upgrade seguro.
