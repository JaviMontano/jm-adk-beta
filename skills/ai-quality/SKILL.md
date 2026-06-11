---
name: ai-quality
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

Router skill. Resolve `topic` from the request, then Read EXACTLY ONE playbook
from `routes:`. Never load the whole cluster. `depth=deep` → apply the playbook
exhaustively with verification at each step; `quick` → essentials only.

Spine: Discover → Analyze → Execute → Validate.
Quality gates: constitution v6.0.0 (enforcement), evidence tags, script-first rule.
