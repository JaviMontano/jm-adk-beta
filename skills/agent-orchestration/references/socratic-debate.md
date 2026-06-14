<!-- distilled from alfa skills/socratic-debate -->
<!-- > -->
# Socratic Debate

> "The unexamined decision is not worth implementing."

## TL;DR

Formal mechanism for resolving ambiguities whose resolutions have *divergent* implementation consequences. Runs a structured thesis → antithesis → counter-evidence → synthesis cycle, scores each surviving option against constitutional principles, eliminates by contradiction, and emits a single answer with full rationale. Records debates in `.specify/debates/` for auditability. [EXPLICIT]

**Trigger when** (any): confidence < 0.95 on a decision; requirements ambiguous with no obvious reading; trade-offs with no dominant winner; two artifacts (spec/plan/ADR/code) imply contradictory choices. [EXPLICIT]
**Do NOT trigger when** (anti-scope): the choice is reversible and cheap to undo; only one option survives the constitution trivially; the disagreement is taste, not consequence; the answer is already fixed by an upstream ADR. Route those to a direct decision, not a debate. [INFERENCE]

## Procedure

### Step 1: Discover
- State the ambiguity in one sentence: what is unclear or contested, and what hinges on it. [EXPLICIT]
- Classify type: requirements ambiguity, architecture trade-off, priority conflict, or implementation choice. [EXPLICIT]
- Gather context: read relevant specs, plans, ADRs, code. [EXPLICIT]
- List the constitutional principles (I–XVI) at stake. If none, the decision likely does not warrant a debate — re-check the anti-scope. [INFERENCE]

### Step 2: Analyze
- Frame the **thesis**: the proposed or default position. [EXPLICIT]
- Generate the **antithesis**: the *strongest* opposing position — steel-man it, do not strawman. [EXPLICIT]
- For each: supporting evidence, constitutional alignment, risk profile, implementation cost. [EXPLICIT]
- Search for counter-evidence via codebase analysis or WebSearch; tag web findings with citation per `verification-tags.md`. [DOC]
- Map each option to affected principles (especially VII, XIV, XV). [EXPLICIT]
- **Cap options at 4.** More than four = the problem is under-decomposed; split it into sub-debates. [INFERENCE]

### Step 3: Execute
- **Elimination by contradiction**: drop any option that violates a constitutional principle. Record *which* principle and *why* — a silent drop is non-auditable. [EXPLICIT]
- For survivors, apply weighted scoring — constitutional alignment (40%), implementation simplicity (25%), evidence strength (20%), risk (15%). Score each axis 0–1, multiply by weight, sum. [EXPLICIT]
- **Tie rule** (scores within 0.05): the option with the lower *reversal cost* wins; if still tied, escalate to user — do not coin-flip. [INFERENCE]
- Produce **synthesis**: the winning option with rationale, including why each loser lost. [EXPLICIT]
- Update confidence (must reach >= 0.95 to close). [EXPLICIT]
- Record the debate in `.specify/debates/debate-YYYY-MM-DD-topic.md`:
  ```
  # Debate: {topic}
  Date: {date}
  Trigger: {what caused the debate}
  Thesis: {position A}
  Antithesis: {position B}
  Evidence: {findings}
  Constitutional Alignment: {principle mapping}
  Synthesis: {final answer}
  Confidence: {score}
  Integrated Into: {ADR-NNN / plan / spec reference}
  ```

### Step 4: Validate
- Synthesis resolves the original ambiguity completely (no residual "it depends"). [EXPLICIT]
- Confidence >= 0.95 achieved and justified, not asserted. [EXPLICIT]
- Every affected party's concern is addressed, or explicitly deprioritized with rationale. [EXPLICIT]
- Debate record is linked to the downstream ADR, plan, or spec. [EXPLICIT]
- No constitutional principle is violated by the synthesis. [EXPLICIT]

## Worked Example

**Topic:** sync vs async handler for the `notify` step.
**Thesis:** synchronous — simpler, principle XIV (simplicity) favors it.
**Antithesis:** async — principle VII (resilience) favors decoupling from a flaky downstream.
**Elimination:** neither violates the constitution; both survive. [EXPLICIT]
**Scoring** (align 0.40 / simplicity 0.25 / evidence 0.20 / risk 0.15):
- sync → 0.7·.40 + 1.0·.25 + 0.6·.20 + 0.4·.15 = **0.71**
- async → 0.9·.40 + 0.5·.25 + 0.8·.20 + 0.9·.15 = **0.78**
**Synthesis:** async (0.78 > 0.71); the resilience gain on a flaky dependency outweighs the simplicity cost. Confidence 0.96. → ADR-014. [EXPLICIT]

