<!-- distilled from alfa skills/rag-patterns -->
<!-- > -->
# Rag Patterns
> "Method over hacks."
## TL;DR
Architect the retrieval-augmented generation pipeline end to end: ingest → chunk → embed → index → retrieve → rerank → assemble context → generate → cite → evaluate. Owns orchestration and answer quality; embedding model/dimension/metric choices live in embedding-strategy.md. [EXPLICIT]

## Decision Order (do not skip)
1. **Do you even need RAG?** Fixed/small corpus that fits context → just stuff it. Stable facts → fine-tune/system prompt. RAG earns its cost only when the corpus is large, changing, or must be cited. [INFERENCE]
2. **Retrieval mode** — dense (semantic) default; add BM25/keyword for exact terms, IDs, code, rare tokens; hybrid (fuse both) when queries mix both. Pure-dense silently misses literal matches. [EXPLICIT]
3. **Granularity** — retrieve small (precise chunk) but generate on larger parent/window for context. Small-to-big beats one fixed size. [INFERENCE]
4. **Rerank** — cross-encoder rerank of top-50→top-5 when answer precision matters; skip only if recall@5 already meets the eval floor. [EXPLICIT]
5. **Context assembly** — order by relevance, dedup near-identical chunks, fit the token budget, and always carry source IDs for citation. [EXPLICIT]

## Procedure
### Step 1: Discover
- Capture corpus size/volatility, query types, latency/cost budget, citation + freshness requirements. [EXPLICIT]
### Step 2: Analyze
- Evaluate retrieval mode, chunking, rerank, and grounding per Constitution XIII/XIV against the budget. [EXPLICIT]
### Step 3: Execute
- Implement the pipeline with evidence tags; enforce grounding (answer only from retrieved context, else abstain). [EXPLICIT]
### Step 4: Validate
- Run the retrieval + answer eval gate below before shipping any change. [EXPLICIT]

## Decisions & Trade-offs
| Decision | Choose when | Cost of getting it wrong |
|----------|-------------|--------------------------|
| Hybrid (dense+BM25) | Queries mix semantics and exact terms/IDs | Dense-only misses literals; sparse-only misses paraphrase |
| Cross-encoder rerank | Top-k precision drives answer quality | Wrong/irrelevant chunks → confident wrong answers; rerank adds latency + cost |
| Small-to-big chunks | Need precise hit + enough context to answer | Too-small: no context; too-big: diluted retrieval, wasted tokens |
| Strict grounding/abstain | Hallucination is unacceptable (legal, support) | Lenient: model invents; too-strict: over-refusal on answerable queries |
| Metadata filter pre-retrieval | Tenant/date/ACL scoping required | Cross-tenant or stale leakage; security incident |

## Worked Example
Ground answers over 2M support docs, p95 < 800ms, must cite. Hybrid retrieve top-50 (dense 768-dim cosine + BM25, RRF fusion) → metadata filter by product+locale → cross-encoder rerank → top-5 parent windows → LLM with "answer only from context, cite chunk IDs, else say you don't know." Log retrieved IDs for eval + audit. [INFERENCE]

## Evaluation (gate before ship)
- **Retrieval:** labeled query→relevant-chunk set (≥50 queries); measure recall@k, MRR/nDCG — the acceptance floor. [EXPLICIT]
- **Answer:** faithfulness/groundedness (answer entailed by context), answer relevance, and citation correctness on a held-out set. [EXPLICIT]
- Re-run on any change to chunking, retrieval mode, rerank, k, or prompt — never ship on vibes. [EXPLICIT]

## Quality Criteria
- [ ] Evidence tags applied
- [ ] Constitution-compliant
- [ ] Grounding enforced (cite-or-abstain), no answer beyond retrieved context [EXPLICIT]
- [ ] Retrieval + answer eval gate passed [EXPLICIT]

## Usage

Example invocations:

- "/rag-patterns" — Run the full rag patterns workflow
- "rag patterns on this project" — Apply to current context
- "ground answers in our docs" — Design the retrieval + grounding pipeline [EXPLICIT]

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) and a labeled eval set. [EXPLICIT]
- Requires English-language output and corpus unless otherwise specified; multilingual needs multilingual embeddings + per-language eval. [INFERENCE]
- Does not replace domain expert judgment for retrieval-quality or grounding acceptance. [EXPLICIT]

## Anti-Scope
- Embedding model/dimension/metric selection → embedding-strategy.md. LLM prompt design → prompt-engineering.md. Pipeline orchestration/infra → ai-pipeline-architecture.md. Fine-tuning → fine-tuning-prep.md. [EXPLICIT]

## Failure Modes & Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Retrieval returns nothing relevant | Abstain ("not in sources"); never fabricate; log query for corpus gap [EXPLICIT] |
| Top chunks contradict each other | Surface conflict + cite both; don't silently pick one [INFERENCE] |
| Stale or out-of-date corpus | Filter by freshness; flag if best chunk is past freshness SLA [INFERENCE] |
| Multi-tenant / ACL corpus | Filter by tenant/permission BEFORE retrieval, never post-hoc [EXPLICIT] |
