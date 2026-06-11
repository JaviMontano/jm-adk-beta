<!-- distilled from alfa skills/socratic-debate -->
<!-- > -->
# Socratic Debate

> "The unexamined decision is not worth implementing."

## TL;DR

Formal mechanism for resolving ambiguities that have divergent implementation consequences. Runs a structured thesis → antithesis → counter-evidence → synthesis cycle, examines each option against constitutional principles, eliminates by contradiction, and produces a single answer with full rationale. Records debates in `.specify/debates/` for auditability. Use when confidence < 0.95, requirements are ambiguous, or trade-offs have no obvious winner. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify the ambiguity: what exactly is unclear or contested?
- Classify type: requirements ambiguity, architecture trade-off, priority conflict, or implementation choice
- Gather context: read relevant specs, plans, ADRs, and code
- Identify which constitutional principles (I-XVI) are at stake

### Step 2: Analyze
- Frame the **thesis**: the proposed or default position
- Generate the **antithesis**: the strongest opposing position
- For each position, identify: supporting evidence, constitutional alignment, risk profile, implementation cost
- Search for counter-evidence via codebase analysis or WebSearch
- Map each option to affected constitutional principles (especially VII, XIV, XV)

### Step 3: Execute
- Run elimination by contradiction: which options violate constitutional principles?
- For surviving options, apply weighted scoring: constitutional alignment (40%), implementation simplicity (25%), evidence strength (20%), risk (15%)
- Produce **synthesis**: the surviving option with full rationale
- Update confidence score (must reach >= 0.95 to close the debate)
- Record debate in `.specify/debates/debate-YYYY-MM-DD-topic.md`:
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
- Synthesis resolves the original ambiguity completely
- Confidence >= 0.95 achieved
- All affected parties' concerns addressed or explicitly deprioritized with rationale
- Debate record is linked to the relevant ADR, plan, or spec
- No constitutional principle violated by the synthesis

## Quality Criteria

- [ ] Ambiguity clearly identified and scoped
- [ ] Both thesis and antithesis have evidence support
- [ ] Constitutional principles explicitly referenced
- [ ] Elimination by contradiction documented
- [ ] Synthesis achieves confidence >= 0.95
- [ ] Debate record stored in `.specify/debates/`
- [ ] Result integrated into downstream artifact (ADR, plan, spec)
- [ ] Evidence tags applied to all claims

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do This Instead |
|-------------|-------------|-----------------|
| Skipping the antithesis | Confirmation bias — you only validate your assumption | Always generate the strongest opposing position |
| Debating without evidence | Opinions are not decisions | Ground every position in code, config, or documentation |
| Closing at < 0.95 | Unresolved ambiguity propagates downstream | Keep debating or escalate to user |
| Not recording the debate | Future decisions lose context | Always write to `.specify/debates/` |
| Debating trivial choices | Overhead without value | Only debate when implementation consequences diverge |

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

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
