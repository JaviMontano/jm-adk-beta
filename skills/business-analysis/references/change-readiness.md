<!-- distilled from alfa skills/change-readiness -->
<!-- > -->
# Change Readiness

> "People don't resist change. They resist being changed." — Peter Senge

## TL;DR

Evaluates organizational readiness for technology or process changes using the ADKAR model, surfaces resistance sources, and designs targeted interventions to drive adoption. Run before major rollouts, platform migrations, or after a prior change initiative has stalled. [EXPLICIT]

**Scope.** Diagnosis + intervention design for a single, bounded change. [EXPLICIT]
**Anti-scope.** Not a project plan, not org-design/restructuring advice, not a comms-copywriting deliverable, not a substitute for a sponsor decision. Hand those to `executive-pitch`, `workshop-design`, or the program owner. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify the change scope: what is changing, who is affected, what stays the same
- Assess the org's change history and fatigue level (count concurrent/recent initiatives) [INFERENCE]
- Map affected groups by function, location, and impact severity

### Step 2: Analyze
- Score each affected group on ADKAR dimensions (1–5 scale; 5 = fully ready):
  - **Awareness**: Do they know why the change is happening?
  - **Desire**: Do they want to participate and support it?
  - **Knowledge**: Do they know how to change?
  - **Ability**: Can they implement the change day-to-day?
  - **Reinforcement**: Are there mechanisms to sustain it?
- Map resistance sources: fear of job loss, comfort with status quo, past failures, lack of trust
- Identify the **first** dimension scoring ≤3 in ADKAR order — that is the barrier point. Higher dimensions are gated by it; do not invest downstream until the barrier is cleared. [INFERENCE]

### Step 3: Execute
- Design targeted interventions for each barrier point, per affected group
- Communication plan → Awareness and Desire gaps
- Training programs → Knowledge gaps
- Coaching and support systems → Ability gaps
- Recognition and measurement systems → Reinforcement

### Step 4: Validate
- Verify interventions target the **actual** barrier point, not assumed ones
- Confirm sponsors are trained and actively, visibly supportive
- Check success metrics go beyond adoption rate (include satisfaction, productivity)
- Validate the timeline allows for learning curves and adjustment periods

## Worked Example (ADKAR scoring → barrier → intervention)

Group: Branch operations staff, ERP migration. [EXPLICIT]

| Dimension | Score | Evidence |
|---|---|---|
| Awareness | 4 | Town-hall held; staff can state the "why" |
| Desire | 2 | Survey shows fear of headcount cuts |
| Knowledge | 3 | Training booked but not delivered |
| Ability | 1 | No sandbox access yet |
| Reinforcement | 1 | No incentives defined |

Barrier = **Desire (2)** — the first dimension ≤3 in ADKAR order. Knowledge/Ability/Reinforcement are downstream and gated by it. Intervention: sponsor addresses job-security directly + names early adopters; defer training spend until Desire ≥4. Re-score before advancing. [INFERENCE]

## Quality Criteria

- [ ] All affected groups assessed on all 5 ADKAR dimensions
- [ ] Barrier point identified per group, with a specific intervention designed
- [ ] Communication plan addresses *why* before *how*
- [ ] Resistance mapping includes specific engagement strategies
- [ ] Each barrier-point claim cites the evidence behind the score
- [ ] Evidence tags applied to all non-obvious claims

## Acceptance Criteria (output is "done" when)

- Every affected group has a 5-dimension score table with one-line evidence per score. [EXPLICIT]
- Exactly one barrier point named per group, justified by ADKAR ordering. [EXPLICIT]
- At least one intervention maps to each named barrier, owned and time-boxed. [EXPLICIT]
- Success metrics include ≥1 outcome metric beyond login/adoption count. [EXPLICIT]
- No dimension scored without stated evidence; gaps tagged `[SUPUESTO]` with a verification step. [DOC]

## Anti-Patterns

- Training-only change management (skipping Awareness and Desire)
- Big-bang rollout without pilot or phased approach
- Measuring adoption by tool login counts instead of outcome metrics
- Averaging the 5 ADKAR scores — averages hide the gating barrier; use the minimum-in-order, not the mean [INFERENCE]
- Scoring from the sponsor's view alone — score from the affected group's perspective [INFERENCE]

## Failure Modes

| Failure mode | Symptom | Mitigation |
|---|---|---|
| Wrong barrier targeted | Adoption flat despite heavy training | Re-score; confirm barrier is first ≤3 in order |
| Sponsor absent | Staff cite "leadership not behind it" | Gate go-live on visible sponsor actions |
| Change fatigue ignored | Cynicism, low survey response | Sequence/pause concurrent initiatives |
| Vanity metrics | Green dashboard, no behavior change | Add productivity/satisfaction outcome metrics |

## Decisions & Trade-offs

- **ADKAR over Kotter/Lewin**: individual-level diagnosis yields per-group barriers and actionable interventions; the trade-off is weaker treatment of enterprise-wide structural change — pair with org-design work when the change is structural, not behavioral. [INFERENCE]
- **Barrier = first ≤3, not lowest score**: ADKAR is sequential, so the earliest weak dimension blocks all later ones; chasing the numerically lowest dimension wastes effort if an earlier one is unmet. [INFERENCE]
- **Pilot before big-bang**: a pilot trades calendar time for de-risked rollout and real ADKAR evidence; skip only when scope is trivial and reversible. [INFERENCE]

## Related Skills

- `stakeholder-mapping` — identifies who is affected and their influence
- `workshop-design` — facilitates change readiness sessions
- `executive-pitch` — secures sponsor commitment for change initiatives

## Usage

Example invocations:

- "/change-readiness" — Run the full change readiness workflow
- "change readiness on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Assumes affected-group input is reachable (survey, interview, or proxy); if not, scores are `[SUPUESTO]` pending validation [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Diagnoses readiness; does not execute the change or own the rollout schedule [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| No access to affected groups | Score from proxies, tag `[SUPUESTO]`, name the validation step |
| Multiple changes at once | Assess fatigue first; recommend sequencing before scoring |
| All dimensions already ≥4 | Confirm with evidence; shift to Reinforcement and monitoring |
