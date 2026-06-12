# Assets bundle — skill-foundry

Deterministic, offline assets the foundry uses while resolving and validating a
routing decision. No network, clock, or model calls. [DOC]

| Asset | Purpose | Used by |
|-------|---------|---------|
| `quality-rubric.json` | Seven-dimension scorecard for grading a routing decision (topic resolution, single-load, tie-break discipline, depth fidelity, playbook gate, evidence tags, governance). | `SKILL.md`, `agents/guardian.md` |
| `checklist.md` | Discover → Analyze → Execute → Validate checklist run before declaring a route done. | `templates/output.md` |

## How they fit

The Guardian agent scores the routing artifact against `quality-rubric.json`; a
decision ships only when topic resolution, single-load, and the playbook gate all
score 2 and every other dimension is at least 1. The `checklist.md` mirrors the
foundry spine and is the manual companion to `templates/output.md`. [DOC]

The manifest (`manifest.json`) lists every asset with its `used_by` targets; each
target file exists in this skill. [DOC]
