# iikit Routing Report — {Feature / Project}

> One report per invocation. Replace every `{...}` with real content; leave no
> placeholder tokens. Use a single IIK evidence-tag family throughout.

## 1. Resolution
- **Requested:** {raw user request}
- **Resolved topic:** {00-constitution | ... | core} [CONFIG]
- **Resolution basis:** {named stage | number | inferred earliest-unmet stage} [INFERENCE]
- **Depth:** {quick | deep} [CONFIG]
- **Playbook read (exactly one):** references/{file}.md [INFERENCE]

## 2. Predecessor check
| Required predecessor artifact | Present? | Action |
|-------------------------------|----------|--------|
| {e.g. PREMISE.md / spec.md / plan.md} | {yes/no} | {proceed / created explicitly / stopped} |

## 3. Determinism (scripts run)
| Script | Phase | Key JSON fields parsed | Result |
|--------|-------|------------------------|--------|
| {check-prerequisites.sh} | {NN} | {FEATURE_DIR, AVAILABLE_DOCS, ...} | {ok / surfaced failure} |

## 4. Stage artifact produced
- **Path(s):** {CONSTITUTION.md / specs/NNN-*/spec.md / tests/features/*.feature / ...}
- **Summary:** {what was written, e.g. "constitution v1.0.0, 4 principles"} [EXPLICIT]
- **Integrity controls touched:** {tdd_determination persisted / assertion hash LOCKED / SC->FR traceability / phase-separation clean} [EXPLICIT]

## 5. Validation gate (stage acceptance criteria)
- [ ] {criterion 1 from the stage's Validation Gate} [EXPLICIT]
- [ ] {criterion 2} [EXPLICIT]
- [ ] One evidence-tag family; zero placeholder tokens; no invented prices; no PII [CONFIG]

## 6. Next step
- **Primary:** {next_step from next-step.sh} (model: {tier})
- **Alternatives:** {alt_step — reason (model: tier)}
- **Dashboard:** file://{resolved}/.specify/dashboard.html

## 7. Assumptions & limits
- {explicit assumptions made during routing/execution} [ASSUMPTION]
