# Meta prompt — reasoning about the ai-architecture router

Use this to reason about HOW to route, and to self-check the routing decision.

## Routing rationale to produce
Before reading any playbook, state:
1. **Intent extracted** — what the user actually wants (design vs audit vs
   implement; which AI subsystem). [INFERENCIA]
2. **Candidate topics** — the 1–2 enum values that could fit, with why. [INFERENCIA]
3. **Tie-break** — if two fit, the ownership rule that decides (e.g. embedding
   model choice → embedding-strategy, NOT rag-patterns). [DOC]
4. **Chosen topic + depth** — the single selection and `quick`|`deep`. [DOC]

## Self-interrogation (answer before dispatch)
- Is this request even AI-system shaped? If not, do not route here. [INFERENCIA]
- Am I about to Read more than one playbook? If yes, stop — pick one. [DOC]
- Does the playbook I chose actually own this slice, or am I keyword-matching? [SUPUESTO]
- Which tag family will the output use? (Alfa core only.) [CONFIG]

## After dispatch — fit check
If the playbook does not address the ask, do NOT patch with a second playbook:
stop, re-resolve `topic`, Read the correct one. If no enum value fits, report the
gap explicitly. [SUPUESTO]

## Meta-governance
Green is not assumed success: state the evidence for each gate pass. No prices,
no PII, single brand, deterministic checks run offline. [CONFIG]
