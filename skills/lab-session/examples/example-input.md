# Example Input — lab-session

A concrete request a user might send to start a Lab.

---

> Start a Lab session for an idea I want to test before committing a project to
> it: **"A 200ms TTL on our RAG embedding cache will not measurably hurt recall
> but will cut p95 retrieval latency by at least 30%."**
>
> Put it under `./labs`. Use the slug `rag-cache-ttl`. I already have two prior
> internal benchmark notes to seed as references:
> - "Q1 retrieval latency baseline" (internal doc)
> - "Recall-vs-cache-size sweep, Apr 2026" (internal doc)
>
> I have NOT decided keep/pivot/kill yet — leave that open.

---

## What the skill should extract
- **Topic:** RAG embedding cache TTL vs. recall/latency trade-off
- **Slug:** `rag-cache-ttl` (supplied)
- **Lab root:** `./labs`
- **Hypothesis:** supplied and already falsifiable (states the refuting outcome:
  measurable recall drop, or <30% p95 improvement)
- **Seed references:** two internal docs → each tagged `[DOC]`
- **Decision:** must start `{POR_CONFIRMAR}` — user explicitly deferred it
