# AI Architecture Routing Deliverable

> Scaffold for the router's handoff. The body artifact is whatever the chosen
> playbook defines; this wrapper records the routing decision and gate result.

## 1. Request summary
- **Ask (verbatim/paraphrased):** <one line>
- **AI-system shaped?** yes / no — if no, do not route here. [INFERENCIA]

## 2. Routing decision
| Field | Value |
|-------|-------|
| Resolved `topic` | <one enum value> |
| `depth` | quick \| deep |
| Playbook Read | `references/<topic>.md` |
| Tie-break applied | <ownership rule, or "none — single fit"> |

Routing rationale (intent, not keywords): <1–2 sentences> [INFERENCIA]

## 3. Playbook artifact
<The deliverable produced by the chosen playbook — e.g. RAG pipeline design,
CONOPS packet, embedding recommendation, prompt instruction package, audit
findings. Keep the playbook's own structure and gates.> [DOC]

## 4. Validation gate result
- [ ] Exactly one `topic`, present in the enum. [DOC]
- [ ] Exactly one playbook Read; cluster not bulk-loaded. [DOC]
- [ ] Output uses ONE evidence-tag family (Alfa core). [CONFIG]
- [ ] Playbook's own gate satisfied (name it): <gate> [DOC]
- [ ] `depth` honored (quick=essentials / deep=exhaustive). [INFERENCIA]

## 5. Evidence tags
Alfa core only: `[DOC]` `[CONFIG]` `[CÓDIGO]` `[INFERENCIA]` `[SUPUESTO]`. [CONFIG]

## 6. Governance check
- [ ] No invented prices. [SUPUESTO]
- [ ] No client PII. [SUPUESTO]
- [ ] Single brand. [SUPUESTO]

## 7. Open assumptions / gaps
- <`[SUPUESTO]` items for stakeholder validation, or "none">
