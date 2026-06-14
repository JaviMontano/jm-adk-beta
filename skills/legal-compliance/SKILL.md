---
name: legal-compliance
version: 1.0.0
description: "Route legal/compliance work to one playbook: contract-review, compliance-assessment (GDPR/SOX/PCI-DSS/HIPAA/ISO 27001/NIST CSF), or compliance-framework design."
params:
  topic:
    enum: [compliance-assessment, compliance-framework, contract-review]
    required: true
    infer: from user request; ask only if ambiguous
  depth:
    enum: [quick, deep]
    default: quick
routes:
  compliance-assessment: references/compliance-assessment.md
  compliance-framework: references/compliance-framework.md
  contract-review: references/contract-review.md
---

# legal-compliance

Router skill. Resolve `topic`, then Read EXACTLY ONE playbook from `routes:`.
Never load the whole cluster — one topic = one file. [DOC]

## When to use
- Reviewing a contract/clause for risk, obligations, or red flags → `contract-review`. [DOC]
- Measuring posture against a named regulation/standard → `compliance-assessment`. [DOC]
- Designing controls, policies, or a control library from scratch → `compliance-framework`. [DOC]
- NOT for: drafting net-new legal text, litigation strategy, or jurisdiction-specific advice — flag and defer to counsel. [INFERENCIA]

## Routing
1. Infer `topic` from the request; if two fit, ask one disambiguating question — never guess. [DOC]
2. `depth=deep` → apply the playbook exhaustively, verify at each step; `quick` → essentials only. [CONFIG]
3. Read only the routed file. If the request spans topics, run them sequentially, one playbook each. [INFERENCIA]

Spine: Discover → Analyze → Execute → Validate.

## Validation gate (before "done")
- Output names the regulation/contract scope explicitly; no silent assumptions. [DOC]
- Every non-obvious claim carries one Alfa-core tag (`[CÓDIGO]` `[CONFIG]` `[DOC]` `[INFERENCIA]` `[SUPUESTO]`), one spelling throughout. See `references/verification-tags.md`. [DOC]
- Each `[SUPUESTO]` is paired with a concrete verification step; missing critical input → stop and ask. [DOC]
- Quality gates: constitution v6.0.0 (enforcement), script-first rule. [CONFIG]
- Check output against the binary per-lane rubric in `assets/` (see `assets/quality-rubric.json`). [CONFIG]

## Anti-patterns
- Loading multiple playbooks "for context" — defeats the router; pick one. [INFERENCIA]
- Asserting compliance/PASS as fact without an evidence tag. [SUPUESTO]
- Inventing clause numbers, fines, or regulatory citations — degrade to `[SUPUESTO]` and flag. [DOC]
