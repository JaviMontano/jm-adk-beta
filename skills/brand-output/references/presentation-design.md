<!-- distilled from alfa skills/presentation-design -->
# Presentation Design
> "Method over hacks."
## TL;DR
Slide-deck patterns + visual storytelling driven by the Minto pyramid: lead with the answer, group supporting arguments, end on the ask. One idea per slide; the title states the takeaway, the body proves it. [EXPLICIT]

## Scope & Anti-Scope
- IN: deck structure, slide-level layout, narrative flow, takeaway titles, evidence placement. [EXPLICIT]
- OUT: brand chrome/templating (see `brand-pptx`/`html-brand`), copywriting beyond titles, live facilitation. [EXPLICIT]
- Not a substitute for domain-expert judgment on the underlying decision. [EXPLICIT]

## Procedure
### Step 1: Discover
- Capture audience, decision being asked for, single governing message, time budget, channel (live vs. leave-behind). [EXPLICIT]
- A leave-behind needs self-explanatory titles; a live deck can lean on the speaker. [INFERENCIA]
### Step 2: Analyze (Minto)
- State the governing thought, then group 3–5 mutually-exclusive arguments under it; each argument becomes a section. [EXPLICIT]
- Choose order: deductive (problem→cause→solution) for skeptics, inductive (answer-first) for sponsors. [INFERENCIA]
### Step 3: Execute
- One idea per slide. Title = the takeaway sentence; body = the proof (chart, table, diagram). [EXPLICIT]
- Tag every data point with its evidence source so claims are traceable in the leave-behind. [EXPLICIT]
### Step 4: Validate
- Run the title-only test (below) and the Quality Criteria before delivery. [EXPLICIT]

## Worked Example (Minto)
Governing thought: "Adopt platform X in Q3." Supporting slides — (1) current cost is unsustainable, (2) X cuts it 40%, (3) migration is 6 weeks, (4) risk is bounded. Reading only the four titles tells the whole story. [INFERENCIA]

## Quality Criteria
- [ ] Title-only test: reading every title in sequence reconstructs the full argument. [EXPLICIT]
- [ ] One idea per slide — no slide carries two takeaways. [EXPLICIT]
- [ ] Each claim/number carries an evidence tag. [EXPLICIT]
- [ ] Governing thought appears on slide 1 and is restated in the close. [EXPLICIT]
- [ ] Actionable ask is explicit on the final slide. [EXPLICIT]

## Usage
Example invocations:
- "/presentation-design" — Run the full presentation design workflow
- "presentation design on this project" — Apply to current context

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs) for evidence. [EXPLICIT]
- English-language output unless otherwise specified. [EXPLICIT]
- Hands off final brand styling to the brand-output renderer; this skill stops at structure. [EXPLICIT]

## Edge Cases & Failure Modes
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding [EXPLICIT] |
| Conflicting requirements | Flag conflicts explicitly, propose resolution [EXPLICIT] |
| Out-of-scope request | Redirect to brand renderer or escalate [EXPLICIT] |
| No single governing thought | Force one before building slides; >1 message = >1 deck [INFERENCIA] |
| More than 5 top-level arguments | Re-group into MECE buckets; flat lists fail the pyramid [INFERENCIA] |
| Generic/label titles ("Overview") | Rewrite as takeaway sentences before validation [EXPLICIT] |
| Data without source | Block the slide until an evidence tag is attached [EXPLICIT] |
