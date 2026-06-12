# Example input — ai-architecture routing

A user brings this ask to the router:

> "We're building an internal assistant over ~2M of our own support and policy
> documents. Answers must be grounded strictly in those documents and must cite
> the specific source chunk. Latency budget is p95 < 800ms, and the corpus is
> updated weekly. Design the retrieval and answer-grounding flow for us."

Invocation parameters:
- `topic`: (to be resolved by the router — not supplied explicitly)
- `depth`: `deep`

What the router must do:
1. Confirm the ask is AI-system shaped. [INFERENCIA]
2. Resolve intent → exactly one `topic`. The ask is about retrieval orchestration
   and grounded, cited answers over a large, changing corpus — this is
   `rag-patterns`, not `embedding-strategy` (no model/dimension/metric question is
   being asked) and not `prompt-engineering` (no instruction-design ask). [DOC]
3. Read ONLY `references/rag-patterns.md`. [DOC]
4. Apply the playbook at `deep`, honoring its retrieval + answer eval gate. [DOC]
