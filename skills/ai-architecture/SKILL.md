---
name: ai-architecture
version: 1.0.0
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

Router skill: resolve `topic` from the request, then Read EXACTLY ONE playbook
from `routes:`. The playbook does the work; this file only routes. [DOC]

## When to use
User asks to design, audit, or implement an AI/LLM system component — software
architecture, pipelines, ConOps, design patterns, RAG, prompts, embeddings,
fine-tuning prep, structured output, chatbot/voice interface. If the request
is not LLM/AI-system shaped, do not route here. [INFERENCIA]

## Inputs → Outputs
- **In:** `topic` (one enum value, required), `depth` (`quick`|`deep`, default `quick`).
- **Resolve `topic`:** infer from the request; ask ONLY if two enum values fit
  equally. Map intent, not keywords (e.g. "make my prompt reliable" →
  `prompt-engineering`; "ground answers in our docs" → `rag-patterns`). [INFERENCIA]
- **Out:** the artifact the chosen playbook defines, with evidence tags and any
  validation gate that playbook specifies — never an answer improvised here. [DOC]

## Routing procedure
1. Pick the single best `topic`; if none fits, say so and stop — do not force-fit. [SUPUESTO]
2. Read its `routes:` playbook. Read NOTHING else from the cluster. [DOC]
3. `quick` → essentials only; `deep` → apply the playbook exhaustively, verifying
   at each step. Honor the playbook's own gates over these defaults. [INFERENCIA]

Spine: Discover → Analyze → Execute → Validate.
Quality gates: constitution v6.0.0 (enforcement), evidence tags, script-first rule. [CONFIG]
Deterministic routing aids: `assets/` (routing-rubric.json, routing-checklist.md). [CONFIG]

## Validation gate (before handing off)
- Exactly one `topic` resolved and present in the enum. [DOC]
- Exactly one playbook Read; cluster not bulk-loaded. [DOC]
- Output carries evidence tags from ONE family (Alfa core here:
  `[DOC]` `[CONFIG]` `[CÓDIGO]` `[INFERENCIA]` `[SUPUESTO]`). [CONFIG]

## Anti-patterns
- Loading several playbooks "to compare" — defeats the router; pick one. [INFERENCIA]
- Answering AI-architecture questions inline without routing. [INFERENCIA]
- Asking for `topic` when the request already makes it obvious. [SUPUESTO]
- Mixing tag families, or emitting `[CÓDIGO]`/`[CONFIG]` you cannot point to in-repo — downgrade to `[SUPUESTO]`. [CONFIG]

## Self-correction
If the playbook doesn't fit the ask, stop, re-resolve `topic`, Read the correct
one — never patch with a second. If no enum fits, report the gap. [SUPUESTO]