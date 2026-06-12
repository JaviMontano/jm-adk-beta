# docs-writing

Router skill for documentation and professional-writing deliverables. It resolves a
single `topic`, reads exactly one playbook from `routes:`, and executes that
playbook's Discover → Analyze → Execute → Validate spine. [CONFIG]

## What it does

`docs-writing` turns source material (code, PRs, prior docs, meeting transcripts,
release diffs) into a finished writing artifact — an API reference, a changelog, an
onboarding guide, a doc standard, a doc-as-code system decision, an executive memo,
meeting notes, a Mermaid diagram, a report, a narrative, or training material. It is a
dispatcher: it never blends playbooks, because mixing dilutes the spine. [INFERENCIA]

## When to use it

- You have a documentation or professional-writing deliverable to produce and one of
  the 13 topics matches the request. [CONFIG]
- You want the deliverable governed: evidence-tagged, single-brand, no invented prices,
  validated before "done". [DOC]

Do NOT use it for ad-hoc prose that matches no topic — write directly. Do not use it to
design API contracts (`api-design`), implement endpoints, or run CI/publish pipelines;
those are owned elsewhere and only documented here once decided. [INFERENCIA]

## How it routes and executes

1. Map the request to one `topic` enum value (the 13 routes in `routes.json`). [CONFIG]
2. If ambiguous between two topics, ask one disambiguating question — never guess. [DOC]
3. Read that single playbook from `references/`. One route per run. [CONFIG]
4. Set `depth`: `quick` (essentials) or `deep` (exhaustive, verify each step). [CONFIG]
5. Run the playbook's spine; never skip Validate. [DOC]

## Topics and routes

| Topic | Playbook | Owns |
|-------|----------|------|
| api-documentation | `references/api-documentation.md` | OpenAPI specs, endpoint reference, error catalog |
| changelog-writing | `references/changelog-writing.md` | Keep-a-Changelog entries, migration notes |
| developer-onboarding | `references/developer-onboarding.md` | Sequenced ramp checklist, buddy/mentor, metrics |
| documentation-standards | `references/documentation-standards.md` | Templates, SemVer-for-docs, review/archival |
| documentation-system | `references/documentation-system.md` | Doc-as-code pipeline, CI publishing |
| internal-memo | `references/internal-memo.md` | BLUF decision/status briefs |
| knowledge-management | `references/knowledge-management.md` | Knowledge capture, taxonomy, findability |
| meeting-notes | `references/meeting-notes.md` | Decisions, action items, attendee context |
| mermaid-diagramming | `references/mermaid-diagramming.md` | Mermaid flow/sequence/ER diagrams |
| reporting-templates | `references/reporting-templates.md` | Status/exec report scaffolds |
| storytelling | `references/storytelling.md` | Narrative arc, transformation framing |
| technical-writing-patterns | `references/technical-writing-patterns.md` | Sentence/section-level style |
| training-material | `references/training-material.md` | Lessons, exercises, assessment |

## Evidence taxonomy

Every output carries one tag family — the Alfa core set: `[CÓDIGO]` `[CONFIG]` `[DOC]`
`[INFERENCIA]` `[SUPUESTO]`. Some legacy playbooks use the `[EXPLICIT]`/`[INFERENCE]`
family; pick ONE family per document and never mix. Every `[SUPUESTO]` must be paired
with a verification step. [DOC]

## Bundle contents

- `references/` — the 13 routed playbooks (the spine of execution).
- `agents/` — role contracts: lead, specialist, support, guardian.
- `knowledge/` — body of knowledge + concept graph.
- `prompts/` — primary, meta, and quick/deep variations.
- `templates/output.md` — the deliverable scaffold.
- `evals/evals.json` — scenario test cases and expected checks.
- `examples/` — a worked input/output pair (API reference).
- `assets/` — quality rubric and routing checklist (see `assets/README.md`).
