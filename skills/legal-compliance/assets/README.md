# Assets — legal-compliance

Reusable, machine-checkable artifacts that back the skill's validation gate and
routing discipline. Each asset is registered in `manifest.json` with the file(s)
that consume it.

## Contents

- **`quality-rubric.json`** — the binary, per-lane quality criteria distilled from
  the three playbooks (shared gate + compliance-assessment + compliance-framework +
  contract-review). The guardian agent (`agents/guardian.md`) and `SKILL.md`'s
  validation gate check against it. Partial credit is a fail.
- **`routing-checklist.md`** — the pre-flight checklist the lead agent runs to
  resolve `topic`/`depth` and confirm single-playbook discipline before execution.

## Usage

These assets are referenced, not edited per-run. Update them only when a playbook's
scoring method, evidence taxonomy, or scope boundary changes — keep them in lockstep
with `references/*.md`.
