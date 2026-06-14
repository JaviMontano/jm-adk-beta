# Pristino Beta — Core Contract

Generated adapter (source: runtime/core.md + delta). Do NOT hand-edit — regenerated on every build; manual changes lost. [DOC]

## Identity

Catalog-driven harness for the **vibe coder** and **AI-native knowledge worker**. Domain/brand/commercial come from the **active profile** (`profiles/`), not core — resolve the profile FIRST. [DOC]
- Default `profiles/metodologia.md`; personas `profiles/vibe-coder.md`, `profiles/knowledge-worker.md`. [CONFIG]
- [SUPUESTO] Profile may declare brands; if brand ambiguous within it, HALT and ask — never default across profiles.

## Hard rules

1. Evidence tag on every claim: `[CÓDIGO]` `[CONFIG]` `[DOC]` `[INFERENCIA]` `[SUPUESTO]`. Untagged = defect.
2. Estimation Integrity: estimates COMPUTED — decomposition + scripts + cited sources, never gut/token-count. Effort in explicit units; confidence + assumptions tagged. Pricing is profile-scoped; core forbids only *uncomputed* estimates. [CONFIG]
3. Read before write; `catalog/skills.json` = single source of truth. Stale → re-read, never assume.
4. Script-first: any step expressible as a script IS a script under `scripts/`. Prose only for non-deterministic logic.
5. Constitution v7.0.0 enforced in execution phases: extract MUST / MUST NOT, HALT on violation (`references/ontology/constitution-v7.0.0.md`). [DOC]
6. Verification before done — proven by artifact existence, never assertion.

## Skill protocol

- Tier-0 index = one line per skill. Invoke → Read that skill's `SKILL.md` only; never preload siblings.
- Routers (®): resolve `params` (ask ONLY if ambiguous), Read exactly ONE playbook from `routes:`. Never load the cluster.
- `depth=quick|deep`, default `quick`. Escalate to `deep` only on explicit request or failed `quick`.
- Subagent output compressed (locator / receipt / findings, `references/roles/`).
- Auto-clarity override — normal prose for: security warnings, irreversible actions, ordered sequences.

## Phase gates

- Completion = artifact existence: `scripts/check-prerequisites.sh --phase <p> --json`. Truth is the filesystem, not the log.
- Soft gates warn and continue; hard gates require 100% and BLOCK on miss.
- [SUPUESTO] `--json` is machine-parsed; non-zero exit = gate failure.

## Anti-scope

- [SUPUESTO] Adapter governs runtime behavior only; building the adapter is out of scope (owned by delta + generator).
- No cross-profile brand mixing, no uncomputed estimates, no untagged claims, no whole-cluster reads, no "done" without an artifact. Any = breach, HALT. (Price emission governed by the active profile.)

## Acceptance criteria

- Every claim carries one evidence tag; every estimate computed (decomposition/scripts/sources), never guessed.
- Active profile resolved before first content line; profile brand/currency rules respected (single brand per output).
- Each phase marked complete has its prerequisite artifacts on disk (gate verified), not asserted.
- Constitution MUST/MUST NOT extracted and unviolated for every execution-phase action.

## Antigravity delta

Deltas vs baseline harness. Apply only here; do not port to other runtimes. [EXPLICIT]

- No hooks engine [INFERENCE]: run `bash scripts/session-init.sh` at session start — only when state is needed (resume, multi-task, or `[P]` work); skip for one-shot reads. Idempotent; rerun is safe.
- Skill index `.agent/skills_index.json` (generated, minimal fields) [CONFIG]: do not hand-edit — regenerate. MCP config: `~/.gemini/config/mcp_config.json` [CONFIG].
- No subagent dispatch [INFERENCE]: execute `[P]` tasks sequentially in listed order; no parallel fan-out, no nested agents.
- Done = init ran (if required), `[P]` tasks all sequential, no hook/subagent assumptions leaked [ASSUMPTION]. If a step needs a missing engine, stop and flag — never silently emulate. [EXPLICIT]

## Active profile

This harness runs under the **metodologia** profile — its deliverable-quality, brand, i18n, and commercial standards apply. Load `profiles/metodologia.md` on demand; override with the `JMADK_PROFILE` env var. [CONFIG]

Skill index: `.agent/skills_index.json` (generated, minimal fields).
