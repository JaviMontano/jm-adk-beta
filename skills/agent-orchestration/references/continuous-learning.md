<!-- distilled from alfa skills/continuous-learning -->
<!-- Extract reusable insights from Socratic debates and discoveries. Capture patterns -->
# Continuous Learning Loop

> "A project that doesn't learn from its own decisions is condemned to re-debate them."

## TL;DR

Implements Constitution XVII: every debate and discovery produces reusable insights captured in `insights/<domain>.md`. Before new debates, consult existing insights. When recurring ambiguity detected, propose constitution amendments. The project compounds knowledge — it never re-debates a settled class of decision. [EXPLICIT]

Use deterministic assets in `assets/` for insight taxonomy, evidence, duplicate handling, amendment gates, update plans, and report shape. When producing a JSON learning report, validate it offline with `bash skills/continuous-learning/scripts/check.sh`. [EXPLICIT]

## Scope & Anti-Scope

- IN: extracting reusable decision patterns from debates/discoveries; writing/indexing insights; detecting recurrence; proposing (not ratifying) amendments. [EXPLICIT]
- OUT: ratifying amendments (human/governance gate owns merge); making the original decision (that is `socratic-debate`); editing source code or configs as a side effect. [EXPLICIT]
- Precondition: a completed debate record or decision artifact exists. Absent one, stop — there is nothing to abstract. [INFERENCIA]

## Procedure

### Step 1: Discover
- Read the debate record; extract the three outputs: (1) direct answer, (2) refinements to the original question, (3) coverage gaps. Missing any → flag, do not fabricate. [EXPLICIT]
- Search `insights/<domain>.md` for the same class. Record the search (terms, files scanned) — an unrecorded search counts as not done. [EXPLICIT]
- Classify the find: new pattern, refinement of an existing insight, or duplicate (no write). [INFERENCIA]

### Step 2: Analyze
- Abstract the reusable pattern from the specific case: drop names/values, keep the decision shape and the condition that selects it. [EXPLICIT]
- Classify domain (one of): `universal`, `security`, `frontend`, `backend`, `testing`, `deployment`, `governance`. Default ambiguous cross-cutting patterns to `universal`. [SUPUESTO]
- Write trigger conditions as a matchable predicate (observable inputs/keywords/file-shapes), not a vibe — future agents pattern-match against it. [EXPLICIT]
- Map to the constitutional anchor (which principle the insight serves); if none fits, the insight is likely too narrow or signals an amendment gap. [INFERENCIA]
- Frequency check: same class seen 3+ times across distinct debates → amendment candidate. Count distinct debates, not restatements of one. [EXPLICIT]

### Step 3: Execute
- Write insight to `insights/<domain>.md` (all fields required; omit none):
  ```markdown
  ### Insight: {title}
  - **Origin**: Debate on {topic} ({date})
  - **Pattern**: {reusable decision pattern}
  - **Rationale**: {why this is the right default}
  - **Trigger**: {matchable condition to apply this insight}
  - **Constitutional Anchor**: Principle {N}
  - **Status**: active | tentative | superseded
  ```
- `tentative` = one occurrence / low confidence; `active` = validated/recurring; `superseded` = replaced — keep it, add `Superseded-by: {id}`, never delete (preserves the audit chain). [EXPLICIT]
- If 3+ distinct debates in same class → draft a constitution amendment in `.specify/adr/` citing the recurrence evidence (the debate ids). [EXPLICIT]
- Update `insights/README.md` index; cross-reference the debate record back to the insight (bidirectional link). [EXPLICIT]

### Step 4: Validate
- Insight abstracts beyond the original case; trigger is specific enough to match future queries without over-firing. [EXPLICIT]
- Constitutional anchor is correct; no duplicate exists (Step 1 search confirms). [EXPLICIT]
- A refinement updates the existing entry in place (does not spawn a near-duplicate). [INFERENCIA]
- If amendment proposed: rationale is strong, scope is bounded, recurrence evidence cited. [EXPLICIT]

## Quality Criteria

- [ ] Three outputs extracted from every debate (answer, refinements, gaps)
- [ ] Insight written to correct domain file
- [ ] Trigger conditions are actionable
- [ ] Constitutional anchor identified
- [ ] `insights/README.md` updated
- [ ] Frequency check performed (3+ → amendment)
- [ ] No duplicate insights
- [ ] Evidence tags applied
- [ ] Prior insight search recorded
- [ ] Amendment candidates include recurrence evidence
- [ ] JSON report passes `scripts/check.sh` when produced

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do This Instead |
|-------------|-------------|-----------------|
| Skipping insight extraction | Knowledge lost, same debates repeat | Extract after every significant decision |
| Over-specific insights | Can't apply to future cases | Abstract the pattern from the specifics |
| Over-broad insights | Trigger fires on everything → noise, agents ignore it | Constrain the trigger to observable conditions |
| Never amending constitution | Ambiguity keeps recurring | Amend when 3+ distinct debates hit same class |
| Not consulting insights before debate | Wasted effort re-debating | Always check `insights/` first |
| Deleting superseded insights | Audit chain broken, decisions un-traceable | Mark `superseded` + `Superseded-by`, keep the record |
| Auto-ratifying own amendments | Bypasses governance gate | Draft only; human/governance ratifies |

## Worked Example

Three separate debates settle "use parameterized queries / reject string-built SQL." Step 1 search finds no `security.md` entry → new pattern. Step 2: domain `security`, anchor = injection-safety principle, trigger = "any debate touching DB query construction with user-controlled input." Step 2 frequency: 3 distinct debates → amendment candidate. Step 3: write the insight (`Status: active`), draft `.specify/adr/NNNN-no-raw-sql.md` citing the three debate ids, update the index. Result: the fourth such question is answered by the insight in seconds, not re-debated. [EXPLICIT]

## Failure Modes

| Mode | Symptom | Recovery |
|------|---------|----------|
| Duplicate insight written | Two near-identical entries in one domain file | Merge into the stronger; mark the other `superseded` |
| Trigger never matches | Insight exists but agents keep re-debating | Re-derive trigger from the actual queries that should hit it |
| Wrong domain file | Insight unfindable where searched | Move entry; fix the `insights/README.md` index |
| Amendment drafted on 1–2 cases | Premature governance churn | Hold at `tentative` insight until 3rd distinct debate |
| `scripts/check.sh` fails on report | JSON shape/schema drift | Fix to the asset schema in `assets/`; re-validate before emit |

## Related Skills

- `socratic-debate` — Produces the debates that feed insights
- `integrity-chain-validation` — Insights improve chain compliance
- `repository-organization` — Insights files follow indexability rules (XVIII)

## Usage

Example invocations:

- "/continuous-learning" — Run the full continuous learning workflow
- "continuous learning on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| No debate record exists | Stop — nothing to abstract; do not invent a decision |
| Insight contradicts an existing `active` one | Open a debate to resolve; mark the loser `superseded` (never silently overwrite) |
| Pattern spans multiple domains | File in the most specific; cross-link from `universal` if broadly applicable |
| Recurrence at exactly 2 | Hold as `tentative`; no amendment until the 3rd distinct debate |
| Conflicting requirements in source debate | Flag conflicts explicitly; do not collapse into a single insight |
| Out-of-scope request | Redirect to `socratic-debate` (decide) or governance (ratify) |
