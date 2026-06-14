# ai-architecture — skill overview

A **router skill** for AI/LLM system architecture. It resolves a single `topic`
from the request, then Reads EXACTLY ONE playbook from `references/` and lets
that playbook do the work. This skill never improvises an answer inline. [DOC]

## What it does
Covers the full lifecycle of designing, auditing, and implementing AI/LLM
system components: concept of operations, design patterns, pipelines, software
architecture, audits, retrieval (RAG), prompts, embeddings, fine-tuning prep,
structured output, and chatbot/voice interfaces. [DOC]

## When to use
Use when a request is **LLM/AI-system shaped** — e.g. "design a RAG pipeline over
our docs", "make this prompt reliable", "audit our model-serving architecture",
"pick an embedding model and dimension". If the request is not AI-system shaped,
do not route here. [INFERENCIA]

## How it routes and executes
1. Resolve the single best `topic` from the `enum` (map **intent**, not keywords).
   Ask only if two enum values fit equally; stop if none fit. [SUPUESTO]
2. Read that topic's `references/<topic>.md` playbook — and nothing else from the
   cluster. Bulk-loading defeats the router. [DOC]
3. `depth=quick` → essentials only; `depth=deep` → apply the playbook
   exhaustively, verifying each step. Playbook gates override these defaults. [INFERENCIA]
4. Emit the playbook's artifact with **one** evidence-tag family
   (Alfa core: `[DOC]` `[CONFIG]` `[CÓDIGO]` `[INFERENCIA]` `[SUPUESTO]`). [CONFIG]

Spine: **Discover → Analyze → Execute → Validate**.

## Routes (topics → playbooks)
| Topic | Playbook | Owns |
|-------|----------|------|
| `ai-conops` | `references/ai-conops.md` | Operational concept (IEEE 1362-2022), stakeholders, autonomy, modes |
| `ai-design-patterns` | `references/ai-design-patterns.md` | Feature Store, Champion-Challenger, Shadow Deploy, Drift Detection, anti-patterns |
| `ai-pipeline-architecture` | `references/ai-pipeline-architecture.md` | Dev/prod pipelines, data stores, model registry, CI/CD |
| `ai-software-architecture` | `references/ai-software-architecture.md` | 6-layer AI stack, module boundaries, serving/feature-store structure |
| `audit` | `references/audit.md` | Gap assessment, severity-ranked findings, remediation roadmap |
| `chatbot-design` | `references/chatbot-design.md` | Conversational flow, turn-taking, fallback, escalation |
| `embedding-strategy` | `references/embedding-strategy.md` | Model/dimension/metric/index selection |
| `fine-tuning-prep` | `references/fine-tuning-prep.md` | When-to-tune decision, dataset readiness, eval gating |
| `implementation` | `references/implementation.md` | Turning architecture into shippable code/config |
| `prompt-engineering` | `references/prompt-engineering.md` | Instruction packages, guardrails, adversarial tests, eval packet |
| `rag-patterns` | `references/rag-patterns.md` | Ingest→retrieve→rerank→ground→cite→eval orchestration |
| `structured-output` | `references/structured-output.md` | Schema-valid JSON/enums, enforcement tiers, validation+recovery |
| `voice-interface` | `references/voice-interface.md` | ASR→NLU→dialog→TTS, latency/barge-in budgets |

## Bundle
- `references/` — the 13 playbooks (one is Read per invocation).
- `agents/` — lead, specialist, support, guardian role contracts.
- `knowledge/` — body of knowledge + knowledge graph.
- `prompts/` — primary, meta, and quick/deep variations.
- `templates/output.md` — routing-decision deliverable scaffold.
- `evals/evals.json` — routing + DoD eval cases.
- `examples/` — a worked routing example.
- `assets/` — deterministic routing aids (rubric + checklist) used by SKILL.md.

## Anti-patterns
Loading several playbooks "to compare"; answering inline without routing; asking
for `topic` when it is obvious; mixing tag families. [INFERENCIA]
