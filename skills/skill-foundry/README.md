# skill-foundry

Router skill for **building and certifying agentic assets**. One request in, one
specialist playbook out. The foundry never builds the asset itself — it resolves
the request to exactly ONE of 16 playbooks (skills, agents, commands, prompts,
hooks, MCP servers, workflows) and hands off. [DOC]

## What it does

Given a `topic` (one of 16 enum values) plus a `depth` (`quick`|`deep`), the
foundry reads exactly one reference playbook from `references/` and runs it under
a shared gate: constitution v6.0.0, Alfa-set evidence tags, single-brand output,
no invented prices, no green-as-success. [DOC]

The 16 routes fall into four families:

| Family | Routes | Job |
|--------|--------|-----|
| Create assets | `agent-creator`, `prompt-creator`, `hook-creator`, `mcp-creator`, `workflow-creator`, `workflow-forge`, `meta-skill-creator`, `prompt-forge` | Produce a new, validated asset definition |
| Design / spec | `design-skill` | Detailed skill spec before any build |
| Quality pipeline | `x-ray-skill` (audit), `certify-skill` (verdict), `benchmark-skill` (A/B diff), `assembly-skill` (full pipeline) | Diagnose, grade, compare, production-ize |
| Index / search | `meta-skill-indexer`, `skill-search`, `auto-prompt-matching` | Build the BM25 index, find skills, match prompts |

## When to use

Use when the verb is **build-an-asset** and the noun is one of the topics above:
"create an agent", "certify this skill", "forge a slash command", "design a
skill spec", "audit a skill", "benchmark v1 vs v2", "index all skills". [DOC]

Do **not** use to *run* an existing asset, edit unrelated files, or answer a
domain question. Those are out of foundry scope — redirect, do not force a route. [INFERENCE]

## How it routes / executes

1. Resolve `topic` against the enum using the `desc` trigger phrases in
   `routes.json`. [DOC]
2. Read EXACTLY ONE playbook from `references/<topic>.md`. Never load the cluster
   "to compare" — one route per invocation keeps context lean. [DOC]
3. Apply by `depth`: `quick` runs the essentials path; `deep` runs the
   exhaustive path with verification at each step. [DOC]
4. Run the playbook's own acceptance gate plus the shared validation gate before
   reporting done. [DOC]

Spine: **Discover → Analyze → Execute → Validate**. [DOC]

## References

- `SKILL.md` — router contract, params, tie-breakers, validation gate.
- `routes.json` — topic → playbook map with trigger descriptions.
- `references/*.md` — the 16 specialist playbooks (one per topic).
- `knowledge/body-of-knowledge.md` — routing model, families, evidence taxonomy.
- `agents/` — lead / specialist / support / guardian role contracts.
- `prompts/` — primary, meta, and quick/deep variation prompts.
- `templates/output.md` — the routing-decision deliverable scaffold.
- `assets/` — quality rubric and routing checklist (see `assets/README.md`).
- `evals/evals.json` — routing-accuracy and gate-enforcement test cases.
