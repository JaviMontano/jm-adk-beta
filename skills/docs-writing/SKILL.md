---
name: docs-writing
description: "Documentation and professional writing: technical docs, changelogs, diagrams, memos, meeting notes, reports, training, and knowledge management. Topics: api-documentation, changelog-writing, developer-onboarding, documentation-standards, documentation-system, internal-memo, knowledge-management, meeting-notes, mermaid-diagramming, reporting-templates, storytelling, technical-writing-patterns, training-material."
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

Router skill. Resolve `topic` from the request, then Read EXACTLY ONE playbook
from `routes:`. Never load the whole cluster. `depth=deep` → apply the playbook
exhaustively with verification at each step; `quick` → essentials only.

Spine: Discover → Analyze → Execute → Validate.
Quality gates: constitution v6.0.0 (enforcement), evidence tags, script-first rule.
