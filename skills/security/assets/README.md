# Assets — security

Deterministic, machine- and human-readable assets that back the `security`
skill's quality gates. These encode *what good looks like* so the guardian and
the meta self-check evaluate every deliverable the same way every run. [DOC]

## Bundle

| Asset | Type | Purpose | Used by |
|-------|------|---------|---------|
| `quality-rubric.json` | JSON rubric | The seven gate criteria (single-route, evidence tags, severity-by-context, determinism, remediation pairing, no-green-as-success, read-only) with weights and fail conditions. | `SKILL.md`, `agents/guardian.md`, `templates/output.md` |
| `checklist.md` | Markdown checklist | Deterministic pre-ship checklist the guardian walks per route. | `agents/guardian.md`, `prompts/meta.md` |

## Precedence
When this bundle and prose disagree, the asset is authoritative for gating — it
is the contract the deliverable is scored against. Fix the prose, not the asset,
to resolve a conflict. [EXPLICIT]

## Governance
A passing rubric/checklist confirms the deliverable is *structurally* conformant;
it never means the target is safe. Never report insecure output as passing. [EXPLICIT]

The manifest is `manifest.json`; every `used_by` target listed there exists in
this skill.
