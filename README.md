# Pristino Beta

> Harness catalog-driven para el **vibe coder** y el **AI-native knowledge worker**. Un solo catálogo de skills corre en **Claude Code, Antigravity y Codex**; el harness carga contexto por capas (≤8k tokens por etapa) en vez de un prompt monolítico, y verifica cada fase con gates determinísticos antes de declararla lista.

---

## Qué es

Pristino Beta es un harness agentico catalog-driven. El catálogo (`catalog/skills.json`) es la fuente única de verdad: cada superficie de runtime (CLAUDE.md, AGENTS.md, GEMINI.md) se **genera** desde el catálogo, nunca se edita a mano. El harness implementa la [Interpretable Context Methodology (ICM)](https://arxiv.org/abs/2603.16021) — estructura-de-carpetas-como-arquitectura — para mantener el contexto por etapa en 2-8k tokens en lugar de un prompt monolítico de 30-50k. Cada fase se valida con gates determinísticos (existencia de artefactos, no aserción del modelo).

**73 catalog skills** (35 routers + 24 competencies + 14 jarvis-os), 351 aliases. **611 capabilities traced and dispositioned** — sin perder capacidad load-bearing. Corre en Claude Code, Antigravity y Codex desde un solo catálogo.

## Para quién

- **Vibe coder** — crea mini y super apps en ciclos build-run-observe, con tests, seguridad y evidencia en cada paso.
- **Knowledge worker** — delega investigación, síntesis, briefs y decisiones con proveniencia y disciplina de fuentes.
- **Perfil MetodologIA** — activa reglas de marca, calidad y comercial cuando el entregable pertenece al ecosistema MetodologIA.

## Principios

- `catalog/skills.json` = fuente única de verdad; cada superficie de runtime se genera, nunca se edita a mano (`scripts/build-indexes.py`). Editar `CLAUDE.md`/`AGENTS.md`/`GEMINI.md` directamente es un anti-patrón — los cambios se pierden al regenerar.
- Trilogía script/template/prompt (spec-kit): scripts determinísticos emiten JSON → templates lo ingieren → prompts añaden juicio. El determinismo vive en scripts para que los prompts sean auditable.
- Phase gates = existencia de artefactos (iikit): `scripts/check-prerequisites.sh --phase pN --json`. Una fase está "lista" solo cuando sus artefactos existen en disco, no cuando un modelo lo afirma.
- Constitution v7.0.0 enforcement en fases de ejecución (`references/ontology/constitution-v7.0.0.md`); slice delgado MUST/MUST NOT (`references/ontology/constitution-must.md`) para stages de ejecución (L3 budget, paper §3.2).
- Contratos de salida comprimidos (caveman) en todos los subagentes; token budgets CI-enforced (`scripts/check-token-budget.py`).

## Quickstart

```
python3 scripts/build-indexes.py                   # regenera todas las superficies desde el catálogo
python3 scripts/validate-coverage.py               # verifica 611 capabilities dispositioned
scripts/check-prerequisites.sh --phase p1 --json   # gate check antes de una fase
python3 scripts/token-stats.py                     # remide token budgets (actualiza tabla abajo)
scripts/auth-doctor.sh                             # diagnostica MCP/auth por runtime antes de smoke
```

Prerequisitos [SUPUESTO, sin version-gate en scripts]: Python 3 + Bash; los scripts se ejecutan desde la raíz del repo. Los scripts `.py` se invocan con `python3` (no todos tienen execute bit [CÓDIGO]); los `.sh` son ejecutables. CI corre `validate-*.py` + `check-token-budget.py`; un gate rojo bloquea merge.

## ICM routing (primer prompt)

Este harness implementa la [Interpretable Context Methodology (ICM)](https://arxiv.org/abs/2603.16021) — estructura-de-carpetas-como-arquitectura: un modelo de contexto de 5 capas (L0 identidad `CLAUDE.md` → L1 workspace `CONTEXT.md` routing → L2 stage `CONTEXT.md` contrato → L3 referencias/config factory → L4 output de trabajo) que mantiene el contexto por etapa en 2-8k tokens en lugar de un prompt monolítico de 30-50k. [DOC]

Tres scripts determinísticos operacionalizan ICM en runtime:

- **`scripts/first-prompt-router.sh`** — en el primer turno detecta modo (`create_project` | `resume_project` | `new_task` | `resume_task` | `ambiguous`) desde prompt + working dir, emite líneas `ROUTE-*` KEY:VALUE (`ENTENDIDO`, `MODO`, `SUPUESTOS`, `GAPS`, `PERFIL`, `SKILL/ROUTER candidato`, `TAREA PROPUESTA`, `GATE`). `ambiguous` → emite `coverage_gap`, pregunta, NO edita. Claude Code enforcement vía `stop-validator.sh` (sensor); Codex/Antigravity enforcement manual (sin hooks engine). [CONFIG]
- **`scripts/workspace-bootstrap.sh <slug> --apply`** — instancia un workspace desde `_template/` (4 stages: `01_discovery` → `02_spec` → `03_build` → `04_validate`); un stage = un job (principio ICM). [CONFIG]
- **`scripts/stage-context-manifest.sh <stage>`** — hace ejecutable la tabla `## Inputs` del `CONTEXT.md` del stage: resuelve paths L0-L4, suma el stack de tokens por etapa (chars/4), advierte >8000t. El paper *afirma* 2-8k/stage; este harness *lo enforcementa* (sensor determinístico, no aserción). Modo `--json`; modo `--enforce` (gate hard, exit 1 over-budget). [CONFIG]

**Delegación sub-agent (paper §4.1):** pasa solo el contexto scoped del stage activo a los sub-agentes, nunca el workspace entero — la estructura de carpetas *es* el contrato de delegación. [DOC]

Decision records: [ADR-0001 — ICM first-prompt routing](docs/decisions/0001-icm-first-prompt-routing.md) · [ADR-0002 — ICM compliance audit](docs/decisions/0002-icm-compliance-audit.md). Auditoría de cumplimiento vs el paper (vía NotebookLM) confirmó que el harness iguala o supera cada claim del paper: sensores determinísticos + stop-validator (el paper solo advierte), catálogo multi-runtime (73 skills on-demand vs bundle estático), constitution v7 gates + coverage/evals. [DOC]

## Layout

```
catalog/      skills.json (truth) · consolidation-map.yaml · coverage-matrix.csv (611-row trace)
skills/       73 dirs: SKILL.md (+ references/ playbooks + evals.json)
agents/       21 agent definitions (orchestrators + specialists; Claude Code Task tool)
commands/     5 slash commands (session, pristino, brand, iikit, jarvis)
references/   shared: brand/ guardrails/ ontology(v7 + must slice)/ roles/ schemas/
harness/      manifest.json (+schema) → adapters + MCP configs
runtime/      core.md + per-runtime deltas → CLAUDE.md / AGENTS.md / GEMINI.md (generated)
hooks/        Claude Code hooks + guard scripts
scripts/      build-indexes.py · check-prerequisites.sh · token-stats.py · first-prompt-router.sh · stage-context-manifest.sh · workspace-bootstrap.sh
workspace/    _template/ (ICM 4-stage: discovery/spec/build/validate) + instances
evals/        token-benchmark.json (CI-gated budget truth)
discovery/    active-plugin discovery artifacts
project/      active-plugin project artifacts
migrate/      one-off porting scripts (deleted at GA)
```

## Token budgets (session start, CI-gated)

Medidos (`evals/token-benchmark.json`, chars/4 aplicado idéntico a todos los arms — los deltas relativos se mantienen bajo cualquier tokenizer consistente; los conteos absolutos shiftan con el tokenizer real):

| Runtime | Session-start (medido) | Cap |
|---|---|---|
| Claude Code | **2,720** | 3,000 |
| Antigravity | **4,052** | 4,200 |
| Codex | **2,505** | 2,600 |

Headroom: claude 280, antigravity 148, codex 95. Regenera con `python3 scripts/token-stats.py`. La tabla se actualiza **solo** desde datos de benchmark commiteados, nunca tipeada a mano (regla caveman honesty) — un número aquí sin commit en `evals/` es un bug.

## Acceptance criteria (GA gate)

- `scripts/validate-coverage.py` PASS — 611/611 capabilities dispositioned.
- `scripts/check-token-budget.py` green para los 3 runtimes.
- 3-runtime smoke: 10 tareas canónicas pasan en Claude Code, Antigravity, Codex.
- Superficies generadas matchean catálogo: re-correr `build-indexes.py` produce sin diff.

## Anti-scope

- No es un framework agentico general — solo el catálogo MetodologIA, no skills arbitrarios de terceros.
- No forks por runtime de la lógica de skills; las diferencias de runtime viven solo en `runtime/*-deltas`.
- `migrate/` es throwaway y **se borra al GA** — no construir sobre él.
- No precios en ningún output; FTE-months + disclaimers solo (regla governance).

## Status

- 611 capabilities traced and dispositioned (`scripts/validate-coverage.py` PASS).
- 73 catalog skills (35 routers + 24 competencies + 14 jarvis-os), 351 aliases.
- ICM first-prompt routing live en los 3 runtimes; compliance audit + ICM workspace model elevado a `core.md` (compartido, 3 runtimes); `--enforce` gate en `stage-context-manifest`; sensor de consistencia governance (true gate). Token budgets PASS (claude 2720/3000, antigravity 4052/4200, codex 2505/2600); coverage 611; evals 36/36. [CONFIG]
- Pendiente validación en campo: 3-runtime smoke (10 tareas canónicas), Stitch-on-Codex proxy, Antigravity end-to-end MCP — correr `scripts/auth-doctor.sh` primero para descartar auth antes de debuggear routing.

---

# Pristino Beta (English)

> A catalog-driven harness for the **vibe coder** and the **AI-native knowledge worker**. One skill catalog runs on **Claude Code, Antigravity and Codex**; the harness loads context in layers (≤8k tokens per stage) instead of a monolithic prompt, and verifies every phase with deterministic gates before calling it done.

---

## What it is

Pristino Beta is a catalog-driven agentic harness. The catalog (`catalog/skills.json`) is the single source of truth: every runtime surface (CLAUDE.md, AGENTS.md, GEMINI.md) is **generated** from the catalog, never hand-edited. The harness implements the [Interpretable Context Methodology (ICM)](https://arxiv.org/abs/2603.16021) — folder-structure-as-architecture — to keep per-stage context at 2-8k tokens instead of a 30-50k monolithic prompt. Every phase is validated with deterministic gates (artifact existence, not model assertion).

**73 catalog skills** (35 routers + 24 competencies + 14 jarvis-os), 351 aliases. **611 capabilities traced and dispositioned** — no load-bearing capability dropped. Runs on Claude Code, Antigravity and Codex from one catalog.

## Who it's for

- **Vibe coder** — build mini and super apps in build-run-observe loops, with tests, security and evidence at every step.
- **Knowledge worker** — delegates research, synthesis, briefs and decisions with provenance and source discipline.
- **MetodologIA profile** — activates brand, quality and commercial rules when the deliverable belongs to the MetodologIA ecosystem.

## Principles

- `catalog/skills.json` = single source of truth; every runtime surface is generated, never hand-edited (`scripts/build-indexes.py`). Editing `CLAUDE.md`/`AGENTS.md`/`GEMINI.md` directly is an anti-pattern — changes are lost on regen.
- Script/template/prompt trilogy (spec-kit): deterministic scripts emit JSON → templates ingest → prompts add judgment. Determinism lives in scripts so prompts stay auditable.
- Phase gates = artifact existence (iikit): `scripts/check-prerequisites.sh --phase pN --json`. A phase is "done" only when its artifacts exist on disk, not when a model asserts it.
- Constitution v7.0.0 enforcement in execution phases (`references/ontology/constitution-v7.0.0.md`); thin MUST/MUST NOT slice (`references/ontology/constitution-must.md`) for execution stages (L3 budget, paper §3.2).
- Compressed output contracts (caveman) in all subagents; token budgets CI-enforced (`scripts/check-token-budget.py`).

## Quickstart

```
python3 scripts/build-indexes.py                   # regenerate all runtime surfaces from catalog
python3 scripts/validate-coverage.py               # assert 611 capabilities dispositioned
scripts/check-prerequisites.sh --phase p1 --json   # gate check before a phase
python3 scripts/token-stats.py                     # remeasure token budgets (updates table below)
scripts/auth-doctor.sh                             # diagnose per-runtime MCP/auth before smoke
```

Prereqs [ASSUMPTION, no version gate in scripts]: Python 3 + Bash; scripts run from repo root. `.py` scripts invoked via `python3` (not all carry the execute bit [CODE]); `.sh` scripts are executable. CI runs `validate-*.py` + `check-token-budget.py`; a red gate blocks merge.

## ICM routing (first prompt)

This harness implements the [Interpretable Context Methodology (ICM)](https://arxiv.org/abs/2603.16021) — folder-structure-as-architecture: a 5-layer context model (L0 identity `CLAUDE.md` → L1 workspace `CONTEXT.md` routing → L2 stage `CONTEXT.md` contract → L3 references/config factory → L4 working output) that keeps per-stage context at 2-8k tokens instead of a 30-50k monolithic prompt. [DOC]

Three deterministic scripts operationalize ICM at runtime:

- **`scripts/first-prompt-router.sh`** — on the first turn, detects mode (`create_project` | `resume_project` | `new_task` | `resume_task` | `ambiguous`) from prompt + working dir, emits `ROUTE-*` KEY:VALUE lines (`ENTENDIDO`, `MODO`, `SUPUESTOS`, `GAPS`, `PERFIL`, `SKILL/ROUTER candidato`, `TAREA PROPUESTA`, `GATE`). `ambiguous` → emit `coverage_gap`, ask, do NOT edit. Claude Code enforces the block via `stop-validator.sh` (sensor); Codex/Antigravity enforce manually (no hooks engine). [CONFIG]
- **`scripts/workspace-bootstrap.sh <slug> --apply`** — instantiates a workspace from `_template/` (4 stages: `01_discovery` → `02_spec` → `03_build` → `04_validate`); one stage = one job (ICM principle). [CONFIG]
- **`scripts/stage-context-manifest.sh <stage>`** — makes the stage `CONTEXT.md` `## Inputs` table *executable*: resolves L0-L4 paths, sums the per-stage token stack (chars/4), warns on >8000t. The paper *claims* 2-8k/stage; this harness *enforces* it (a deterministic sensor, not an assertion). `--json` mode; `--enforce` mode (gate hard, exit 1 on over-budget). [CONFIG]

**Sub-agent delegation (paper §4.1):** pass only the active stage's scoped context to sub-agents, never the whole workspace — folder structure *is* the delegation contract. [DOC]

Decision records: [ADR-0001 — ICM first-prompt routing](docs/decisions/0001-icm-first-prompt-routing.md) · [ADR-0002 — ICM compliance audit](docs/decisions/0002-icm-compliance-audit.md). Compliance audit vs the paper (via NotebookLM) confirmed the harness matches or exceeds every paper claim: deterministic sensors + stop-validator (paper only warns), multi-runtime catalog (73 on-demand skills vs static bundle), constitution v7 gates + coverage/evals. [DOC]

## Layout

```
catalog/      skills.json (truth) · consolidation-map.yaml · coverage-matrix.csv (611-row trace)
skills/       73 dirs: SKILL.md (+ references/ playbooks + evals.json)
agents/       21 agent definitions (orchestrators + specialists; Claude Code Task tool)
commands/     5 slash commands (session, pristino, brand, iikit, jarvis)
references/   shared: brand/ guardrails/ ontology(v7 + must slice)/ roles/ schemas/
harness/      manifest.json (+schema) → adapters + MCP configs
runtime/      core.md + per-runtime deltas → CLAUDE.md / AGENTS.md / GEMINI.md (generated)
hooks/        Claude Code hooks + guard scripts
scripts/      build-indexes.py · check-prerequisites.sh · token-stats.py · first-prompt-router.sh · stage-context-manifest.sh · workspace-bootstrap.sh
workspace/    _template/ (ICM 4-stage: discovery/spec/build/validate) + instances
evals/        token-benchmark.json (CI-gated budget truth)
discovery/    active-plugin discovery artifacts
project/      active-plugin project artifacts
migrate/      one-off porting scripts (deleted at GA)
```

## Token budgets (session start, CI-gated)

Measured (`evals/token-benchmark.json`, chars/4 applied identically to all arms — relative deltas hold under any consistent tokenizer; absolute counts will shift with the real tokenizer):

| Runtime | Session-start (measured) | Cap |
|---|---|---|
| Claude Code | **2,720** | 3,000 |
| Antigravity | **4,052** | 4,200 |
| Codex | **2,505** | 2,600 |

Headroom: claude 280, antigravity 148, codex 95. Regenerate with `python3 scripts/token-stats.py`. The table updates **only** from committed benchmark data, never hand-typed (caveman honesty rule) — a number here with no matching commit in `evals/` is a bug.

## Acceptance criteria (GA gate)

- `scripts/validate-coverage.py` PASS — 611/611 capabilities dispositioned.
- `scripts/check-token-budget.py` green for all 3 runtimes.
- 3-runtime smoke: 10 canonical tasks pass on Claude Code, Antigravity, Codex.
- Generated surfaces match catalog: re-running `build-indexes.py` produces no diff.

## Anti-scope

- Not a general agent framework — only the MetodologIA catalog, not arbitrary third-party skills.
- No per-runtime forks of skill logic; runtime differences live only in `runtime/*-deltas`.
- `migrate/` is throwaway and **deleted at GA** — do not build on it.
- No prices in any output; FTE-months + disclaimers only (governance rule).

## Status

- 611 capabilities traced and dispositioned (`scripts/validate-coverage.py` PASS).
- 73 catalog skills (35 routers + 24 competencies + 14 jarvis-os), 351 aliases.
- ICM first-prompt routing live across all 3 runtimes; compliance audit + ICM workspace model elevated to `core.md` (shared, 3 runtimes); `--enforce` gate on `stage-context-manifest`; governance consistency sensor (true gate). Token budgets PASS (claude 2720/3000, antigravity 4052/4200, codex 2505/2600); coverage 611; evals 36/36. [CONFIG]
- Pending field validation: 3-runtime smoke (10 canonical tasks), Stitch-on-Codex proxy, Antigravity end-to-end MCP — run `scripts/auth-doctor.sh` first to rule out auth before debugging routing.