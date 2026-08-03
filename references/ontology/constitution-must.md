# Constitution v7.0.0 — MUST/MUST NOT slice (Layer 3 reference)

> **Derived** from `constitution-v7.0.0.md` (authoritative). Thin L3 slice for
> execution stages (03_build, 04_validate) — the full doc (5292t) exceeds the
> paper's per-stage L3 budget (500-2k tok, arXiv 2603.16021v2 §3.2). This slice
> carries only the binding rules + evidence taxonomy + gates. For rationale,
> personas, or cross-reference tables, read the full constitution. [DOC]

## Evidence taxonomy `[DOC]`

`[CODE]` (read in source) · `[CONFIG]` (read in config/manifest) · `[DOC]` (read in a spec/doc) · `[INFERENCE]` (derived from evidence, not stated) · `[ASSUMPTION]` (unverified, must be confirmed). **Untagged technical claims fail G1.**

## Phase separation (P1) — non-negotiable

Constitution (WHY) → Spec (WHAT) → Plan (HOW) → Tasks (WORK) → Tests/Checks (PROOF) → Deliverable (SOLUTION). Phase artifacts exist in order. Assumption ratio ≤30% or mandatory clarification triggers.

## MUST / MUST NOT (binding)

- **MUST**: complexity beyond the simplest alternative MUST document why the simpler approach was insufficient (P2).
- **MUST NOT**: assertions MUST NOT be modified to pass — fix the code instead (P3). A flaky test is quarantined + ticketed, never deleted, never "fixed" by weakening its assertion.
- **MUST**: tests written BEFORE production code; red → green → refactor (P3).
- **MUST**: every directory navigable by reading only index files; every directory has README.md (P7).
- **MUST**: estimates COMPUTED — (a) explicit decomposition, (b) deterministic scripts, (c) cited sources. NEVER from token-count, gut, or vibes (P8). Effort units + confidence + assumptions tagged.
- **MUST NOT**: no secrets in client-side or shipped code (P10).
- **MUST**: input sanitized at the boundary (strip dangerous markup, not escape); authorization enforced at data layer, never trust the client (P10).
- **MUST**: sequential-first execution (P5). Parallel ONLY when plan tags `[PARALLEL-OK]` with zero pre/co-dependencies + zero shared mutable state; WIP ≤3 agents.
- **MUST**: every new working session follows Session Protocol (context load → workspace detect → state recover → execute → close).

## Quality gates (blocking, ordered, never waived)

| Gate | When | Exit criteria | On failure |
|------|------|---------------|------------|
| **G0** | Pre-flight | Secrets clean; feature branch (never default); Constitution loaded; active profile resolved | Abort |
| **G1** | After spec | Spec complete (FR/SC/G-W-T); claims tagged; `[ASSUMPTION]` ≤30%; estimates computed | Return to Think |
| **G2** | After plan | Data model + contracts defined; security rules drafted; BDD hash-locked; profile standards referenced | Re-plan |
| **G3** | Deliverable-ready | All tests green; security/runtime pass; active profile acceptance met | Block; fix + re-run |

## Governance precedence (highest wins)

Security (10) + Deliverable-Quality of active profile (9) > Foundation (1,2) > Test discipline (3,4) > Estimation Integrity (8) + remaining > convenience/speed. A lower tier never overrides a higher one. **Escalation**: missing input, conflicting instruction, or unpassable gate → STOP, surface blocker with principle cited, do NOT proceed on `[ASSUMPTION]`.