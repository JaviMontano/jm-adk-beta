# Example Output — pm-delivery (risk-assessment route)

> Routed topic: **risk-assessment** · Depth: **deep** · Playbook:
> `references/risk-assessment.md`

## 1. Context and inputs
- Orders service migrating monolith → Firebase/Firestore before Q3 launch. [EXPLICIT]
- Inputs: `firestore.rules` draft, `migration-plan.md`, team note. [EXPLICIT]
- Constraint: timeline commitment pending this assessment. [EXPLICIT]
- Gap: no backup/restore step in the migration plan. [DOC]

## 2. Method applied
Loaded only `references/risk-assessment.md`. Ran Discover → Analyze → Execute →
Validate; walked all 7 categories; scored Severity × Likelihood; named a
mitigation per High/Medium. [EXPLICIT]

## 3. Risk register
| ID | Category | Risk | Sev | Lik | Score | Evidence | Mitigation |
|----|----------|------|-----|-----|-------|----------|------------|
| RISK-001 | Security | Firestore rules allow unauthenticated writes to `/orders` | 5 | 4 | 20 (High) | [CONFIG] firestore.rules:12 | Require `request.auth != null` + owner check before launch |
| RISK-002 | Data | Migration plan has no backup/restore step for 5 legacy tables | 5 | 3 | 15 (High) | [DOC] migration-plan.md | Add tested backup + restore rehearsal pre-cutover |
| RISK-003 | Team | Bus factor 1 on on-call; one engineer onboarded 3 weeks ago | 4 | 3 | 12 (Medium) | [DOC] team note | Pair on payments path; document runbook; add second on-call |
| RISK-004 | Timeline | Payments path on critical path with thin estimate confidence | 4 | 3 | 12 (Medium) | [INFERENCE] from scope + team size | Discovery spike on payments before committing the date |
| RISK-005 | Technical | New persistence model (Firestore) unproven for this team | 3 | 3 | 9 (Medium) | [INFERENCE] | Spike + read/write pattern review |
| RISK-006 | Operational | No documented rollback for the cutover | 4 | 2 | 8 (Medium) | [ASSUMPTION] not in plan | Define rollback + monitoring before cutover |
| RISK-007 | Scalability | Order write volume vs. Firestore hotspot limits unknown | 3 | 2 | 6 (Low) | [ASSUMPTION] | Load-test write key distribution |

## 4. Evidence tag summary
- `[EXPLICIT/CONFIG/DOC]`: ~71%  ·  `[INFERENCE]`: ~14%  ·  `[ASSUMPTION]`: ~14%
- WARNING banner (>30% ASSUMPTION): not triggered. [EXPLICIT]

## 5. Recommendations
- Do not commit the Q3 date until RISK-001 and RISK-002 are mitigated and the
  payments spike (RISK-004) lands — both High risks are launch-blocking. [INFERENCE]

## 6. Acceptance gate
- [x] Exactly one playbook loaded; output matches the register schema
- [x] Every non-trivial claim tagged
- [x] No raw prices (none applicable; no currency used)
- [x] All 7 categories addressed; every High/Medium has a named mitigation
- [x] No implementation steps (phase separation, Art. 1.5); Constitution v6.0.0
      + script-first; single brand; no client PII
