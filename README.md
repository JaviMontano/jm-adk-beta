# Pristino Beta

Catalog-driven multi-runtime agent harness. Successor of [jm-adk-alfa](https://github.com/JaviMontano/jm-adk-alfa) (frozen at tag `alfa-final`).

**611 skills → ~92** (routers + hardened core + shared library) keeping all load-bearing functionality. Runs on **Claude Code, Antigravity, Codex**.

## Principles

- `catalog/skills.json` = single source of truth; every runtime surface generated (`scripts/build-indexes.py`).
- Script/template/prompt trilogy (spec-kit): deterministic scripts emit JSON → templates ingest → prompts add judgment.
- Phase gates = artifact existence (iikit): `scripts/check-prerequisites.sh --phase pN --json`.
- Constitution v6.0.0 enforcement mode in execution phases.
- Compressed output contracts (caveman) in all subagents; token budgets CI-enforced (`scripts/check-token-budget.py`).

## Layout

```
catalog/      skills.json (truth) · consolidation-map.yaml · coverage-matrix.csv (611-row trace to alfa)
skills/       ~92 dirs: SKILL.md (+ references/ playbooks + evals.json)
references/   shared: brand/ guardrails/ ontology(v6)/ roles/ schemas/
harness/      manifest.json (+schema) → adapters + MCP configs
runtime/      core.md + per-runtime deltas → CLAUDE.md / AGENTS.md / GEMINI.md (generated)
hooks/        Claude Code hooks + guard scripts
migrate/      one-off porting scripts (deleted at GA)
```

## Token budgets (session start, CI-gated)

Measured (`evals/token-benchmark.json`, chars/4 applied identically to all arms):

| Runtime | Alfa (measured) | Beta naive | Beta (measured) | vs alfa |
|---|---|---|---|---|
| Claude Code | 29,552 | 3,869 | **2,294** | **−92%** |
| Antigravity | 36,801 | 5,377 | **2,990** | **−92%** |
| Codex | 1,651 | 3,820 | **2,289** | +39%* |

\* Alfa's AGENTS.md carried no skill index — Codex sessions had no catalog access.
Beta inlines the full 73-skill tier-0 index; the +638 tokens buy complete
catalog routing. Honest trade-off, recorded as measured.

Regenerate: `python3 scripts/token-stats.py`. README table updates only from
committed benchmark data (caveman honesty rule).

## Status

- 611/611 alfa skills dispositioned (`scripts/validate-coverage.py` PASS)
- 73 beta skills (35 routers + 24 competencies + 14 jarvis-os), 351 aliases
- Pending field validation: 3-runtime smoke (10 canonical tasks), Stitch-on-Codex
  proxy, Antigravity end-to-end MCP (`scripts/auth-doctor.sh` to check auth)
