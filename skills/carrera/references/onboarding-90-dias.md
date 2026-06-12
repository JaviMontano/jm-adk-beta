<!-- distilled from alfa skills/onboarding-90-dias -->
<!-- Genera y valida planes 30/60/90 para nuevos roles con evidencia, hitos verificables, limites anti-burnout, prioridades acotadas y sin promesas de desempeno no sustentadas. -->
# Onboarding 90 Dias

## Purpose

Use this skill to design a sustainable 30/60/90 onboarding plan for a new role, engagement, or internal transition. The skill converts supplied role evidence into phase-specific priorities, measurable deliverables, learning goals, stakeholder actions, and validation checkpoints while enforcing anti-burnout limits. `[DOC]`

**Use it when:** starting a role, taking a new client engagement, an internal team transfer, or a scope expansion that resets expectations.
**Do NOT use it for:** day-to-day task planning (no phase reset), performance reviews, compensation cases, or HR dispute documentation — those have no 30/60/90 contract and would force invented structure. `[INFERENCIA]`

## Evidence Tags

Every non-trivial claim below carries a tag, matching the house convention in `cierre-conversacion.md`. `[CÓDIGO]`

- `[CÓDIGO]`: local files, commands, fixtures, or script output.
- `[CONFIG]`: an asset policy/contract or workflow rule the skill enforces.
- `[DOC]`: distilled from the canonical alfa skill documentation.
- `[INFERENCIA]`: conclusion derived from the contracts above.
- `[SUPUESTO]`: unverified assumption to confirm with the user.

## Inputs Expected

- Role title, organization or team context, and source evidence for the role expectations. `[DOC]`
- User constraints: weekly hours, energy boundaries, non-negotiables, relocation or parallel-stream constraints. `[DOC]`
- Stakeholder map or known onboarding contacts. `[DOC]`
- Phase priorities for days 1-30, 31-60, and 61-90. `[DOC]`
- Desired output: plan, audit, overload report, stakeholder handoff, or validation packet. `[DOC]`

**Minimum viable input** (below this, planning is blocked): role title + role expectations evidence + weekly-hour capacity. Everything else degrades to open questions, not a block. `[CONFIG]`

## Outputs Expected

- A 30/60/90 plan with exactly three phases. `[CONTRATO via assets/phase-contract.json]` `[CONFIG]`
- At most four priorities per phase and a sustainable weekly-hour estimate. `[CONFIG]`
- Each priority has a deliverable, validation signal, and evidence reference. `[CONFIG]`
- Burnout, always-on, vague promise, missing evidence, and unverifiable task findings. `[DOC]`
- Validation command evidence when a JSON packet is supplied. `[CÓDIGO]`

## Procedure

### Discover

Identify role context, constraints, stakeholders, available evidence, and the user's preferred planning granularity. If role expectations or weekly capacity are missing, block confident planning and request them. `[DOC]`

Capture as `[SUPUESTO]` (never invent): start date, ramp expectations, who owns the 30/60/90 review, and what "good" looks like to the manager. These are the most common silent gaps. `[INFERENCIA]`

### Analyze

Apply `assets/phase-contract.json`, `assets/burnout-policy.json`, `assets/evidence-policy.json`, `assets/validation-policy.json`, and `assets/output-contract.json`. Treat dates, performance guarantees, stakeholder availability, and organizational priorities as unsupported unless supplied. `[CONFIG]`

### Execute

Build the plan phase by phase: `[DOC]`

- Days 1-30: learn, listen, map systems, and ship one small trust-building artifact.
- Days 31-60: contribute to prioritized work, reduce ambiguity, and validate working agreements.
- Days 61-90: own a bounded improvement, document learnings, and propose next operating cadence.

Keep each phase small enough to execute sustainably. Replace always-on language with explicit recovery boundaries. `[CONFIG]`

**Decision — why 4 priorities/phase, not more:** the cap is a forcing function. A phase with 6 priorities reliably overshoots the weekly-hour budget; the contract returns nonzero rather than letting the user silently over-commit. Trade-off: legitimately large roles may feel under-planned in one phase — resolve by deferring priorities to the next phase, not by raising the cap. `[INFERENCIA]`

**Decision — one trust artifact in phase 1, not many:** early credibility comes from one shipped, visible thing, not breadth. Trade-off: ambitious users want to "prove themselves" fast; reframe extra ambition as phase-2 contribution. `[INFERENCIA]`

### Validate

Run the deterministic fixture suite: `[CÓDIGO]`

```bash
bash skills/onboarding-90-dias/scripts/check.sh
```

For one plan packet: `[CÓDIGO]`

```bash
python3 skills/onboarding-90-dias/scripts/plan_30_60_90.py --input <packet.json>
```

Exit code 0 = plan passes all contracts. Nonzero = overload, missing phase, missing evidence, or unsupported-promise language; the message names the failing rule. Never report a pass while a validation is nonzero. `[CÓDIGO]`

## Assets

- `assets/phase-contract.json` — exactly three phases (30/60/90), priority cap. `[CONFIG]`
- `assets/burnout-policy.json` — weekly-hour ceiling and recovery-boundary rule. `[CONFIG]`
- `assets/evidence-policy.json` — what counts as evidence; missing-evidence handling. `[CONFIG]`
- `assets/validation-policy.json` — pass/block/partial decision rules. `[CONFIG]`
- `assets/output-contract.json` — required fields per priority. `[CONFIG]`

## Quality Criteria

