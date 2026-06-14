# Pristino Beta — Core Contract

Generated adapter (source: runtime/core.md + delta). Do NOT hand-edit — regenerated on every build; manual changes lost. [DOC]

## Identity

Catalog-driven harness. 3 brands, never mixed — identify brand FIRST. [DOC]
- Sofka (enterprise) · MetodologIA (open) · JM Labs (personal).
- [SUPUESTO] Brand inferable from context; if ambiguous, HALT and ask — never default.

## Hard rules

1. Evidence tag on every claim: `[CÓDIGO]` `[CONFIG]` `[DOC]` `[INFERENCIA]` `[SUPUESTO]`. Untagged = defect.
2. NEVER prices — FTE-months + disclaimers only. No currency, rates, totals.
3. Read before write; `catalog/skills.json` = single source of truth. Stale read → re-read, never assume.
4. Script-first: any step expressible as a script IS a script under `scripts/`. Prose only for non-deterministic logic.
5. Constitution v6.0.0 enforced in execution phases: extract MUST/MUST NOT, HALT on violation (`references/ontology/constitution-v6.0.0.md`). [DOC]
6. Verification before done — proven by artifact existence, never assertion.

## Skill protocol

- Tier-0 index = one line per skill. Invoke → Read that skill's `SKILL.md` only; never preload siblings.
- Routers (®): resolve `params` from request (ask ONLY if ambiguous), Read exactly ONE playbook from `routes:`. Never load the whole cluster.
- `depth=quick|deep`, default `quick`. Escalate to `deep` only on explicit request or failed `quick`.
- Subagent output compressed (locator / receipt / findings, `references/roles/`).
- Auto-clarity override — normal prose (not compressed) for: security warnings, irreversible actions, ordered sequences.

## Phase gates

- Completion = artifact existence: `scripts/check-prerequisites.sh --phase <p> --json`. Truth is the filesystem, not the log.
- Soft gates warn and continue; hard gates require 100% and BLOCK on miss.
- [SUPUESTO] `--json` is machine-parsed by the orchestrator; non-zero exit = gate failure.

## Anti-scope

- [SUPUESTO] This adapter governs runtime behavior only; building the adapter itself is out of scope (owned by the delta + generator).
- No brand mixing, no price emission, no untagged claims, no whole-cluster reads, no "done" without an artifact. Any = contract breach, HALT.

## Acceptance criteria

- Every claim carries exactly one evidence tag; no price tokens.
- Single brand per output; brand declared before first content line.
- Each phase marked complete has its prerequisite artifacts on disk (gate script verified), not asserted.
- Constitution MUST/MUST NOT extracted and unviolated for every execution-phase action.

## Antigravity delta

Deltas vs baseline harness. Apply only here; do not port to other runtimes. [EXPLICIT]

- No hooks engine [INFERENCE]: run `bash scripts/session-init.sh` at session start — only when state is needed (resume, multi-task, or `[P]` work); skip for one-shot reads. Idempotent; rerun is safe.
- Skill index `.agent/skills_index.json` (generated, minimal fields) [CONFIG]: do not hand-edit — regenerate. MCP config: `~/.gemini/config/mcp_config.json` [CONFIG].
- No subagent dispatch [INFERENCE]: execute `[P]` tasks sequentially in listed order; no parallel fan-out, no nested agents.
- Done = init ran (if required), `[P]` tasks all sequential, no hook/subagent assumptions leaked [ASSUMPTION]. If a step needs a missing engine, stop and flag — never silently emulate. [EXPLICIT]

Skill index: `.agent/skills_index.json` (generated, minimal fields).
