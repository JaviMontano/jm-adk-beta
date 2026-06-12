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
