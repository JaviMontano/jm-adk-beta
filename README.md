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

| Runtime | Alfa | Beta target |
|---|---|---|
| Claude Code | ~14K | ≤2.6K |
| Antigravity | ~35-40K | ≤4K |
| Codex | ~20K | ≤2.3K |

Measured claims only: 3-arm benchmark committed before README tables update.
