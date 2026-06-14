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
- Constitution v6.0.0 enforcement mode in execution phases (`references/ontology/`).
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

## Layout

```
catalog/      skills.json (truth) · consolidation-map.yaml · coverage-matrix.csv (611-row trace to alfa)
skills/       73 dirs: SKILL.md (+ references/ playbooks + evals.json)
references/   shared: brand/ guardrails/ ontology(v6)/ roles/ schemas/
harness/      manifest.json (+schema) → adapters + MCP configs
runtime/      core.md + per-runtime deltas → CLAUDE.md / AGENTS.md / GEMINI.md (generated)
hooks/        Claude Code hooks + guard scripts
migrate/      one-off porting scripts (deleted at GA)
```

## Token budgets (session start, CI-gated)

Measured (`evals/token-benchmark.json`, chars/4 applied identically to all arms — relative deltas hold under any consistent tokenizer; absolute counts will shift with the real tokenizer):

| Runtime | Alfa (measured) | Beta naive | Beta (measured) | vs alfa |
|---|---|---|---|---|
| Claude Code | 29,552 | 3,869 | **2,301** | **−92%** |
| Antigravity | 36,801 | 5,377 | **3,614** | **−90%** |
| Codex | 1,651 | 3,820 | **2,281** | +38%* |

\* Alfa's AGENTS.md carried no skill index — Codex sessions had no catalog access. Beta inlines the full 73-skill tier-0 index; the +630 tokens buy complete catalog routing. Honest trade-off, recorded as measured, not hidden.

Regenerate with `python3 scripts/token-stats.py`. The table updates **only** from committed benchmark data, never hand-typed (caveman honesty rule) — a number here with no matching commit in `evals/` is a bug.

## Acceptance criteria (GA gate)

- `scripts/validate-coverage.py` PASS — 611/611 dispositioned.
- `scripts/check-token-budget.py` green for all 3 runtimes (Codex +39% is an accepted, documented regression, not a failure).
- 3-runtime smoke: 10 canonical tasks pass on Claude Code, Antigravity, Codex.
- Generated surfaces match catalog: re-running `build-indexes.py` produces no diff.

Current private-preview note: on the universal branch inspected 2026-06-12,
`validate-coverage.py` passes and `check-token-budget.py` fails
(`claude-code 3075/2600`, `antigravity 4514/4000`, `codex 3118/2300`). [CONFIG]
That failure is a release blocker, not a hidden detail.

## Anti-scope

- Not a general agent framework — only the MetodologIA catalog, not arbitrary third-party skills.
- No per-runtime forks of skill logic; runtime differences live only in `runtime/*-deltas`.
- `migrate/` is throwaway and **deleted at GA** — do not build on it.
- No prices in any output; FTE-months + disclaimers only (governance rule).

## Status

- 611/611 alfa skills dispositioned (`scripts/validate-coverage.py` PASS).
- 73 beta skills (35 routers + 24 competencies + 14 jarvis-os), 351 aliases.
- Pending field validation: 3-runtime smoke (10 canonical tasks), Stitch-on-Codex proxy, Antigravity end-to-end MCP — run `scripts/auth-doctor.sh` first to rule out auth before debugging routing.
