<!-- distilled from alfa skills/user-research -->
<!-- > -->
# User Research

> "You are not your user." — UX Research Axiom

## TL;DR

Creates personas, empathy maps, and user journey maps from qualitative and quantitative research to ground product decisions in real user needs. Use this skill when starting a new product, redesigning an experience, or when the team is making assumptions about user behavior without evidence. [EXPLICIT]

**In scope:** persona synthesis, empathy maps, journey maps, opportunity framing. **Out of scope (anti-scope):** usability testing of a built UI (use `accessibility-design` / a usability skill), A/B test design, market sizing, requirement specs (hand off to `requirements-engineering`). [SUPUESTO]

## Procedure

### Step 1: Discover
- Define research objectives and the decisions each will inform — research that changes no decision is waste. [INFERENCIA]
- Identify user segments and recruit representative participants; aim for 5–8 interviews per segment, where new themes stop appearing (saturation). [DOC]
- Choose research methods: interviews, surveys, contextual inquiry, analytics review. Match method to question type — *why/how* → qualitative (interviews, inquiry); *how many/how often* → quantitative (surveys, analytics). [INFERENCIA]

### Step 2: Analyze
- Synthesize research data using affinity diagrams and thematic analysis; code transcripts, cluster codes into themes, name each theme from participant language.
- Build personas with demographics, goals, frustrations, and behavioral patterns — anchor on goals/behavior, not demographics, which rarely predict need. [INFERENCIA]
- Create empathy maps: what users Say, Think, Do, and Feel. Watch for Say-vs-Do gaps (stated vs observed) — the gap is itself a finding.
- Map user journeys with touchpoints, emotions, pain points, and opportunities.

### Step 3: Execute
- Document 2–4 primary personas with photo, bio, goals, and pain points. Cap at 4; more dilutes focus and signals weak segmentation. [INFERENCIA]
- Create empathy maps for each persona capturing emotional and behavioral insights.
- Build end-to-end user journey maps with stages, actions, and sentiment curves.
- Identify "moments of truth" — critical touchpoints that determine satisfaction.

### Step 4: Validate
- Verify personas are based on research data, not stereotypes; each persona attribute traces to a source (interview ID, survey item, analytics metric).
- Confirm journey maps include both positive and negative emotional states.
- Cross-check qualitative findings against quantitative analytics; reconcile, don't average — when they disagree, the disagreement is the insight. [INFERENCIA]
- Validate with stakeholders that personas represent target user segments.

## Worked Example

B2B invoicing redesign. Discover: objective = "why do users abandon at payment?"; 6 interviews + funnel analytics. Analyze: affinity clusters surface "unclear fees" and "no save-draft". Persona *Marta, AP clerk* — goal: close month-end fast; frustration: re-keying rejected invoices. Empathy map Say-vs-Do gap: says "I trust the system" but Does export to a spreadsheet to double-check. Journey moment-of-truth: the approval-submit step, sentiment dips from +2 to −3. Opportunity: inline fee preview + autosave. Validate: analytics confirm 38% drop at that exact step. [SUPUESTO]

## Quality Criteria

- [ ] Personas are research-backed with cited data sources
- [ ] Empathy maps capture all four quadrants (Say, Think, Do, Feel)
- [ ] User journeys cover the complete experience lifecycle
- [ ] Pain points are linked to specific improvement opportunities
- [ ] Each opportunity is owned and prioritized (not an orphan insight)
- [ ] Evidence tags applied to all claims

## Anti-Patterns & Failure Modes

- Personas based on assumptions rather than research data → demand a source per attribute.
- Journey maps that only show the happy path → require at least one negative-sentiment stage.
- Research theater: conducting research but ignoring findings → tie each finding to a decision in Step 1.
- Sample bias: recruiting only reachable/power users → state who was excluded and the risk. [INFERENCIA]
- Leading questions in interviews → review the guide for assumptions before fielding. [INFERENCIA]
- Persona sprawl (>4) or "elastic user" (a persona that conveniently wants everything) → re-segment. [INFERENCIA]

## Related Skills

- `requirements-engineering` — translates user needs into specifications
- `accessibility-design` — ensures inclusive design for all users
- `workshop-design` — facilitates collaborative research synthesis

## Usage

Example invocations:

- "/user-research" — Run the full user research workflow
- "user research on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Outputs are hypotheses to validate, not proof; qualitative findings do not generalize statistically without quantitative confirmation. [INFERENCIA]
- No access to live users by default — when primary data is absent, label personas *provisional* and propose the study that would confirm them. [SUPUESTO]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| No access to real users | Build provisional personas from proxies (support tickets, analytics, sales notes); mark `[SUPUESTO]` and name the validation study |
| Only quantitative data (no interviews) | Personas describe behavior, not motivation; flag the missing "why" as a gap |
| Findings contradict stakeholder belief | Present evidence neutrally; reconcile in a session, do not silently drop either side |
