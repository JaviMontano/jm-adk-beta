---
name: ai-quality
version: 1.0.0
description: "AI quality: testing strategy, assisted testing, code review, safety, content detection, docs, workflow automation. Topics: ai-assisted-testing, ai-code-review, ai-content-detection, ai-documentation, ai-safety, ai-testing-strategy, ai-workflow-automation, code-review, llm-evaluation."
params:
  topic:
    enum: [ai-assisted-testing, ai-code-review, ai-content-detection, ai-documentation, ai-safety, ai-testing-strategy, ai-workflow-automation, code-review, llm-evaluation]
    required: true
    infer: from user request; ask only if ambiguous
  depth:
    enum: [quick, deep]
    default: quick
routes:
  ai-assisted-testing: references/ai-assisted-testing.md
  ai-code-review: references/ai-code-review.md
  ai-content-detection: references/ai-content-detection.md
  ai-documentation: references/ai-documentation.md
  ai-safety: references/ai-safety.md
  ai-testing-strategy: references/ai-testing-strategy.md
  ai-workflow-automation: references/ai-workflow-automation.md
  code-review: references/code-review.md
  llm-evaluation: references/llm-evaluation.md
---

# ai-quality

Router for AI/code quality work. Resolve ONE `topic`, Read ONLY its playbook
from `routes:`, then execute. [DOC]

## When to use
Any request to assess, test, review, evaluate, or harden code or AI output:
test plans, AI-assisted/LLM-judge evaluation, human or AI code review, model
safety, AI-vs-human content detection, quality docs, or QA automation. [DOC]
Not for: building features, prompt authoring, deployment — route elsewhere.

## Inputs / Outputs
- **In:** `topic` (required; infer from intent, ask only if two routes tie),
  `depth` (`quick`=essentials, `deep`=exhaustive with verification per step),
  plus the artifact under review (code, model output, spec, pipeline). [CONFIG]
- **Out:** the playbook's deliverable, every non-obvious claim carrying one
  Alfa-set tag (`[CÓDIGO]` `[CONFIG]` `[DOC]` `[INFERENCIA]` `[SUPUESTO]`). [DOC]

## Routing
1. Map intent → exactly one `topic` (enums are fixed; never invent one). [CÓDIGO]
2. Disambiguate near-collisions: AI judges/scores output → `llm-evaluation`;
   AI writes/runs tests → `ai-assisted-testing`; AI reviews a diff →
   `ai-code-review`; human/tool review of a diff → `code-review`. [INFERENCIA]
3. Read that single playbook. Never preload the cluster — token waste and
   cross-topic bleed are the failure modes. [INFERENCIA]
4. Apply the spine: Discover → Analyze → Execute → Validate. [DOC]

Routing/gate contracts live in `assets/` (`routing-matrix.json`,
`quality-rubric.json`); see `assets/README.md`. [CONFIG]

## Validation gate (before "done")
- [ ] Resolved topic ∈ enum; exactly one playbook Read. [CÓDIGO]
- [ ] Quality gates honored: constitution v6.0.0, evidence tags, script-first. [CONFIG]
- [ ] One tag family throughout (Alfa set here); no `[CÓDIGO]` without an
      in-repo referent — else downgrade to `[SUPUESTO]`. [DOC]
- [ ] `deep` ran verification at each step; `quick` stayed at essentials.

## Anti-patterns & self-correction
Avoid: loading >1 route; answering from this router without a playbook;
guessing an ambiguous `topic`; untagged prose; mixed tag families. [SUPUESTO]
On any of these → stop, re-resolve `topic` via the disambiguation rules,
re-read the one playbook. [INFERENCIA]