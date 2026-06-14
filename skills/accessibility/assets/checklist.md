# Accessibility Deliverable Checklist

Reusable gate for any accessibility deliverable, used by the guardian agent and the
output template before declaring "done". Mirrors the four playbooks' Quality Gates. [DOC]

## Routing
- [ ] Exactly one playbook loaded (audit / design / testing / writing)
- [ ] Topic matches user intent; multi-topic work sequenced, not merged
- [ ] Target artifact + assumed WCAG level (AA unless stated) recorded

## Evidence
- [ ] Every finding cites a specific WCAG success criterion + concrete fix
- [ ] Automated: tool/version, target, rule id, impact, selector, WCAG tags, artifact
- [ ] Manual: keyboard, screen-reader (with AT+browser pairing), contrast, motion
- [ ] Contrast results carry the ratio and threshold, or `not verified` + next action
- [ ] axe "0 violations" reported as "no automated violations", not "accessible"

## Status
- [ ] Final status is `pass` / `conditional` / `fail` / `not verified`
- [ ] No green-as-success; a clean scan never overrides a manual blocker
- [ ] No "WCAG compliant" without level, scope, tested technologies, date, evidence

## Topic extras
- [ ] design: name/role/value/state + keyboard map + focus plan + contrast tokens
- [ ] testing: suppressions carry issue id, owner, expiry, re-enable criteria
- [ ] writing: reader-facing copy is tag-free; separate validation table; no invented detail

## Governance
- [ ] One evidence tag per claim, single family (no tag drift)
- [ ] No invented prices, no client PII, single-brand
