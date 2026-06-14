# Body of Knowledge — ai-architecture

Domain knowledge for routing and executing AI/LLM system architecture work.
Evidence taxonomy throughout: Alfa core
`[DOC]` `[CONFIG]` `[CÓDIGO]` `[INFERENCIA]` `[SUPUESTO]`. [CONFIG]

## 1. The router contract (core concept)
ai-architecture is a **dispatch table**, not a solver. Its job is intent →
exactly one `topic` → exactly one playbook. Quality is owned by the playbook;
the router owns *correct selection* and *gate enforcement*. Loading more than one
playbook is the cardinal failure: it dilutes context and produces averaged,
ungrounded answers. [DOC]

## 2. Topic boundaries (anti-scope is the skill)
Each topic owns a slice; overlaps are resolved by **ownership**, not preference:
- Retrieval orchestration + answer quality → **rag-patterns**.
- Embedding model / dimension / metric / index → **embedding-strategy** (rag-patterns
  defers these). [DOC]
- LLM instruction design / guardrails → **prompt-engineering**.
- Machine-parseable JSON/enum output → **structured-output**.
- Data-flow infra (dev/prod pipelines, registry, CI/CD) → **ai-pipeline-architecture**.
- Internal code structure / 6-layer stack → **ai-software-architecture**.
- Reusable structural solutions (Feature Store, Champion-Challenger) → **ai-design-patterns**.
- "What does the system do, for whom" → **ai-conops** (precedes architecture).
- Assess an existing system → **audit**. Build it → **implementation**. [DOC]

## 3. Decision rules (cross-topic)
- **Do you even need RAG?** Small/fixed corpus → stuff context. Stable facts →
  fine-tune/system prompt. RAG earns cost only when the corpus is large, changing,
  or must be cited. [INFERENCIA]
- **Retrieval mode** — dense default; add BM25 for exact terms/IDs/code; hybrid
  (RRF fusion) when queries mix both. Pure-dense silently misses literals. [DOC]
- **Embedding metric** must match the model's training (cosine for normalized text). [DOC]
- **Structured-output enforcement tier** — native constrained/tool-call schema >
  JSON mode > prompt-only. Use the strongest the provider supports; validate in code. [CÓDIGO]
- **CONOPS before architecture** — autonomy level and operational modes constrain
  every downstream design choice. [DOC]
- **The pipeline is the architecture** — most production effort is data infra, not
  the algorithm. [INFERENCIA]

## 4. Standards and references
- **IEEE 1362-2022** — Concept of Operations (CONOPS) document standard. [DOC]
- **Avila & Ahmad (2025)** — AI CONOPS stakeholder/autonomy framing. [DOC]
- **6-layer AI architecture stack** — data → feature → model → serving →
  application → governance layering for AI-software-architecture. [DOC]
- **RRF (Reciprocal Rank Fusion)** — combine dense + sparse rankings in hybrid RAG. [DOC]
- **Matryoshka / MRL** — one embedding model serving multiple truncated dimensions. [DOC]
- **Constitution v6.0.0** — enforcement, evidence tags, script-first rule. [CONFIG]

## 5. Validation discipline
- Never ship retrieval/prompt/structured changes "on vibes" — re-run the playbook's
  eval gate on any change to chunking, retrieval mode, rerank, k, prompt, or schema. [DOC]
- Grounding: answer only from retrieved context, else abstain — no fabrication. [DOC]
- Deterministic checks run offline (no network/wall-clock/random). [CÓDIGO]

## 6. Evidence-tag rules
Use ONE family. Alfa core here. Downgrade `[CÓDIGO]`/`[CONFIG]` you cannot point
to in-repo to `[SUPUESTO]`. Never mix `[EXPLICIT]`/`[INFERENCE]` (playbook-internal
distillation tags) into router-level output. [CONFIG]
