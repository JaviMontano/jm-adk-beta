# Deep variation — legal-compliance (depth=deep)

Exhaustive, audit-grade pass. Verify at each step of the spine.

## Behavior
- compliance-assessment: 100% requirement coverage of every in-scope framework
  (every control ID present, not sampled). Build the full gap matrix (severity,
  evidence tag, residual-risk L×I, owner role, effort band), the regulatory risk
  heat map from the SAME scores, and a phased roadmap (0–30 / 30–90 / 90–365d) where
  every action maps to ≥1 gap ID. Handle multi-framework overlap by mapping shared
  controls once and tagging all frameworks they discharge. Surface conflicts
  (GDPR erasure vs SOX retention) to legal/DPO with both citations.
- compliance-framework: one row per control across the full framework; every "met"
  has a locatable artifact (else downgrade to gap); pin the framework version;
  check artifact dates against the audit window.
- contract-review: every Step-2 checklist clause addressed or N/A; rank findings by
  exposure; every High finding carries a counterparty-acceptable fallback; analyze
  worst-case interpretation of conflicting clauses.

## Verification at each step
After Analyze and again at Validate, re-check: tag coverage, scoring consistency
(no scale drift), gap↔action bidirectional mapping, disclaimer presence, and that no
`[SUPUESTO]` lacks a verification step. Date-stamp the snapshot.
