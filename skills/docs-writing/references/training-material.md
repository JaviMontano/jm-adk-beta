<!-- distilled from alfa skills/training-material -->
<!-- > -->
# Training Material
> "Method over hacks."
## TL;DR
Design course-ready training: learning objectives, exercises, assessments, facilitator guide, learner handouts. [EXPLICIT]

## Scope
- In: objective design, exercise/lab authoring, assessment + rubric, facilitator script, handouts, timing plan. [EXPLICIT]
- Out (anti-scope): video production, LMS deployment/SCORM packaging, live delivery, translation, accreditation sign-off. [EXPLICIT]

## Procedure
### Step 1: Discover
- Gather audience, prior knowledge, delivery mode (self-paced vs. instructor-led), duration, success metric. [EXPLICIT]
### Step 2: Analyze
- Set objectives as observable verbs (Bloom: apply/analyze/create, not "understand"). Evaluate options per Constitution XIII/XIV. [INFERRED]
### Step 3: Execute
- Author each module: objective -> teach -> worked example -> practice exercise -> check. Tag every claim with evidence. [EXPLICIT]
### Step 4: Validate
- Verify quality criteria; dry-run timing; confirm each assessment item maps to an objective. [EXPLICIT]

## Quality Criteria
- [ ] Evidence tags applied [EXPLICIT]
- [ ] Constitution-compliant [EXPLICIT]
- [ ] Actionable output [EXPLICIT]
- [ ] Every objective has >=1 exercise and >=1 assessment item (no orphans) [INFERRED]
- [ ] Timing plan sums to stated duration +/-10% [INFERRED]
- [ ] Facilitator guide includes answer key + common-mistake notes [INFERRED]

## Acceptance Criteria
- A facilitator unfamiliar with the topic can run the session from the guide alone. [INFERRED]
- A learner can self-check via the assessment without instructor access. [INFERRED]
- Removing any handout breaks a referenced step (no dead handouts). [INFERRED]

## Decisions & Trade-offs
- Objective-first authoring over content-first: prevents scope creep and orphan content; costs more upfront design time. [INFERRED]
- Worked example before practice: faster novice ramp; risks rote copying — mitigate with a varied practice variant. [INFERRED]
- Instructor-led default unless input states self-paced: richer feedback loop; lower scale. State the assumption explicitly. [INFERRED]

## Worked Example
Topic "Git rebase basics", 60 min, instructor-led, dev audience. [EXPLICIT]
- Objective: "Learner can rebase a feature branch onto main and resolve one conflict." [EXPLICIT]
- Teach (10m) -> worked demo (10m) -> paired lab w/ seeded conflict (25m) -> assessment: rebase a fresh branch unaided (10m) -> debrief (5m). [EXPLICIT]
- Handout: conflict-resolution cheatsheet, referenced in the lab step. [EXPLICIT]

## Usage
Example invocations:
- "/training-material" — Run the full training material workflow
- "training material on this project" — Apply to current context

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Does not validate content accuracy against a live system — author must verify technical claims [INFERRED]

## Edge Cases & Failure Modes
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Mixed-skill audience | Split into tracks or add prerequisite pre-work; state the assumption [INFERRED] |
| Duration too short for objectives | Cut objectives, not depth; flag the trade-off to requester [INFERRED] |
| No success metric given | Propose a default assessment threshold and confirm before authoring [INFERRED] |
| Objective without assessment item | Block validation; author the missing check or drop the objective [INFERRED] |
