# pm-delivery Deliverable — {{topic}}

> Routed topic: **{{topic}}** · Depth: **{{quick|deep}}** · Playbook:
> `references/{{topic}}.md`

## 1. Context and inputs
- Request summary: …
- Inputs gathered (artifacts/docs/code/configs): …
- Constraints / NFRs: …
- Known gaps (state explicitly): … [EXPLICIT|ASSUMPTION]

## 2. Method applied
One-paragraph statement of the playbook method used and the spine phases run
(Discover → Analyze → Execute → Validate). [EXPLICIT]

## 3. Deliverable body
Fill the block matching the routed topic; delete the others.

### cost-estimation / budget-management / capacity-planning (FTE-months — NO prices)
| Workstream | Inductors | Multiplier (justified) | Opt | Exp | Pess |
|-----------|-----------|------------------------|-----|-----|------|
| … | … | … | … | … | … |
| **Total** | — | — | … | … | … |
Disclaimer: figures are FTE-months, not cost; no rates applied. [EXPLICIT]

### risk-assessment (7 categories)
| ID | Category | Risk | Sev | Lik | Score | Evidence | Mitigation |
|----|----------|------|-----|-----|-------|----------|------------|
| RISK-001 | … | … | … | … | … | [CONFIG] … | … |

### okr-design
- **Objective** (qualitative, no metric): …
- **KR1 …KRn**: baseline → target → due → owner; committed/stretch.

### stakeholder-mapping / team-topology / sla-definition / vendor-evaluation / roadmap / retro
Use the playbook's native schema (power-interest grid + RACI; team types +
interaction modes; SLI/SLO/SLA + error budget; weighted scorecard; Now/Next/
Later; what-went-well / actions).

## 4. Evidence tag summary
- `[EXPLICIT]`: __%  ·  `[INFERENCE]`: __%  ·  `[ASSUMPTION]`: __%
- WARNING banner if `[ASSUMPTION]` > 30%: ☐

## 5. Recommendations / next steps
Actionable items, each tagged. [INFERENCE]

## 6. Acceptance gate
- [ ] Exactly one playbook loaded; output matches its template
- [ ] Every non-trivial claim tagged
- [ ] No raw prices (FTE-months only where applicable)
- [ ] Topic-specific completeness met (categories / bands / KR shape)
- [ ] Constitution v6.0.0 + script-first satisfied; single brand; no client PII
