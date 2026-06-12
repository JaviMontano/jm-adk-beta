<!-- distilled from alfa skills/okr-design -->
<!-- > -->
# Okr Design
> "Method over hacks."
## TL;DR
Design OKRs: one qualitative Objective + 2–5 measurable Key Results, cascade alignment top-down, score 0.0–1.0, review on cadence. [EXPLICIT]

## Procedure
### Step 1: Discover
- Gather strategy, time horizon (quarter/year), owning team, and parent OKR to align under. [EXPLICIT]
- Confirm baseline + target per metric; an unmeasurable KR is a task, not a KR. [INFERENCIA]
### Step 2: Analyze
- Draft Objective: directional, inspirational, no number. Draft KRs: outcome metrics (not activities), each with baseline→target. Evaluate per Constitution XIII/XIV. [EXPLICIT]
- Separate committed KRs (must hit, score ~1.0) from aspirational/stretch (target ~0.7 = success). [INFERENCIA]
### Step 3: Execute
- Write final set with owner, baseline, target, due date, and parent link; tag each claim. [EXPLICIT]
### Step 4: Validate
- Run Quality Criteria; verify horizontal alignment (no conflicting KRs across teams) and vertical traceability to parent. [INFERENCIA]

## Scoring & Cadence
- Score = (current − baseline) / (target − baseline), clamped 0.0–1.0; Objective score = mean of its KR scores. [INFERENCIA]
- Stretch OKR healthy band: 0.6–0.7. Consistently 1.0 ⇒ targets too soft; consistently <0.3 ⇒ too aggressive or under-resourced. [INFERENCIA]
- Cadence: weekly check-in (confidence + blockers), end-of-cycle grade + retro. Grading is for learning, never for compensation. [EXPLICIT]

## Quality Criteria
- [ ] Objective is qualitative, time-bound, no embedded metric
- [ ] 2–5 KRs, each an outcome with explicit baseline → target → due date
- [ ] Each KR has a single named owner
- [ ] Vertical alignment: links to a parent objective (or stated as top-level)
- [ ] No KR restates an activity/task ("ship X") instead of an outcome ("X drives Y")
- [ ] Evidence tags applied; Constitution-compliant; actionable output

## Worked Example
- **Objective:** Make onboarding a competitive advantage this quarter. [EXPLICIT]
- **KR1:** Activation rate 42% → 60% (owner: PM). **KR2:** Time-to-first-value 3d → 1d (owner: Eng). **KR3:** Onboarding NPS 25 → 40 (owner: CS). [EXPLICIT]
- End-of-quarter: KR scores 0.7 / 0.5 / 0.9 ⇒ Objective 0.70 (healthy stretch). [INFERENCIA]

## Usage
Example invocations:
- "/okr-design" — Run the full okr design workflow
- "okr design on this project" — Apply to current context

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs) and the parent/company strategy to cascade under. [EXPLICIT]
- English-language output unless otherwise specified. [EXPLICIT]
- Does not replace domain expert judgment for final target-setting. [EXPLICIT]
- Anti-scope: not for task/sprint planning (use a backlog), not a KPI dashboard (KPIs are health metrics; OKRs are change goals), not a performance-review instrument. [INFERENCIA]

## Edge Cases
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| KR has no baseline | Block; set a measurement period to establish baseline before committing a target |
| More than 5 KRs proposed | Force-rank, keep top 3–5; the rest become tasks or next-cycle candidates |
| KR is binary (done/not-done) | Allow only for committed KRs; prefer a graded metric for stretch |
| No parent objective exists | Treat as top-level; record rationale so children can later align upward |
| Sandbagged targets (all scoring 1.0) | Flag in retro; raise next-cycle ambition |
