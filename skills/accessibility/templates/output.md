# Accessibility Deliverable

> Fill every field. Mark anything untested `not verified` with a next action.
> Status is `pass` / `conditional` / `fail` / `not verified` — never green-as-success.

## 1. Routing & scope
- **Topic:** audit | design | testing | writing  (exactly one)
- **Target:** <URL | route list | component | repo path | copy | image asset>
- **WCAG target:** 2.1 AA (state if different)
- **Depth:** quick | deep
- **Environment:** browser, viewport(s), auth/session state, AT pairing(s), tool versions, date

## 2. Summary verdict
- **Status:** pass | conditional | fail | not verified
- **One-line rationale:** <why this status, in evidence terms>
- **Coverage note:** automated covers ~30–40% of SCs; manual completes the picture.

## 3. Automated evidence
| Route/Component | State | Tool + version | Rule id | Impact | Selector | WCAG tags | Artifact |
|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |

> Report as "N axe violations in scanned states", never "accessible".

## 4. Manual findings
| ID | Type (keyboard/SR/contrast/motion) | WCAG SC (level) | Expected | Observed | Severity | Evidence | Status |
|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |

## 5. Findings detail / remediation tickets
For each finding:
- **WCAG criterion:** <e.g. 2.4.3 Focus Order (AA)>
- **User impact:** <who is blocked and how>
- **Reproducer:** <exact steps>
- **Expected behavior:** <...>
- **Fix / acceptance check:** <concrete, testable>
- **Evidence:** <artifact path or `not verified` + next action>
- **Tag:** <one evidence tag>

## 6. Design / writing addendum (if topic applies)
- **Design:** name · role · value/state · keyboard map · focus plan · contrast/token evidence · acceptance criteria.
- **Writing:** reader-facing copy (tag-free) PLUS a separate validation table — item, issue, rewrite, rationale, evidence/source, assumption, residual risk.

## 7. Suppressions / exceptions
| Item | Issue ID | Owner | Selector | Rule id | Reason | Expiry | Re-enable criteria |
|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |

## 8. Gate checklist
- [ ] Exactly one playbook loaded; topic matches intent
- [ ] Every finding cites a WCAG SC + concrete fix
- [ ] Automated and manual evidence present (or `not verified` + next action)
- [ ] Status is pass/conditional/fail/not-verified; no green-as-success
- [ ] One evidence tag per claim, single family
- [ ] No invented prices, no client PII, single-brand
