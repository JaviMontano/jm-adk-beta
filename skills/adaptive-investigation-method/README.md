# Adaptive Investigation Method — Skill Overview

## What it does

Builds agents that investigate unknown domains (codebases, datasets, document corpora) **without burning the context budget**. The method combines three engineering moves: **cheap mapping** of the problem surface (`Glob`/`Grep`, no full reads), **explicit prioritization** of where to invest, and **selective deep-dive** only on promising nodes. Re-plan is disciplined: it fires *only* when evidence invalidates the active hypothesis — never reflexively every turn. A **hard budget** (reads or tokens) is the safety bound that guarantees termination even when the domain is effectively infinite.

The constructible artifact is a loop with: (1) a persisted scratchpad separating `plan` / `hypotheses` / `findings`; (2) a budget counter that decrements per expensive read; (3) a typed re-plan rule that only triggers on `hypothesis_invalidated`.

## When to use it

- An agent must understand a large repo or corpus before acting, and reading it all is infeasible.
- Exploration cost must be bounded by design (latency, tokens, tool calls).
- You want to avoid re-planning every turn and the resulting loops of doubt.
- You need traceability: why an area was explored and why another was discarded.

**Do not use** when the domain is small enough to read whole (< ~15 files or fits one context window), when the task is deterministic with no discovery, or when you already know the target node and only need to read it.

## How it routes / executes

1. **Define the hard budget** (`budget = N`) and persist the counter in the scratchpad.
2. **Map cheaply** with `Glob`/`Grep` — structure, names, entrypoints. Mapping does **not** spend budget.
3. **Formulate ranked hypotheses** by expected value / cost, each pointing at map nodes that confirm or invalidate it.
4. **Deep-dive selectively** into top-ranked nodes; each `Read` decrements budget and emits a `finding` with node reference + provenance tag.
5. **Re-plan only on invalidation** — re-prioritize when evidence refutes the active hypothesis; otherwise keep momentum.
6. **Close** on `budget_exhausted` or `goal_resolved`; synthesize the deliverable from `findings`, never from fuzzy memory.

The deterministic compiler validates a finished investigation spec:

```bash
python3 scripts/compile-adaptive-investigation.py --input path/to/investigation.json --format markdown
bash scripts/check.sh
```

## References and bundle

- `SKILL.md` — full capability contract, build steps, gate, self-correction, edge cases.
- `knowledge/body-of-knowledge.md` — core concepts, standards, decision rules.
- `knowledge/knowledge-graph.json` — concept graph over the method.
- `prompts/` — primary, meta, quick, deep prompts.
- `templates/output.md` — deliverable scaffold.
- `agents/` — lead / specialist / support / guardian role contracts.
- `examples/` — a worked auth-in-monorepo investigation.
- `assets/` — schema, policy, report template, and quality rubric consumed by the compiler and the gate (see `assets/README.md`).

## Evidence taxonomy

Every claim carries a provenance tag: `[DOC]` (documented in SKILL.md / spec), `[CÓDIGO]` (from code or compiler), `[CONFIG]` (from config), `[INFERENCIA]` (reasoned), `[SUPUESTO]` (assumption to confirm). Findings reuse the same taxonomy. Single brand: JM Labs. No invented prices; partial coverage is declared, never hidden.
