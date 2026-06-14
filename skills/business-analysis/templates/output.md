# Business Analysis Deliverable — <project / feature name>

> Skill: `business-analysis` · Topic: `<resolved-topic>` · Depth: `<quick|deep>`
> Spine: Discover → Analyze → Execute → Validate

## 1. Routing record
- **Resolved topic:** `<topic>` — selected because `<dominant signal in request>`. [DOC]
- **Playbook loaded:** `references/<topic>.md` (exactly one). [DOC]
- **Scope boundaries:** start `<...>`, end `<...>`, unit under assessment `<...>`. [DOC]
- **Out of scope (redirected):** `<architecture / pricing / sprint plan, if any>`. [CONFIG]

## 2. Discover
- Inputs gathered: `<docs, code, configs, interviews, surveys>`. [DOC]
- Constraints: technical / stack `<Firebase·Google·Hostinger>`, timeline, team, NFRs. [CONFIG]
- Open gaps logged as `[ASSUMPTION]` with verification steps: `<list>`.

## 3. Analyze
<Fill the section that matches the topic; delete the others.>

### Process modeling
- As-is BPMN summary (pools/lanes/gateways/events). Bottleneck: `<...>`. [EXPLICIT]
- Value-stream: lead time `<>`, value-add `<>`, **PCE = `<>`%**. Top waste: `<category>`. [EXPLICIT]

### Flow mapping
- DDD bounded contexts: `<list>`. Flows selected (8–12): `<F-NN names>`. [EXPLICIT]
- Integration matrix rows: `<count>` (reconciled to sequence-diagram arrows). [EXPLICIT]

### Requirements
- INVEST stories: `<count>`. AC coverage: happy / negative / boundary present. [DOC]
- Traceability: requirements `<>` ↔ objectives `<>`, orphans = 0. [DOC]

### Feasibility
| Dim | Architecture | Team | Timeline | Cost | Risk | Integration | Scalability |
|-----|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| Score (1–5) | | | | | | | |
- Mean `<>`; showstoppers (any 1): `<...>`. [INFERENCE]

### Scenario analysis
| Scenario | Crit-A `<w>` | Crit-B `<w>` | Crit-C `<w>` | Weighted |
|----------|:--:|:--:|:--:|:--:|
- Weights sum to 1.0, locked pre-scoring. Sensitivity / close-call: `<...>`. [INFERENCE]

### Change readiness
| Group | Awareness | Desire | Knowledge | Ability | Reinforcement | Barrier |
|-------|:--:|:--:|:--:|:--:|:--:|:--|
- Barrier = first ≤3 in ADKAR order, per group. [INFERENCE]

## 4. Execute — deliverable artifacts
- `<BPMN / Mermaid sequence diagrams / story list / scorecard / scenario matrix / ADKAR table>`
- Mermaid blocks inline where applicable (≤12 messages each). [EXPLICIT]

## 5. Recommendation
- **Decision:** `<go / no-go / conditional-go / recommended scenario / barrier intervention>`. [INFERENCE]
- **Justified trade-off:** `<not just the top number>`. [INFERENCE]
- **Confidence:** `<%>` — biggest unknown: `<...>`. [INFERENCE]
- Effort expressed in FTE-time only; **no pricing**. [CONFIG]

## 6. Validate (acceptance gate)
- [ ] Exactly one playbook loaded; topic matches intent. [DOC]
- [ ] Topic-specific quality criteria met (see `assets/quality-rubric.json`). [DOC]
- [ ] Every claim tagged, one family, consistent spelling; no orphans. [DOC]
- [ ] `[ASSUMPTION]` ratio ≤30% (else WARNING banner present). [EXPLICIT]
- [ ] No phase leakage; stack lens honored. [CONFIG]

## 7. Evidence-tag summary
`[CODE] <%> · [CONFIG] <%> · [DOC] <%> · [INFERENCE] <%> · [ASSUMPTION] <%>`
> If `[ASSUMPTION]` >30%: **⚠ WARNING** — assumption-heavy; top gaps to close: `<list>`.
