<!-- distilled from alfa skills/developer-onboarding -->
<!-- > -->
# Developer Onboarding
> "Method over hacks."

## TL;DR
Author an onboarding guide that gets a new engineer to first merged PR fast and
to independent delivery soon after. Deliverables: a sequenced checklist, a
buddy/mentor pairing, and explicit ramp-up metrics with target windows. This is
a writing playbook, not an HR/provisioning process. [DOC]

## Procedure
### Step 1: Discover
- Pull the actual setup path from repo artifacts (README, `Makefile`,
  `.env.example`, CI config) — never invent steps. Tag each `[CÓDIGO]`/`[CONFIG]`. [DOC]
- Identify the target role/seniority and the "done" bar (first PR vs. on-call). [DOC]

### Step 2: Analyze
- Order tasks by dependency, not importance: environment → build/test green →
  read one subsystem → ship a trivial real change. [INFERENCIA]
- Choose ramp metrics + windows (defaults below); evaluate options per
  Constitution XIII/XIV. Mark chosen defaults `[SUPUESTO]`. [INFERENCIA]

### Step 3: Execute
- Write the checklist as verifiable, single-outcome steps ("clone and `make test`
  passes" — not "set up environment"). Each carries an evidence tag. [DOC]
- Name a buddy (daily, unblocks) and a mentor (weekly, growth) — distinct roles. [INFERENCIA]

### Step 4: Validate
- Confirm a fresh machine can follow the guide end-to-end with zero tribal
  knowledge; every external claim is tagged and checkable. [DOC]

## Ramp-up metrics (defaults — confirm per team)
| Metric | Target window | Signal it measures |
|---|---|---|
| Env to green build | Day 1 | Setup friction [SUPUESTO] |
| First merged PR | Week 1 | Workflow fluency [SUPUESTO] |
| First on-call / solo feature | Week 4–6 | Independence [SUPUESTO] |

## Worked example (checklist row)
`- [ ] Run \`make bootstrap && make test\`; all suites green [CONFIG]` — verifiable,
single outcome, tagged. Contrast the vague "set up your environment" (untestable). [INFERENCIA]

## Quality Criteria
- [ ] Every setup step is reproducible on a clean machine from the doc alone [DOC]
- [ ] Each external/derived claim carries one Alfa-core tag (`[CÓDIGO]` `[CONFIG]` `[DOC]` `[INFERENCIA]` `[SUPUESTO]`) [DOC]
- [ ] Ramp metrics have explicit target windows, not just labels [DOC]
- [ ] Buddy and mentor are named with cadence and scope [INFERENCIA]
- [ ] Constitution-compliant; actionable, scannable output [DOC]

## Usage
- "/developer-onboarding" — Run the full developer onboarding workflow
- "developer onboarding on this project" — Apply to current repo context

## Assumptions & Limits
- Assumes read access to project artifacts (code, docs, CI/configs) [SUPUESTO]
- English output unless otherwise specified [SUPUESTO]
- Produces the onboarding *document*; does not provision accounts, hardware, or
  access — flag those as prerequisites, don't execute them [DOC]
- Does not replace a human mentor's judgment on growth and readiness [DOC]

## Edge Cases & Failure Modes
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request the repo/role before drafting [DOC] |
| Conflicting setup paths (README vs. CI) | Treat CI as source of truth; flag the drift [INFERENCIA] |
| Undocumented tribal step surfaces | Capture it into the guide as a new tagged step [DOC] |
| Out-of-scope (provisioning, HR) | Redirect to the owning team or escalate [DOC] |
| Stale instructions (build fails as written) | Stop, mark `[SUPUESTO]`, verify before publishing [DOC] |
