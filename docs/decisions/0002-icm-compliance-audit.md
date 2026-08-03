# ADR-0002 — ICM compliance audit (paper vs harness, "igual o mejor")

- **Date:** 2026-08-03
- **Status:** Accepted
- **Sources:** ICM paper arXiv 2603.16021v2 (notebook 13845882, queried via NotebookLM), harness-engineering notebook (c94c6afa), `references/ontology/constitution-v7.0.0.md`, `plan-evolucion.md` §3
- **Evidence:** [DOC] [CONFIG]

## Context

The user requested an audit of the `jm-adk-beta` harness against the ICM paper
("Interpretable Context Methodology: Folder Structure as Agent Architecture",
arXiv 2603.16021v2) to verify it auto-orchestrates skills/workflows/agents per the
paper — "igual o mejor" (equal or better). The audit was run via NotebookLM
queries against the paper and the harness-engineering notebook.

Gaps found (evidence-tagged in `plan-evolucion.md` §3):

1. **ICM model lived only in `runtime/delta-claude.md`.** Codex/Antigravity
   inherited it via a fragile reference ("fields: `delta-claude.md` § First-prompt
   routing") rather than a first-class shared contract. [DOC]
2. **The workspace template was incomplete.** Stage `CONTEXT.md` files
   referenced `output/` directories that did not exist; no `_config/` home for
   Layer-3 stable references; no sub-agent delegation section (paper §4.1). [CONFIG]
3. **The paper's per-stage budget (2-8k tokens, §3.2) was a CLAIM, not enforced.**
   `01_discovery` loaded the full constitution (5292t) + a skill (2743t) = 8035t
   in L3 alone — over the paper's own cap. Nothing detected this. [CONFIG]
4. **No decision record** existed for the audit or for the `constitution-must.md`
   slice. [DOC]

## Decision

Four closures, all respecting the anti-scope boundary ("adapter governs runtime
behavior only; building the adapter is out of scope"):

1. **`scripts/stage-context-manifest.sh` — make the Inputs table executable.**
   The paper's §3.2 Inputs table is static prose; the harness turns it into a
   deterministic sensor that resolves L0-L4 paths, sums the per-stage token stack
   (chars/4), and warns on >8000t. The paper *claims* 2-8k/stage; the harness
   *enforces* it. `--json` mode; `--enforce` mode (gate hard, exit 1 on
   over-budget — added in P3). [CONFIG]

2. **`references/ontology/constitution-must.md` — configure the factory, not the
   product (paper §3.1 P5).** A thin L3 slice (~811t) carries only the binding
   MUST/MUST NOT + evidence taxonomy + gates. The full constitution (5292t) stays
   authoritative for human rationale but is NOT loaded into execution stages
   (it would blow the L3 budget). Execution stages (03_build, 04_validate) load
   the slice; the full doc is read only for audits. [DOC]

3. **Template completeness.** Pre-created `output/.gitkeep` in all 4 stages,
   `_config/.gitkeep` (Layer-3 stable-reference home), sub-agent delegation
   section in `workspace/_template/CONTEXT.md` (pass only the active stage's
   scoped context, never the whole workspace — paper §4.1), review gates at
   each stage handoff. [CONFIG]

4. **ICM model elevation to `core.md` (P2, deferred).** The 5-layer model,
   one-stage-one-job, edit-source principle, and `stage-context-manifest` move
   to `runtime/core.md` so all three runtimes inherit it first-class — not via a
   fragile cross-delta reference. P2 carries the budget risk (headroom:
   antigravity 188t, codex 214t) and is tracked in `plan-evolucion.md` §4 P2. [DOC]

## Consequences

- **Budget enforced, not claimed.** A deterministic sensor catches the
  over-budget case the paper only warns about. All 4 stages now measure
  <8000t (6206 / 3814 / 4246 / 4723). [CONFIG]
- **All runtimes inherit ICM first-class (after P2).** No fragile delta-to-delta
  reference. [DOC]
- **Anti-scope respected.** The sensor and the slice are runtime artifacts
  (scripts + references), not adapter-build changes. The generated adapter
  contract is untouched. [DOC]
- **Harness matches or exceeds every paper claim:**
  - Deterministic sensors + `stop-validator.sh` where the paper only warns. [CONFIG]
  - Multi-runtime catalog (73 on-demand skills via `catalog/skills.json`) vs the
    paper's static context bundle. [CONFIG]
  - Constitution v7 gates (G0-G3) + `validate-coverage.py` (611) + `validate-evals.py`
    (36/36) — enforcement the paper does not specify. [CONFIG]
  - Edit-source principle operationalized (fix the script/source, not the output). [DOC]

## Rejected alternatives

- **Hand-edit generated files** (`CLAUDE.md`/`AGENTS.md`/`GEMINI.md`) to embed the
  ICM model — **rejected**: violates the generated-adapter contract ("Do NOT
  hand-edit — regenerated on every build; manual changes lost"). Fix the source,
  regenerate. [DOC]
- **Load the full constitution into execution stages** — **rejected**: 5292t
  exceeds the paper's own L3 cap (500-2k tok, §3.2); blew the per-stage budget.
  The thin slice is the paper's own "configure the factory" principle applied to
  the constitution itself. [DOC]
- **Keep ICM in `delta-claude.md` only** — **rejected**: codex/antigravity inherit
  via a fragile reference; P2 elevates to `core.md` as the shared contract. [DOC]

## Cross-references

- `plan-evolucion.md` §3 (baseline audit, evidence-tagged gaps)
- `plan-evolucion.md` §4 P2 (ICM elevation to `core.md`, budget risk)
- ADR-0001 (ICM first-prompt routing — the runtime mechanism this audit validated)
- `references/ontology/constitution-must.md` (the slice; derived, not authoritative)
- `scripts/stage-context-manifest.sh` (the executable Inputs-table sensor)