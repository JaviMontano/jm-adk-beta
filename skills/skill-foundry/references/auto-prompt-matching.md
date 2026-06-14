<!-- distilled from alfa skills/auto-prompt-matching -->
<!-- > -->
# Auto Prompt Matching

> "Method over hacks. Evidence over assumption."

## TL;DR

Routes user input to the best available skill or prompt using deterministic evidence from `PRISTINO-INDEX.md`, `.agent/skills_index.json`, skill frontmatter, prompt metadata, and explicit user prefixes. Use for orchestration-layer prompt routing, **not** for executing the routed task. Never invent a skill, prompt, confidence score, or capability absent from the inspected sources. [DOC]

**In scope:** select among indexed skills/prompts; emit a routing decision object. **Out of scope (anti-scope):** running the routed skill, summarizing the corpus, ranking skills not present in any index, or scoring confidence from memory. [DOC]

**Confidence bands** (thresholds live in `assets/routing-checklist.md`): `route` = one candidate clears the threshold and beats the runner-up by the tie-break margin; `ask` = top candidates within margin, or evidence partial; `decline` = no candidate clears the floor or request is out-of-corpus. Default on ambiguity is `ask`, never a forced `route`. [CONFIG]

## Procedure

### Step 1: Discover
- Capture the raw user request, explicit prefixes, mentioned brand/context, requested artifact type, language, and safety constraints.
- Load the smallest sufficient routing sources in this order: explicit prefix/command, `PRISTINO-INDEX.md`, `.agent/skills_index.json`, matching `skills/*/SKILL.md`, and relevant prompt metadata.
- Normalize tokens deterministically: lowercase, strip punctuation, split hyphenated slugs, preserve quoted terms, and keep brand names as exact terms.
- Build a candidate list only from discovered skills/prompts. Mark missing indexes as `coverage_gap`; do not replace them with memory.

### Step 2: Analyze
- Score candidates with the stable rubric in `assets/routing-checklist.md`: explicit trigger, slug/name match, purpose match, artifact type, context/brand fit, negative-scope penalties, and source freshness.
- Keep the top three candidates with evidence for each score component.
- Apply stable tie-breakers: explicit prefix wins; then exact trigger; then exact slug/name; then stronger purpose evidence; then narrower scope; then alphabetical slug for reproducibility.
- Classify confidence as `route`, `ask`, or `decline` using the checklist thresholds. Do not force a route when the evidence is ambiguous.

### Step 3: Execute
- Return a routing decision, not the downstream task result.
- Include selected skill/prompt, confidence band, score components, sources inspected, rejected alternatives, and required next action.
- If no candidate is reliable, ask a targeted clarification or hand off to discovery/orchestration instead of guessing.
- Use evidence tags on all claims (Alfa core set, per `references/verification-tags.md`): `[CÓDIGO]` inspected repo/index evidence, `[CONFIG]` routing policy/threshold, `[INFERENCIA]` derived fit, `[SUPUESTO]` user-accepted default. One tag per claim; never mix the Jarvis `{...}` family here. [CONFIG]

### Step 4: Validate
- Selected route exists in an inspected index or the file tree (not memory). [CÓDIGO]
- Every confidence/tie-break claim cites the score component that drives it.
- Known false positives are rejected: weather, generic prose, unsupported plugin claims, or any request outside the indexed corpus.
- `assets/routing-checklist.md` was applied before finalizing.

## Worked Example

Input: `"build a deterministic XLSX template"` (no prefix). Discover → `PRISTINO-INDEX.md` lists `xlsx-template-creator` (slug + purpose match) and `xlsx-author` (purpose-only). Analyze → checklist scores: `xlsx-template-creator` wins on slug + purpose + "deterministic" trigger; `xlsx-author` loses on narrower-scope tie-break. Decision: `route` → `xlsx-template-creator`, rejected `[xlsx-author: weaker purpose evidence]`, sources `[PRISTINO-INDEX.md]`. [INFERENCIA] Counter-case: same words but index missing both slugs → emit `coverage_gap` + `ask`, never guess a third skill. [CONFIG]

## Acceptance Criteria

- [ ] Output is a routing decision object (skill/prompt, band, score components, sources, rejected alternatives, next action) — not the downstream result.
- [ ] Every routing claim carries exactly one Alfa-core tag; sources listed by path or index name.
- [ ] Candidate set contains only discovered skills/prompts; missing indexes surface as `coverage_gap`.
- [ ] Score components and tie-breakers are visible and reproducible (same input → same route).
- [ ] Ambiguous → `ask` with one narrow clarification; unsupported → `decline`/handoff with zero invented capabilities.
- [ ] Final decision references `assets/routing-checklist.md`.

## Failure Modes

| Failure | Symptom | Guard |
|---------|---------|-------|
| Hallucinated skill | Route names a slug absent from every index | Step 4 existence check; fail closed to `decline` [CÓDIGO] |
| Forced route | `route` emitted with sub-threshold or tied scores | Default to `ask`; band thresholds in checklist [CONFIG] |
| Stale index | Route points to a removed/renamed skill | Treat missing slug as `coverage_gap`; inspect direct files [INFERENCIA] |
| Scope creep | Skill executed instead of routed | Anti-scope: emit decision only unless user asks to run it |
| Tag drift | Foreign `{...}` tags or untagged claims | Single-family Alfa-core tags; one per claim [CONFIG] |

## Related Skills

- `input-analyst` - normalize messy user input before routing
- `workflow-orchestration` - plan resumable multi-step execution after routing
- `subagent-orchestration` - isolate candidate reviewers when routing risk is high
- `output-contract-enforcer` - enforce downstream deliverable shape after routing

## Usage

Example invocations:

- "/auto-prompt-matching" - Run the full routing workflow
- "Which skill should handle this prompt: build a deterministic XLSX template?"
- "Route this user request to the right prompt without executing it."


## Assumptions & Limits

- Assumes read access to project artifacts (code, docs, configs); if none load, the only valid outputs are `coverage_gap` + `ask`. [DOC]
- Uses the language of the user request unless repo conventions require otherwise. [DOC]
- Does not replace domain-expert judgment for final decisions. [DOC]
- Does not execute the routed skill unless the user explicitly asks for execution after routing. [DOC]
- Does not use memory or unstated plugin knowledge as a source of truth when indexes are unavailable. [DOC]
- Trade-off: deterministic, index-only routing can miss a capability that exists but is unindexed — accepted, because a reproducible `coverage_gap` is safer than a confident wrong route. [INFERENCIA]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Ask for the task goal and artifact type before routing |
| Explicit prefix names a valid skill | Route to that skill and still report source evidence |
| Multiple high-confidence matches | Apply tie-breakers; if still tied, ask one narrow clarification |
| Source index missing or stale | Report `coverage_gap` and inspect direct skill files where possible |
| Unsupported capability | Decline or hand off; do not invent a skill |
| Out-of-scope request | Redirect to discovery/orchestration or ask for scope |
| Prefix names a non-existent skill | `decline` with the prefix echoed; do not silently substitute a near-match |
| Conflicting prefix vs. body intent | Prefix wins (it is explicit); note the conflict in the decision for the coordinator |
| Mixed-language request | Route in the request's dominant language; keep brand/slug terms verbatim |

## Assets

- `assets/routing-checklist.md` defines the scoring, tie-break, and final decision checklist.
