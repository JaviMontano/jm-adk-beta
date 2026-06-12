# Quick variation — fast routing, essentials only

For `depth=quick`. Resolve and dispatch with minimal ceremony, full discipline.

1. **Resolve** the single best `topic` by intent (one line of rationale). If two
   fit equally, ask one question; if none fit, stop. [SUPUESTO]
2. **Read** exactly one `references/<topic>.md` — nothing else. [DOC]
3. **Apply essentials only** — the playbook's core decision order and its primary
   artifact. Skip exhaustive enumeration; still honor the playbook's hard gate
   (e.g. rag-patterns grounding; structured-output schema validation). [INFERENCIA]
4. **Emit** the artifact with Alfa core tags, one family. [CONFIG]

Gate: one topic in enum, one playbook Read, one tag family, playbook gate met. [DOC]

Example: "Pick an embedding model for 5M support chunks, cosine, p95<300ms" →
topic=`embedding-strategy`, quick → recommend hosted model + dimension + HNSW
index + cosine, with the recall/cost/latency rationale. [INFERENCIA]
