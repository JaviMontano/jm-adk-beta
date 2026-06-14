<!-- distilled from alfa skills/prototyping -->
<!-- > -->
# Prototyping
> "Method over hacks."
## TL;DR
Move from low-fi to high-fi deliberately: sketch → wireframe → clickable mockup → high-fi flow, raising fidelity only when the cheaper artifact has answered its question. Each rung tests one thing; skipping rungs hides which assumption broke. [EXPLICIT]

**Fidelity ladder** — pick the lowest rung that can falsify the current assumption: [INFERENCIA]

| Fidelity | Artifact | Answers | Cost to change |
|----------|----------|---------|----------------|
| Low | Paper / whiteboard sketch | Is the flow/concept right? | Minutes |
| Mid | Wireframe (greyscale) | Is the layout/IA right? | Hours |
| Mid-high | Clickable mockup (linked screens) | Does the path make sense? | Hours–day |
| High | High-fi interactive (real content, states) | Does it feel right; edge states? | Days |

Raise fidelity only after the lower rung passes; otherwise you polish a wrong concept. [INFERENCIA]

## Procedure
### Step 1: Discover
- Gather context, requirements, and the **one question** this prototype must answer. No question → no prototype. [EXPLICIT]
- Identify target fidelity from the ladder; default to the lowest that can answer the question. [INFERENCIA]
### Step 2: Analyze
- Evaluate options per Constitution XIII/XIV. [EXPLICIT]
- Choose tool by fidelity + handoff need (e.g. paper/Figma low-mid; Figma/code high). Trade-off: code prototypes test feel best but cost most to throw away — use only when interaction nuance is the open question. [SUPUESTO]
### Step 3: Execute
- Build the smallest artifact that answers the question; tag evidence inline. [EXPLICIT]
- Use realistic content, not lorem ipsum, once above wireframe — fake content hides length/overflow failures. [INFERENCIA]
- Model the unhappy paths (empty, error, loading), not just the happy flow. [INFERENCIA]
### Step 4: Validate
- Verify quality criteria met; test with ≥1 real user or proxy before raising fidelity. [EXPLICIT]
- Capture what the prototype falsified, then iterate or escalate fidelity. [INFERENCIA]

## Quality Criteria
- [ ] Evidence tags applied
- [ ] Constitution-compliant
- [ ] Actionable output
- [ ] Fidelity matches the question being tested (no gold-plating) [INFERENCIA]
- [ ] Unhappy/edge states represented, not only the happy path [INFERENCIA]
- [ ] Tested with a real user or proxy before declaring done [SUPUESTO]

## Usage

Example invocations:

- "/prototyping" — Run the full prototyping workflow
- "prototyping on this project" — Apply to current context

**Worked example.** Validating a checkout redesign: Step 1 question = "will users find the new express-pay button?". Lowest falsifying rung = clickable mockup (mid-high), not high-fi — visual polish is not the open question. Build 3 linked screens, test with 5 users, measure find-time. If they miss it, the concept failed cheaply; iterate the wireframe before any high-fi work. [INFERENCIA]

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- **Anti-scope:** not production code, not visual/brand design sign-off, not accessibility audit, not usability-test facilitation — prototypes feed those, they don't replace them. [SUPUESTO]
- A prototype proves desirability/usability, not feasibility or performance; load, security, and scale stay unanswered. [INFERENCIA]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| No testable question defined | Stop; return to Discover — a prototype without a question is decoration [INFERENCIA] |
| Stakeholder mistakes high-fi mockup for finished product | Label fidelity on the artifact; state explicitly it is non-production [SUPUESTO] |
| Pressure to skip to high-fi | Surface the unvalidated lower-rung assumption being carried forward [INFERENCIA] |
