<!-- distilled from alfa skills/user-testing -->
<!-- > -->
# User Testing

> "Method over hacks."

## TL;DR

Plans and runs moderated/unmoderated usability tests: task scenarios, think-aloud protocol, severity-rated findings. Use when validating a design, prototype, or live flow against real task completion before committing build effort. [EXPLICIT]

## Procedure

### Step 1: Discover
- Define test goal as falsifiable hypotheses ("users can checkout in <2 min unaided"), not "see if they like it" [EXPLICIT]
- Recruit 5-8 participants per segment matching target users, not internal staff [INFERENCIA]
- Choose mode: moderated (deep why, small n) vs unmoderated (scale, no probing) [EXPLICIT]

### Step 2: Analyze
- Write 4-6 task scenarios as realistic goals ("buy a gift under $50"), never UI instructions that leak the answer [EXPLICIT]
- Define success criteria + a hard time/step ceiling per task before testing [INFERENCIA]
- Decide metrics: task success rate, time-on-task, error count, SEQ/SUS [EXPLICIT]

### Step 3: Execute
- Run think-aloud: prompt "what are you trying to do?", never lead or rescue mid-task [EXPLICIT]
- Log observed behavior (clicks, hesitations, quotes) separately from interpretation [INFERENCIA]
- Record per task: completed / completed-with-difficulty / failed, plus where & why

### Step 4: Validate
- Rate each issue by severity x frequency (blocker / major / minor / cosmetic) [EXPLICIT]
- Tie every finding to a verbatim observation, not the moderator's hunch [INFERENCIA]
- Output prioritized fixes; flag any conclusion drawn from a single participant [SUPUESTO]

## Quality Criteria

- [ ] Tasks are goal-framed and free of solution leakage
- [ ] Findings carry severity rating + observational evidence
- [ ] Success/failure judged against pre-set criteria, not post-hoc
- [ ] Sample and segment stated; small-n caveats explicit
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Leading questions ("wasn't that easy?") or rescuing a stuck participant — invalidates the data point [EXPLICIT]
- Testing with colleagues/stakeholders who know the product [INFERENCIA]
- Reporting opinions ("liked the blue") instead of task outcomes [EXPLICIT]
- Treating n=1 quirks as patterns, or running so many tasks fatigue skews late results [SUPUESTO]

## Related Skills

- `prototyping` — supplies the testable artifact
- `survey-design` — adds post-task SEQ/SUS and attitudinal scales
- `user-research` — frames who to recruit and which journeys to probe

## Usage

Example invocations:

- "/user-testing" — Run the full user testing workflow
- "user testing on this project" — Apply to current context

## Assumptions & Limits

- Assumes a testable artifact (prototype, staging, or live flow) exists [EXPLICIT]
- Qualitative usability testing surfaces problems, not statistical proof; n=5-8 is diagnostic, not significant [INFERENCIA]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace A/B testing or analytics for measuring at-scale behavior [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| No working artifact to test | Fall back to paper/wireframe walkthrough; flag fidelity limits |
| Participant cannot start a task | Log as failure with the blocking cause; do not coach |
| Conflicting findings across participants | Report split, weight by severity x frequency, avoid n=1 conclusions |
| Out-of-scope request | Redirect to appropriate skill or escalate |