- The plan contains phases 30, 60, and 90 exactly once. `[CONFIG]`
- No phase has more than four priorities; three or fewer is preferred. `[CONFIG]`
- Weekly hours are at or below 45 and include recovery boundaries. `[CONFIG]`
- Every priority has evidence, a deliverable, and a validation signal. `[CONFIG]`
- Vague goals like "be strategic" are converted into observable behavior. `[DOC]`
- Performance outcomes are framed as intended contributions, not guaranteed results. `[CONFIG]`
- Missing role evidence produces a blocked or partial plan, not invented priorities. `[CONFIG]`

### Acceptance Criteria (binary, testable)

- [ ] `plan_30_60_90.py` exits 0 on the final packet. `[CÓDIGO]`
- [ ] Each priority resolves to: `{deliverable, validation_signal, evidence_ref}` — no empty field. `[CONFIG]`
- [ ] No priority text contains always-on/hustle markers (e.g. "24/7", "whatever it takes", "no days off"). `[CONFIG]`
- [ ] No outcome is phrased as a guarantee (no "will get promoted", "will be the best"). `[CONFIG]`
- [ ] Every date, headcount, or org-priority claim traces to supplied evidence or is tagged `[SUPUESTO]`. `[INFERENCIA]`

## Edge Cases

- Empty role: block and request the role context. `[CONFIG]`
- Weekly hours above 45: flag overload and return nonzero validation. `[CONFIG]`
- More than four priorities in one phase: flag overload and return nonzero validation. `[CONFIG]`
- Missing phase: block readiness. `[CONFIG]`
- Always-on or hustle language: block and rewrite with sustainable cadence. `[CONFIG]`
- No stakeholders: ask for known contacts or mark stakeholder map as open. `[DOC]`
- User asks for guaranteed promotion or impact: reframe as measurable contribution. `[CONFIG]`
- Exactly 45 hours: passes (boundary is inclusive); 45.5 fails. `[INFERENCIA]`
- Two phases share a date range (e.g. both "1-30"): treat as missing-phase block, not a valid 3-phase plan. `[INFERENCIA]`
- Plan supplied with priorities but no evidence refs: partial plan, not pass — evidence is non-optional. `[CONFIG]`

## Failure Modes (what goes wrong, and the guard)

- **Fabricated org priorities** — model invents "the team's top OKR is X". Guard: org priorities are unsupported unless supplied; tag `[SUPUESTO]`. `[CONFIG]`
- **Hidden over-commitment** — phase looks fine per-priority but sums past 45h. Guard: weekly-hour ceiling is checked at phase level, not per-priority. `[CONFIG]`
- **Promise smuggling** — "deliver X" silently becomes "guarantee promotion". Guard: unsupported-promise scan blocks the packet. `[CONFIG]`
- **Stale paths after refactor** — script/asset paths drift from the canonical skill. Guard: run `check.sh`; a path error fails loudly rather than passing on a missing file. `[CÓDIGO]`

## Worked Example (compact)

Input: role "Data PM", 40 h/week cap, evidence = offer letter + manager brief. `[SUPUESTO: start date unknown → open question]`

- **Phase 30** — Priority: "Map the 3 active data pipelines." Deliverable: one-page system map. Validation: manager confirms map covers all live pipelines. Evidence: manager brief §2. `[CONFIG]`
- **Phase 60** — Priority: "Ship dashboard refresh for weekly review." Deliverable: live dashboard. Validation: used in 2 consecutive reviews. Evidence: offer letter scope. `[CONFIG]`
- **Phase 90** — Priority: "Propose next-quarter data cadence." Deliverable: cadence doc + decision. Validation: steering sign-off. Evidence: manager brief §4. `[CONFIG]`

Result: 3 phases, ≤4 priorities each, 40 h ≤ 45, every field populated → `plan_30_60_90.py` exits 0. `[CÓDIGO]`

## Assumptions and Limits

- This skill supports planning and onboarding; it does not guarantee role success, promotion, compensation, visa, legal, HR, or health outcomes. `[CONFIG]`
- It does not read calendars, fetch company systems, or infer hidden organizational priorities. `[CONFIG]`
- Time estimates are planning inputs supplied by the user, not live workload telemetry. `[DOC]`
- The 45 h ceiling is a default policy value, not a medical threshold; the user's real boundary may be lower. Confirm rather than assume. `[SUPUESTO]`
- Validation is deterministic and offline; a passing packet means contract-valid, not real-world-correct. `[INFERENCIA]`

## Scripts

`scripts/plan_30_60_90.py --input <json>` validates onboarding packets for phase completeness, priority limits, evidence, deliverables, validation signals, anti-burnout rules, and unsupported promise language. `scripts/check.sh` runs valid, blocked, and invalid fixtures offline. `[CÓDIGO]`

## Related Skills

- `negociacion-oferta` — runs before this; decide whether to accept before planning the ramp. `[DOC]`
- `red-y-referencias` — feeds the stakeholder map this skill consumes. `[INFERENCIA]`
- `proceso-seleccion-orchestrator` — upstream router that hands off into onboarding. `[DOC]`

## Evidence Requirements

- Tie role expectations, stakeholder commitments, deliverables, and validation signals to supplied evidence. `[CONFIG]`
- Mark missing evidence, stakeholder uncertainty, and capacity assumptions as open questions. `[CONFIG]`
- Report validation commands and results when a machine-readable packet is used. `[CÓDIGO]`

## Update-Safety Notes

- Keep validation offline and deterministic. `[CONFIG]`
- Do not add calendar, HR system, or network calls. `[CONFIG]`
- Do not modify other skills while hardening this one. `[CONFIG]`
- If you change a contract default (e.g. the 45 h ceiling), update `burnout-policy.json` AND its fixtures together, or `check.sh` will fail. `[INFERENCIA]`
