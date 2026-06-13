# seo-growth — Assets Bundle

Deterministic, machine-readable assets that back the router's decisions and gates. These
are the source of truth the agents reference instead of re-deriving rules ad hoc.

## Contents

| Asset | Type | Used by | Purpose |
|---|---|---|---|
| `quality-rubric.json` | JSON | `SKILL.md`, `agents/guardian.md`, `templates/output.md` | Routing gates, governance gates, and per-topic acceptance checks. The guardian emits `pass` only when every applicable check holds. |
| `routing-matrix.json` | JSON | `agents/lead.md`, `prompts/meta.md`, `README.md` | Signal-to-enum disambiguation, `not_this_if` rules, tie-break, and the out-of-scope list. The lead uses it to resolve exactly one topic. |
| `manifest.json` | JSON | (index) | Lists every asset with type, purpose, and `used_by` targets. |

## How they fit the flow

1. **Lead** resolves the topic with `routing-matrix.json` — signals in, one enum out; on a
   tie it asks one question rather than reading two playbooks.
2. **Specialist/Support** produce the artifact per the resolved playbook.
3. **Guardian** scores the artifact against `quality-rubric.json` (routing + governance +
   that topic's acceptance list) and returns `pass` or a blocking finding.

## Conventions

- All assets are valid JSON, version-pinned where applicable.
- Evidence taxonomy is the Alfa core set: `EXPLICIT`, `DOC`, `INFERENCE`, `SUPUESTO`.
- No prices, no client PII; single brand voice — consistent with the skill's governance.
