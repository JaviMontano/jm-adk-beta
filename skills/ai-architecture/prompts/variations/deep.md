# Deep variation — exhaustive playbook application

For `depth=deep`. Same single-topic discipline, maximal rigor.

1. **Resolve** the single best `topic`; record the routing rationale (intent,
   candidates, tie-break by ownership). Still exactly one topic. [DOC]
2. **Read** exactly one `references/<topic>.md` — never a second to "compare". [DOC]
3. **Apply exhaustively** — every step of the playbook's procedure, verifying at
   each step:
   - Decision order, all trade-offs, failure modes / edge cases.
   - The playbook's full evaluation gate (e.g. rag-patterns: labeled retrieval set
     ≥50 queries, recall@k + faithfulness + citation correctness; ai-conops: full
     `jm-labs.ai-conops.report.v1` schema; structured-output: parse+validate+recover
     on every response). [DOC]
   - Deterministic/script checks where the playbook defines them, run offline. [CÓDIGO]
4. **Emit** the complete artifact with Alfa core tags, one family; surface
   assumptions as `[SUPUESTO]` for stakeholder validation. [CONFIG]

Gate (stricter): every playbook step verified, eval gate passed with evidence,
no improvisation, no second playbook, single tag family. [DOC]
