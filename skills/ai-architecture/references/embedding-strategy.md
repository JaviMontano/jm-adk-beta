<!-- distilled from alfa skills/embedding-strategy -->
# Embedding Strategy
> "Method over hacks."
## TL;DR
Select, deploy, and operate text embeddings for semantic search, clustering, dedup, and RAG retrieval. Pick model + dimension + distance metric for the recall/cost/latency budget; chunk deliberately; evaluate before shipping. [EXPLICIT]

## Decision Order (do not skip)
1. **Task** — retrieval vs classification vs clustering vs dedup. Drives metric + eval. [EXPLICIT]
2. **Model** — hosted API (low ops, per-token cost, data leaves boundary) vs self-hosted (fixed GPU cost, full control). Default to hosted for <10M chunks; self-host when data residency or volume dominates. [INFERENCE]
3. **Dimension** — higher = better recall, more storage/latency. Prefer models with Matryoshka/MRL truncation so one model serves 256→1536 dims without re-embedding. [EXPLICIT]
4. **Metric** — cosine for normalized text embeddings (default); dot-product only if vectors are unnormalized and magnitude is meaningful; L2 rarely for text. Must match what the model was trained with. [EXPLICIT]
5. **Index** — exact (flat) under ~100k vectors; HNSW/IVF (ANN) above. ANN trades recall@k for latency — tune, then measure. [INFERENCE]

## Chunking (retrieval quality lives here)
- Target 200–500 tokens/chunk with 10–20% overlap; respect semantic boundaries (headings, paragraphs) over fixed windows. [INFERENCE]
- Embed query and document with the **same** model + same prompt/instruction prefix; asymmetric search needs the model's query vs passage modes. [EXPLICIT]
- Store chunk text + source ID + offsets alongside the vector for citation and re-chunking without re-ingest. [EXPLICIT]

## Decisions & Trade-offs
| Decision | Choose when | Cost of getting it wrong |
|----------|-------------|--------------------------|
| Hosted API | Low volume, fast iteration, no residency limits | Recurring per-token spend; data egress; vendor lock to one vector space |
| Self-hosted | Residency/PII limits, >10M chunks, stable model | GPU ops, eval + upgrade burden |
| Truncate dims (MRL) | Storage/latency bound, recall headroom exists | Silent recall drop if truncated below eval floor |
| Re-rank after ANN | Top-k precision matters (RAG answer quality) | Added latency + 2nd model cost |

## Worked Example
RAG over 2M support docs, p95 < 300ms, English-only. Pick hosted MRL model at 768 dims, cosine, HNSW (efSearch tuned to recall@10 ≥ 0.95). Chunk 400 tok / 15% overlap. Retrieve top-50 → cross-encoder rerank → top-5 to LLM. Re-embed only on model upgrade, gated by the eval below. [INFERENCE]

## Evaluation (gate before ship)
- Build a labeled query→relevant-chunk set (≥50 queries). Measure recall@k and MRR/nDCG; this is the acceptance floor. [EXPLICIT]
- Re-run eval on any model, dimension, chunking, or metric change — never ship an embedding change on vibes. [EXPLICIT]

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs) and a labeled eval set. [EXPLICIT]
- English-language output and corpus unless otherwise specified; multilingual needs a multilingual model + per-language eval. [EXPLICIT]
- Does not replace domain expert judgment for final retrieval-quality acceptance. [EXPLICIT]

## Anti-Scope
- Not LLM prompt design → prompt-engineering.md. Not full pipeline orchestration → rag-patterns.md / ai-pipeline-architecture.md. Not model fine-tuning → fine-tuning-prep.md. [EXPLICIT]

## Failure Modes & Edge Cases
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution; cite the trade-off table |
| Out-of-scope request | Redirect to the skill named in Anti-Scope |
| Query/doc model mismatch | Reject — recall collapses silently; re-embed corpus with the query model |
| Metric ≠ training objective | Force cosine for normalized text models; flag dot/L2 misuse |
| Mixed languages in corpus | Switch to multilingual model; re-run eval per language |
| Model deprecated/upgraded | Re-embed full corpus in a shadow index; cut over only after eval passes |
| Recall regression after dim truncation | Restore dims to last passing eval floor |

## Quality Criteria
- [ ] Evidence tags applied
- [ ] Constitution-compliant (XIII/XIV)
- [ ] Metric matches model training objective
- [ ] Eval recall@k meets the documented floor
- [ ] Query and document embeddings use the same model/mode
- [ ] Actionable output

## Usage
- "/embedding-strategy" — Run the full embedding strategy workflow
- "embedding strategy on this project" — Apply to current context
