# Body of Knowledge — legal-compliance

Domain reference for the three lanes this router serves. Grounded in the skill's
own playbooks; evidence-tagged per the Alfa core set.

## 1. Routing model

`topic ∈ {compliance-assessment, compliance-framework, contract-review}` selects
one playbook. `depth ∈ {quick, deep}`. One topic = one file. The spine is
**Discover → Analyze → Execute → Validate**, identical across lanes; only the
domain object (regulation, control library, contract) changes. [DOC]

## 2. Regulatory frameworks (compliance-assessment lane)

| Framework | Anchor obligation | Gap trigger |
|-----------|-------------------|-------------|
| GDPR | Art. 30 RoPA, Art. 32 security of processing | Encryption absent, no processing register [DOC] |
| SOX | ICFR, segregation of duties, 7-year retention | Change/access controls undocumented [DOC] |
| PCI-DSS | Req. 3 (PAN protection), Req. 10 (audit logging) | Cardholder data unencrypted [DOC] |
| HIPAA | Privacy & Security Rule safeguards on PHI | Access/audit controls on PHI missing [DOC] |
| ISO 27001 | Annex A controls + ISMS | Asset register / control owner missing [DOC] |
| NIST CSF | Identify-Protect-Detect-Respond-Recover | Function-level coverage gap [DOC] |

Default scope is `multi` — most organizations are subject to several regulations;
a single-framework run creates false completeness. [EXPLICIT]

## 3. Scoring (single method — no scale drift)

- **Gap severity** = max(control absence, regulatory weight): Critical (mandatory
  control absent + fines/license/breach-notification), High (partial/ineffective or
  undocumented compensating control), Medium (recommended control missing or doc
  gap), Low (cosmetic). [DOC]
- **Residual risk** = Likelihood (1–5) × Impact (1–5) → band: 1–4 green, 5–9 yellow,
  10–14 orange, 15–25 red. Impact anchors to regulatory penalty tier, not
  engineering effort. [SUPUESTO → confirm penalty tiers with legal counsel]
- **Anti-scope (never score):** absolute fine amounts, probability of enforcement,
  insurance/indemnity adequacy. [DOC]

## 4. Control-to-evidence (compliance-framework lane)

A control claim is only "met" with a locatable artifact. Worked anchors:
SOC2 CC6.1 → IAM policy export + access-review log; ISO 27001 A.8 → versioned asset
register with owner; GDPR Art. 30 → RoPA covering every processing activity. A
control with no checkable pointer is a gap — "evidence theater" is the top failure
mode. Pin the framework version in Discover; control IDs differ across versions. [INFERENCIA]

## 5. Clause risk (contract-review lane)

High-leverage clauses, ranked by exposure (likelihood × business impact), not order:
liability/indemnity (uncapped + broad carve-out = top risk), termination
(for-convenience vs for-cause, notice, cure, survival), auto-renewal (opt-out
deadline, price escalation), payment, IP/license, confidentiality/data
(sub-processor + breach-notice duties), dispute resolution. Every High finding must
carry a concrete, counterparty-acceptable fallback. [INFERENCIA]

## 6. Decision rules (cross-lane)

1. Two lanes fit → ask one disambiguating question; never guess. [DOC]
2. Conflicting requirements (GDPR erasure vs SOX 7-year retention; cap vs carve-out)
   → surface and route to legal/DPO with both citations; do not resolve. [INFERENCIA]
3. Undocumented control → max "partial," never "present"; first roadmap item is
   "establish control documentation." [EXPLICIT]
4. Missing critical input (governing law, framework version, executed contract,
   missing exhibit) → stop and ask. [DOC]
5. Local regulation (Ley 1581, LGPD) → require user-supplied requirement text. [EXPLICIT]

## 7. Standing constraints

- Output is decision support / pre-audit readiness, **not** legal advice,
  certification, or attestation. Verbatim disclaimer mandatory on every output. [DOC]
- Point-in-time snapshot; date-stamp and flag scope-change invalidation. [INFERENCIA]
- Evidence taxonomy: `[CÓDIGO]` `[CONFIG]` `[DOC]` `[INFERENCIA]` `[SUPUESTO]`,
  one spelling, each `[SUPUESTO]` paired with a verification step. [DOC]
