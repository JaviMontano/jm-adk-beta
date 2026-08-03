# Pristino Beta

Catalog-driven multi-runtime agent harness. Successor of [jm-adk-alfa](https://github.com/JaviMontano/jm-adk-alfa) (frozen at tag `alfa-final`).

## Private Preview Status

Pristino Beta is a private pre-release harness. [CONFIG] It is not public yet and
is planned for public release with Ciclo 2 of the 2026 Programa de
Empoderamiento, after release gates pass. [SUPUESTO] If a user without access
opens or clones `JaviMontano/jm-adk-beta`, GitHub may return 404; that is the
expected behavior for a private repository.

Beta is a separate product line from Alfa. [CONFIG] Alfa remains the public,
operational harness for site/app creation, Hostinger/Firebase workflows, and
vibe coding today. Beta focuses on a smaller catalog-driven harness for the
vibe coder and the AI-native knowledge worker.

Start here:

- [Private preview](docs/pristino-beta/private-preview.md)
- [How to install private Beta](docs/pristino-beta/how-to-install-private-beta.md)
- [Prompt parametrico para empezar](docs/pristino-beta/prompt-parametrico-empezar.md)
- [Personas: vibe coder / knowledge worker](docs/pristino-beta/personas-vibe-coder-knowledge-worker.md)
- [FAQ](docs/pristino-beta/faq.md)

**611 alfa skills → 73 beta skills** (35 routers + 24 competencies + 14 jarvis-os) [CODE: `ls -d skills/*/` = 73], all 611 dispositioned and traced, no load-bearing capability dropped. Runs on **Claude Code, Antigravity, Codex** from one catalog.

## Principles

- `catalog/skills.json` = single source of truth; every runtime surface is generated, never hand-edited (`scripts/build-indexes.py`). Editing `CLAUDE.md`/`AGENTS.md`/`GEMINI.md` directly is an anti-pattern — changes are lost on regen.
- Script/template/prompt trilogy (spec-kit): deterministic scripts emit JSON → templates ingest → prompts add judgment. Determinism lives in scripts so prompts stay auditable.
- Phase gates = artifact existence (iikit): `scripts/check-prerequisites.sh --phase pN --json`. A phase is "done" only when its artifacts exist, not when a model asserts it.
- Constitution v7.0.0 enforcement mode in execution phases (`references/ontology/constitution-v7.0.0.md`); thin MUST/MUST NOT slice (`references/ontology/constitution-must.md`) for execution stages (L3 budget, paper §3.2).
- Compressed output contracts (caveman) in all subagents; token budgets CI-enforced (`scripts/check-token-budget.py`).

## Quickstart

```
python3 scripts/build-indexes.py                   # regenerate all runtime surfaces from catalog
python3 scripts/validate-coverage.py               # assert 611/611 alfa skills dispositioned
scripts/check-prerequisites.sh --phase p1 --json   # gate check before a phase
python3 scripts/token-stats.py                     # remeasure token budgets (updates table below)
scripts/auth-doctor.sh                             # diagnose per-runtime MCP/auth before smoke
```

Prereqs [ASSUMPTION, no version gate in scripts]: Python 3 + Bash; scripts are run from repo root. `.py` scripts are invoked via `python3` (not all carry the execute bit [CODE]); `.sh` scripts are executable. CI runs `validate-*.py` + `check-token-budget.py`; a red gate blocks merge.

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
catalog/      skills.json (truth) · consolidation-map.yaml · coverage-matrix.csv (611-row trace to alfa)
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

| Runtime | Alfa (measured) | Beta naive | Beta (measured) | vs alfa |
|---|---|---|---|---|
| Claude Code | 29,552 | 3,869 | **2,720** | **−91%** |
| Antigravity | 36,801 | 5,377 | **4,052** | **−89%** |
| Codex | 1,651 | 3,820 | **2,505** | +52%* |

\* Alfa's AGENTS.md carried no skill index — Codex sessions had no catalog access. Beta inlines the full 73-skill tier-0 index; the +854 tokens buy complete catalog routing. Honest trade-off, recorded as measured, not hidden.

Regenerate with `python3 scripts/token-stats.py`. The table updates **only** from committed benchmark data, never hand-typed (caveman honesty rule) — a number here with no matching commit in `evals/` is a bug.

## Acceptance criteria (GA gate)

- `scripts/validate-coverage.py` PASS — 611/611 dispositioned.
- `scripts/check-token-budget.py` green for all 3 runtimes (Codex +52% is an accepted, documented regression, not a failure).
- 3-runtime smoke: 10 canonical tasks pass on Claude Code, Antigravity, Codex.
- Generated surfaces match catalog: re-running `build-indexes.py` produces no diff.

Current private-preview status: `validate-coverage.py` PASS (611/611) and
`check-token-budget.py` PASS for all 3 runtimes
(`claude-code 2720/3000`, `antigravity 4052/4200`, `codex 2505/2600`). [CONFIG]
Headroom: claude 280, antigravity 148, codex 95. ICM routing + compliance audit
landed (PR #5, merged 2026-08-03); ICM workspace model elevated to `core.md`
(shared, all 3 runtimes, P2); all session-start gates green.

## Anti-scope

- Not a general agent framework — only the MetodologIA catalog, not arbitrary third-party skills.
- No per-runtime forks of skill logic; runtime differences live only in `runtime/*-deltas`.
- `migrate/` is throwaway and **deleted at GA** — do not build on it.
- No prices in any output; FTE-months + disclaimers only (governance rule).

## Status

- 611/611 alfa skills dispositioned (`scripts/validate-coverage.py` PASS).
- 73 beta skills (35 routers + 24 competencies + 14 jarvis-os), 351 aliases.
- ICM first-prompt routing live across all 3 runtimes; compliance audit + `plan-evolucion.md` landed (PR #5, merged 2026-08-03). Phase gates p0-p6 READY; token budgets PASS (claude 2601/3000, antigravity 3812/4000, codex 2386/2600); coverage 611; evals 36/36. [CONFIG]
- Pending field validation: 3-runtime smoke (10 canonical tasks), Stitch-on-Codex proxy, Antigravity end-to-end MCP — run `scripts/auth-doctor.sh` first to rule out auth before debugging routing.
