# observability — assets bundle

Machine-readable policies the router and its agents rely on. These are domain
artifacts, not decoration: the guardian and lead read them at decision time.

## Files
- **`routing-matrix.json`** — intent-to-topic map. The lead/router resolves a
  single `topic` against this matrix (by underlying symptom, not keyword overlap)
  and loads EXACTLY ONE playbook. Encodes the ambiguity rule (ask, never guess
  past a `{VACIO_CRITICO}`). Used by `SKILL.md`, `README.md`, `agents/lead.md`.
- **`quality-rubric.json`** — per-topic quality gates plus the global gates the
  guardian applies before emitting `dod=pass`. Names the deterministic validator
  for `alerting-strategy` and `health-check-automation`, the evidence-tag
  vocabulary, and the not-green-as-success rule. Used by `agents/guardian.md` and
  `templates/output.md`.

## Contract
- These JSON policies are source of truth for routing and acceptance. If prose in
  a playbook disagrees with a policy here, the JSON wins — mirroring the
  deterministic playbooks' own `assets/*.json` convention.
- Every `used_by` target listed in `manifest.json` is an existing file in this
  skill.
- No client PII, no invented prices, single-brand.
