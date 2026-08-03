# Harness debt — triage findings (2026-06-12)

Triaged the 71 `validate-skills.py` errors + 1095 warnings after the elevation waves.

## Errors are phantom (not real debt) — do NOT fabricate
- **70/71 — iikit broken links to `../iikit-core/*`** [CODE]. `iikit` is a thin overlay
  over the tessl tile `tessl-labs/intent-integrity-kit`; `iikit-core` (references,
  templates, scripts) is provisioned by **tessl at runtime** under
  `.tessl/tiles/.../skills/iikit-core/`, not vendored in this repo. Creating those files
  locally would duplicate upstream content. Left as-is by design. [DOC]
- **1/71 — `skills/seo-growth/.../indexability-validator.md` `path/`** [CODE]. False
  positive: the validator's link extractor parsed the illustrative prose
  `` `[text](path/)` `` as a link. Not a real link. Left as-is. [DOC]

## Real debt — DoD structure (warnings, non-strict)
- 73 skills missing the 15 DoD `REQUIRED_CORE_FILES` + `assets/` bundle
  (per `scripts/validate-skill-dod.py`). Addressed on `feat/harness-dod-debt` by
  generating real, skill-specific, validator-passing bundles (no generic markers,
  >=8 evals, assets manifest). [DOC]

## Resolved (2026-08-03, PR #5)

- ~~`constitution-must.md` thin L3 slice missing~~ — **RESUELTO.** Created
  `references/ontology/constitution-must.md` (~811t) carrying binding MUST/MUST
  NOT + evidence taxonomy + gates; full constitution (5292t) stays authoritative
  for humans but is not loaded into execution stages (exceeds paper §3.2 L3
  budget). Decision: ADR-0002. [DOC]
- ~~per-stage context budget not enforced (paper only claims 2-8k)~~ — **RESUELTO.**
  `scripts/stage-context-manifest.sh` makes the `CONTEXT.md` `## Inputs` table
  executable: resolves L0-L4 paths, sums the token stack, warns >8000t. Paper
  *claims* 2-8k/stage; harness *enforces* it. All 4 stages <8000t
  (6206 / 3814 / 4246 / 4723). Decision: ADR-0002. [CONFIG]
- ~~ICM routing lived only in `delta-claude.md` (fragile ref for codex/antigravity)~~
  — **RESUELTO (routing)** via PR #5 (first-prompt routing across all 3 runtimes,
  ADR-0001). **Elevation to `core.md` as shared contract** tracked as
  `plan-evolucion.md` §4 P2 (deferred, budget risk). [DOC]
- ~~workspace template incomplete (no output dirs, no `_config/`, no sub-agent
  delegation, no review gates)~~ — **RESUELTO.** Pre-created `output/.gitkeep` in
  all 4 stages, `_config/.gitkeep` (L3 stable-ref home), sub-agent delegation
  section in `workspace/_template/CONTEXT.md` (paper §4.1), review gates at each
  stage handoff. [CONFIG]
