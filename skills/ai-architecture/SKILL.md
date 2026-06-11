---
name: ai-architecture
description: "AI/LLM system architecture: software arch, pipelines, conops, design patterns, audit, implementation. Topics: ai-conops, ai-design-patterns, ai-pipeline-architecture, ai-software-architecture, audit, chatbot-design, embedding-strategy, fine-tuning-prep, implementation, prompt-engineering, rag-patterns, structured-output, voice-interface."
params:
  topic:
    enum: [ai-conops, ai-design-patterns, ai-pipeline-architecture, ai-software-architecture, audit, chatbot-design, embedding-strategy, fine-tuning-prep, implementation, prompt-engineering, rag-patterns, structured-output, voice-interface]
    required: true
    infer: from user request; ask only if ambiguous
  depth:
    enum: [quick, deep]
    default: quick
routes:
  ai-conops: references/ai-conops.md
  ai-design-patterns: references/ai-design-patterns.md
  ai-pipeline-architecture: references/ai-pipeline-architecture.md
  ai-software-architecture: references/ai-software-architecture.md
  audit: references/audit.md
  chatbot-design: references/chatbot-design.md
  embedding-strategy: references/embedding-strategy.md
  fine-tuning-prep: references/fine-tuning-prep.md
  implementation: references/implementation.md
  prompt-engineering: references/prompt-engineering.md
  rag-patterns: references/rag-patterns.md
  structured-output: references/structured-output.md
  voice-interface: references/voice-interface.md
---

# ai-architecture

Router skill. Resolve `topic` from the request, then Read EXACTLY ONE playbook
from `routes:`. Never load the whole cluster. `depth=deep` → apply the playbook
exhaustively with verification at each step; `quick` → essentials only.

Spine: Discover → Analyze → Execute → Validate.
Quality gates: constitution v6.0.0 (enforcement), evidence tags, script-first rule.
