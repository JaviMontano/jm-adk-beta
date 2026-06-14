# Assets Bundle — Runtime Routing

This bundle holds the **deterministic, machine-checkable contract** behind the
routing decision plus the scored quality rubric. The tables in `SKILL.md` are the
human-readable shortcut; these files are the source of truth. [DOC]

If a policy file is absent at runtime, honor its rule as a *requirement to meet* —
do not treat its absence as evidence that the rule is satisfied. [SUPUESTO]

## Files

| File | Type | Purpose | Used by |
|---|---|---|---|
| `manifest.json` | manifest | Declares every asset, its type, purpose, and consumer | validator |
| `quality-rubric.json` | rubric | Scored quality criteria the deliverable must meet (evidence grounding, lowest-permission, fallback, secret boundary) | `SKILL.md`, `templates/output.md` |
| `runtime-catalog-policy.json` | policy | Allowed runtime ids + their permission levels (the lowest-permission ranking) | `SKILL.md` |
| `evidence-policy.json` | policy | What may ground a capability claim (repo file / executed check / runtime metadata / user config) | `SKILL.md` |
| `capability-matrix-policy.json` | policy | The supported / pending / unsupported axes and promotion rule | `SKILL.md` |
| `fallback-policy.json` | policy | Requires a local-first fallback with visible limits + no-auth path | `SKILL.md` |
| `runtime-routing-contract.json` | schema | Shape of a valid route decision report | `SKILL.md` |

## Rule of use

- A capability is `supported` only when `evidence-policy.json` recognizes its
  evidence id; otherwise it is `validation pending`. [DOC]
- The recommended runtime must exist in `runtime-catalog-policy.json` and sit at
  the lowest permission level among evidence-backed survivors. [CONFIG]
- `fallback-policy.json` makes the local-first fallback non-optional. [DOC]
