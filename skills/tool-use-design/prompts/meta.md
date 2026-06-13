# Meta Prompt — Tool Use Design (self-check)

Use this to audit a draft routing-contract report before the guardian gate.

## Self-interrogation

- **Contract completeness**: does every description declare input format, output shape, 1–2 examples, and a boundary? If any is missing, the description is not yet a contract. [DOC]
- **Boundary reciprocity**: for each competing pair, does X point to Y *and* Y point back to X? A one-way mention fails. [DOC]
- **Overload honesty**: did I resolve any >1-responsibility tool with `rename_split`, or did I hide it in prose? Prose is a silent failure. [INFERENCIA]
- **Repo strategy**: is the sequence exactly `grep, read, edit`? Did I forbid `read_all_upfront` and `glob_all_then_read_all`? [DOC]
- **Edit safety**: is `unique_anchor_required=true` set, with `read_write_full_rewrite` as fallback? [CÓDIGO]
- **Determinism**: are `offline`, `network_required`, `deterministic` flags set correctly? [DOC]
- **Evidence discipline**: is every claim tagged with one Alfa-core family — no mixing? [CONFIG]

## Bias checks

- Am I preferring prose because splitting "feels heavier"? The extra tool surface is linear and cheap. [INFERENCIA]
- Am I tempted to read-all "to be safe"? Measure the token cost first; default to selective. [SUPUESTO]
- Am I treating an ambiguous Edit anchor as safe? It is not — expand it or fall to Write. [CÓDIGO]
