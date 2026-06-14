# Example output — ai-architecture routing (for the example-input ask)

## 1. Request summary
- **Ask:** Grounded, cited assistant over ~2M support/policy docs; p95 < 800ms;
  weekly-updated corpus. [DOC]
- **AI-system shaped?** Yes — retrieval + grounded generation. [INFERENCIA]

## 2. Routing decision
| Field | Value |
|-------|-------|
| Resolved `topic` | `rag-patterns` |
| `depth` | deep |
| Playbook Read | `references/rag-patterns.md` (only) |
| Tie-break applied | Ownership: embedding model/dimension/metric belongs to embedding-strategy and is NOT being asked; this is retrieval orchestration + grounding → rag-patterns |

Routing rationale: intent is "ground answers in our docs and cite", which is the
rag-patterns charter. [INFERENCIA]

## 3. Playbook artifact (rag-patterns, deep)
- **Need-RAG check:** corpus is large, changing weekly, and must be cited → RAG is
  justified over context-stuffing or fine-tuning. [INFERENCIA]
- **Retrieval mode:** hybrid — dense (semantic) + BM25 (exact policy IDs / clause
  numbers), fused with RRF. Pure-dense would miss literal IDs. [DOC]
- **Granularity:** small-to-big — retrieve precise child chunks, generate on parent
  windows. [INFERENCIA]
- **Pipeline:** hybrid retrieve top-50 → metadata filter (product + freshness ≤ 1
  week) → cross-encoder rerank → top-5 parent windows → LLM with "answer only from
  context; cite chunk IDs; else say you don't know." Log retrieved IDs for eval +
  audit. [DOC]
- **Latency:** rerank top-50→top-5 fits p95 < 800ms with a cached embedding index
  (HNSW); verify under load. [SUPUESTO]

## 4. Validation gate result
- [x] Exactly one `topic` (`rag-patterns`), in enum. [DOC]
- [x] Exactly one playbook Read. [DOC]
- [x] One tag family (Alfa core). [CONFIG]
- [x] Playbook gate named: retrieval eval (recall@k, MRR/nDCG on ≥50 labeled
      queries) + answer eval (faithfulness, citation correctness). [DOC]
- [x] `depth=deep` honored — full decision order + eval gate applied. [INFERENCIA]

## 5. Evidence tags
Alfa core only: `[DOC]` `[CONFIG]` `[CÓDIGO]` `[INFERENCIA]` `[SUPUESTO]`. [CONFIG]

## 6. Governance check
- [x] No invented prices. [SUPUESTO]
- [x] No client PII (no real document contents shown). [SUPUESTO]
- [x] Single brand. [SUPUESTO]

## 7. Open assumptions / gaps
- Labeled retrieval eval set (≥50 query→relevant-chunk pairs) must be built before
  ship; freshness SLA of 1 week assumed pending stakeholder confirmation. [SUPUESTO]