## Confidence Rubric

Confidence is the analyst's estimate that the synthesis survives new evidence — not a vote tally. [INFERENCE]

| Score | Meaning |
|---|---|
| >= 0.95 | Winner is robust; remaining doubt is cosmetic. **Close.** |
| 0.80–0.94 | Plausible winner, real residual risk. Gather one more piece of evidence or run one more antithesis round. |
| < 0.80 | No clear winner. Decompose, reframe, or escalate to user — do not force a close. |

## Quality Criteria

- [ ] Ambiguity scoped in one sentence; anti-scope checked (not a trivial/reversible choice). [EXPLICIT]
- [ ] Antithesis is steel-manned and evidence-backed, not a strawman. [EXPLICIT]
- [ ] Constitutional principles referenced by number; eliminations name the violated principle. [EXPLICIT]
- [ ] Weighted scores shown per surviving option (not just the winner). [EXPLICIT]
- [ ] Synthesis explains why each loser lost. [EXPLICIT]
- [ ] Confidence >= 0.95, justified against the rubric. [EXPLICIT]
- [ ] Debate record stored in `.specify/debates/` and linked into a downstream artifact. [EXPLICIT]
- [ ] One evidence-tag family used consistently throughout (per `verification-tags.md`). [DOC]

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do This Instead |
|-------------|-------------|-----------------|
| Skipping the antithesis | Confirmation bias — you only validate your assumption | Always steel-man the strongest opposing position |
| Strawman antithesis | A weak opponent rigs the score; the debate is theater | Argue the antithesis as if you held it |
| Debating without evidence | Opinions are not decisions | Ground every position in code, config, or docs |
| Closing at < 0.95 | Unresolved ambiguity propagates downstream | Keep debating, decompose, or escalate |
| Forcing a close on a true tie | Manufactures false confidence | Apply the tie rule (reversal cost), then escalate |
| Silent elimination | Auditor cannot see why an option died | Record the violated principle for every drop |
| Not recording the debate | Future decisions lose context | Always write to `.specify/debates/` |
| Debating trivial/reversible choices | Overhead without value | Decide directly; reserve debate for divergent consequences |
| Debate loop (rounds without new evidence) | Burns budget, never converges | After 2 evidence-free rounds, escalate — re-running rhetoric adds nothing |

## Failure Modes

| Mode | Symptom | Recovery |
|---|---|---|
| Deadlock | Scores oscillate across rounds | Freeze options; the tie rule decides, else escalate |
| Constitution gap | No principle speaks to the trade-off | Flag for an ADR that *adds* the missing principle; debate that meta-question first |
| Evidence vacuum | Neither side is checkable in-repo or via web | Mark `[SUPUESTO]`, propose the experiment that would settle it, defer the close |
| Scope creep | One debate spawns three sub-questions | Split into sub-debates; do not resolve them inline |

## Related Skills

- `trade-off-analysis` — Weighted decision matrices for architecture choices
- `scenario-analysis` — Multi-scenario comparison with scoring
- `requirements-engineering` — When the ambiguity is in requirements, not solutions
- `integrity-chain-validation` — Debates may reveal integrity chain gaps

## Usage

Example invocations:

- "/socratic-debate" — Run the full socratic debate workflow
- "socratic debate on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs). [EXPLICIT]
- Requires English-language output unless otherwise specified. [EXPLICIT]
- Does not replace domain-expert judgment for final, high-stakes decisions — it structures the reasoning, it does not own the call. [EXPLICIT]
- Scoring weights are a default, not a constant; a project may re-weight them in its constitution, but the four axes are fixed. [INFERENCE]
- Out of scope: irreversible/cheap-to-undo choices, taste disputes, and questions already settled by an upstream ADR. [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution, debate only the consequential fork |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Single surviving option after elimination | No scoring needed; record the eliminations as the rationale and close |
| User overrides the synthesis | Honor it; record the override and its stated reason in the debate file [EXPLICIT] |
