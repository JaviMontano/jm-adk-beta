---
name: docs-writing
version: 1.0.0
description: "Documentation and professional writing router: technical docs, changelogs, diagrams, memos, meeting notes, reports, training, knowledge management. Topics: api-documentation, changelog-writing, developer-onboarding, documentation-standards, documentation-system, internal-memo, knowledge-management, meeting-notes, mermaid-diagramming, reporting-templates, storytelling, technical-writing-patterns, training-material."
params:
  topic:
    enum: [api-documentation, changelog-writing, developer-onboarding, documentation-standards, documentation-system, internal-memo, knowledge-management, meeting-notes, mermaid-diagramming, reporting-templates, storytelling, technical-writing-patterns, training-material]
    required: true
    infer: from user request; ask only if ambiguous
  depth:
    enum: [quick, deep]
    default: quick
routes:
  api-documentation: references/api-documentation.md
  changelog-writing: references/changelog-writing.md
  developer-onboarding: references/developer-onboarding.md
  documentation-standards: references/documentation-standards.md
  documentation-system: references/documentation-system.md
  internal-memo: references/internal-memo.md
  knowledge-management: references/knowledge-management.md
  meeting-notes: references/meeting-notes.md
  mermaid-diagramming: references/mermaid-diagramming.md
  reporting-templates: references/reporting-templates.md
  storytelling: references/storytelling.md
  technical-writing-patterns: references/technical-writing-patterns.md
  training-material: references/training-material.md
---

# docs-writing

Router skill. Resolve `topic` from the request, Read EXACTLY ONE playbook from
`routes:`, then execute it. Never load the whole cluster — one route per run. [CONFIG]

## When to use
Any documentation or professional-writing deliverable: API refs, changelogs,
onboarding guides, doc standards/systems, memos, meeting notes, Mermaid
diagrams, report templates, narrative, writing patterns, training. For ad-hoc
prose with no matching topic, write directly without routing. [INFERENCIA]

## Routing
1. Map the request to one `topic` enum value (see `routes:` / `routes.json`). [CONFIG]
2. Ambiguous between two? Ask one disambiguating question; do not guess. [DOC]
3. Read that single playbook. Mixing playbooks dilutes the spine — anti-pattern. [INFERENCIA]
4. Set `depth`: `quick` → essentials only; `deep` → apply exhaustively with
   verification at each step. Default `quick`. [CONFIG]

## Spine
Discover → Analyze → Execute → Validate. Each route specializes these stages;
none skips Validate. [DOC]

## Inputs / Outputs
- **In:** `topic` (required), `depth` (default `quick`), the source material/request. [CONFIG]
- **Out:** the deliverable the routed playbook defines, fully tagged with the
  Alfa core set: `[CÓDIGO]` `[CONFIG]` `[DOC]` `[INFERENCIA]` `[SUPUESTO]`; one
  family per document. [DOC]

## Quality gates
- Constitution v6.0.0 enforcement; evidence tags on every non-obvious claim;
  script-first rule. [CONFIG]
- No invented prices; never report green-as-success; no client PII; single brand
  per output. [DOC]
- Apply the acceptance rubric in `assets/quality-rubric.json` at Validate. [CONFIG]

## Acceptance (done = all true)
- Exactly one route read and executed; topic matches the request. [INFERENCIA]
- Output completed the full spine through Validate. [DOC]
- Tags consistent (one family, correct spelling); every `[SUPUESTO]` paired with
  a verification step. [DOC]

## Self-correction
Loaded two playbooks, skipped Validate, mixed tag families, or invented a topic
not in the enum → stop, re-route from the request, redo. [INFERENCIA]