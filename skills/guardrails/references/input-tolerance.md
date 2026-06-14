<!-- distilled from alfa skills/input-tolerance -->
<!-- Normalize imperfect input (typos, voice, dyslexia, multilingual, multimodal) into clean intent before any downstream skill runs. [EXPLICIT] -->
# Input Tolerance

> "Method over hacks. Evidence over assumption."

## TL;DR

Normalize imperfect input — typos, voice transcripts, dyslexic spelling, multilingual code-switching, multimodal fragments — into a clean, taggable intent before any downstream skill runs. Orchestration-layer skill used internally by Pristino and the adk-orchestrator; never client-facing. Full protocol in PRISTINO.md. [EXPLICIT]

**Anti-scope:** does not translate for delivery, does not auto-correct domain terms it cannot verify, does not decide the task — it only resolves *what was meant* so the next skill can decide *what to do*. [EXPLICIT]

## Procedure

### Step 1: Discover
- Gather raw input plus context (locale, modality, prior turns). [EXPLICIT]
- Load relevant indexes/config. Detect modality (text/voice/image-OCR) and language(s) — these drive normalization, not the user's stated intent. [INFERENCIA]

### Step 2: Analyze
- Evaluate candidate interpretations per Constitution XIII/XIV. [EXPLICIT]
- Score by relevance and confidence. Preserve the verbatim original alongside the normalized form — never discard source for downstream traceability. [INFERENCIA]
- Prefer the interpretation needing the fewest unverifiable corrections (Occam over cleverness): a literal-but-odd reading beats a fluent guess that invents intent. [INFERENCIA]

### Step 3: Execute
- Apply the selected normalization; tag every output with evidence markers. [EXPLICIT]
- Mark each correction's basis: corrected-from-context vs. assumed. Assumed corrections to proper nouns, numbers, or commands are surfaced, not silently applied. [EXPLICIT]

### Step 4: Validate
- Verify quality criteria below are met. [EXPLICIT]
- Confirm confidence >= 0.95. Below threshold → emit best read + flag, do not block. Only ambiguity that changes the *action* blocks. [INFERENCIA]

## Quality Criteria

- [ ] Evidence tags applied to every non-obvious correction [EXPLICIT]
- [ ] Constitution-compliant (XIII/XIV) [EXPLICIT]
- [ ] Confidence >= 0.95, else flagged not blocked [EXPLICIT]
- [ ] Original input preserved verbatim alongside normalized form [INFERENCIA]
- [ ] Actionable output: a single resolved intent, or an explicit clarification request [EXPLICIT]

## Failure Modes

| Failure | Symptom | Mitigation |
|---------|---------|------------|
| Over-correction | Fluent rewrite that invents intent the input never carried | Fewest-corrections rule; surface assumed proper-noun/number/command edits [INFERENCIA] |
| Silent language flip | Output drops a code-switched clause as "noise" | Treat every detected language as signal until proven filler [SUPUESTO] |
| OCR/voice garble passed through | Homophone or mis-segmented token reaches downstream skill | Flag low-confidence tokens; do not auto-fix unverifiable spans [INFERENCIA] |
| Premature blocking | Halts on cosmetic ambiguity that doesn't change the action | Block only when ambiguity changes the resolved action [EXPLICIT] |

## Worked Example

Input (voice, ES/EN mix): *"corre el lint en el repo de orquestador y... eh, también el de gardrails"*

Resolved: run lint on `adk-orchestrator` and `guardrails` repos. `gardrails`→`guardrails` [INFERENCIA, corrected-from-context]; filler "eh" dropped [EXPLICIT]; both languages retained as intent, not noise. Confidence 0.97 → proceed, no clarification. [INFERENCIA]

## Related Skills

- See PRISTINO.md for full orchestration protocol

## Usage

Example invocations:

- "/input-tolerance" — Run the full input tolerance workflow
- "input tolerance on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Tag family is the Alfa core set (`[EXPLICIT]`/`[INFERENCIA]`/`[SUPUESTO]`); never mix in operator `{...}` tags — this is kit-facing output [INFERENCIA]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Mixed-language input | Retain all languages as intent; normalize, do not strip |
| Unverifiable token (name, number, command) | Surface as assumed correction; never auto-apply silently |
| Confidence below 0.95 but action unambiguous | Emit best read with flag; proceed without blocking |
