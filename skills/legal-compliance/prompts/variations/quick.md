# Quick variation — legal-compliance (depth=quick)

Essentials only. Use when the requester needs a fast, defensible read, not an
exhaustive audit.

## Behavior
- Resolve `topic`, read one playbook, run Discover → Analyze → Execute → Validate at
  the essentials tier.
- compliance-assessment: assess the named framework(s) only; surface the top
  Critical/High gaps with severity + residual-risk band + one remediation each.
  State which frameworks were out of scope (guard against false completeness).
- compliance-framework: produce the control table for the in-scope control family;
  mark each row met/partial/gap with an evidence pointer or "gap, owner needed."
- contract-review: walk the high-leverage clauses (liability/indemnity, termination,
  auto-renewal, payment); flag only High/Med findings with a one-line redline each.

## Non-negotiables (still required at quick depth)
- One Alfa-core evidence tag per non-obvious claim; `[SUPUESTO]` → verification step.
- Verbatim legal disclaimer present.
- No invented citations, fines, or clause numbers; no PASS-as-fact.
- If critical input is missing, stop and ask — quick depth does not waive this.
