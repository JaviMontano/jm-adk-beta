# Example Output — lab-session

Worked result for the `rag-cache-ttl` request in `examples/example-input.md`.

## Console summary

```
lab-session: ./labs/rag-cache-ttl/  created=4 skipped=0
```

## Folder written: `./labs/rag-cache-ttl/`

### notas.md
```
# Notas — rag-cache-ttl

## 2026-06-12
- Session opened. Probe: 200ms TTL on the RAG embedding cache. [DOC]
- Open question: what recall delta counts as "measurable"? Define before run. [INFERENCE]

## Open questions
- Which recall metric (Recall@10?) and which eval set? [ASSUMPTION]

## Next probe
- Baseline p95 with cache disabled vs. 200ms TTL. [INFERENCE]
```

### hipotesis.md
```
# Hipotesis — rag-cache-ttl

Claim (falsifiable): A 200ms TTL on the RAG embedding cache will NOT measurably
reduce recall, while cutting p95 retrieval latency by >=30%. [INFERENCE]

Refuted if: recall drops beyond noise OR p95 improvement is <30%. [INFERENCE]
```

### referencias.md
```
# Referencias — rag-cache-ttl

- Q1 retrieval latency baseline (internal doc) [DOC]
- Recall-vs-cache-size sweep, Apr 2026 (internal doc) [DOC]
```

### decision.md
```
# Decision — rag-cache-ttl

Verdict (keep / pivot / kill): {POR_CONFIRMAR}
```

## Why this passes the gate
- Exactly four canonical files; nothing pre-existing was touched (`skipped=0`).
- Hypothesis is falsifiable (explicit refuting condition).
- Every reference entry carries one `[DOC]` tag, one spelling.
- `decision.md` left `{POR_CONFIRMAR}` — verdict deferred to the human.
- Single-brand JM Labs; green not used as a success signal; summary line emitted.
