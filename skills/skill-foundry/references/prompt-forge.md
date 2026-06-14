<!-- distilled from alfa skills/prompt-forge -->
<!-- Create, review, evolve, repair, and port system prompts using a deterministic Playbook format, source-boundary rules, platform portability notes, rubric scorecards, adversarial test cases, and script-backed forge packet validation. Use when the user asks to create a system prompt, review a prompt, optimize or repair prompt behavior, port prompts across Claude, ChatGPT, Gemini, or API runtimes, or apply Prompt Forge / Playbook format. [EXPLICIT] -->
# Prompt Forge

Turn assistant ideas or existing prompts into structured, production-ready instruction packages. The skill works in five modes: create, review, evolve, repair, and port. Every mode produces a deterministic forge packet before delivery. [EXPLICIT]

**Scope boundary.** This skill engineers *runtime instruction artifacts* (system prompts, project/GPT/Gem instructions, API system messages). It does not write durable prompt files for an agent ecosystem (`prompt-creator`), author agents (`agent-creator`), or build full skills (`skill-creator`). When a request mixes concerns, do the Forge analysis first, then hand off the durable-file write. [INFERRED]

## When to Activate

Activate when the user requests any of the following: [EXPLICIT]

- Create a system prompt, project instruction, Custom GPT instruction, Gemini Gem instruction, or API system message. [EXPLICIT]
- Review, score, optimize, repair, or port an existing prompt. [EXPLICIT]
- Apply Prompt Forge, Playbook format, prompt rubric, prompt portability, prompt repair, or prompt deployment instructions. [EXPLICIT]
- Paste a prompt and ask whether it is good, why it fails, or how to improve it. [EXPLICIT]

Do not activate for reminders such as "prompt me tomorrow", conceptual Q&A such as "what is a system prompt?", or durable prompt-file generation that belongs to `prompt-creator` unless Prompt Forge analysis is explicitly requested first. [EXPLICIT]

**Anti-scope (out of bounds, redirect instead of forging):** raw prose copywriting with no instruction contract; one-off chat replies; tuning model hyperparameters (the model owner sets temperature, not this skill — Forge only *documents* the determinism intent); jailbreak or guardrail-evasion requests (refuse). [INFERRED]

## Required Inputs

Capture the minimum viable context before writing final output: [EXPLICIT]

- Mode: create, review, evolve, repair, or port. [EXPLICIT]
- Prompt goal and primary user outcome. [EXPLICIT]
- Target platform: `claude-project`, `custom-gpt`, `gemini-gem`, `api`, or `unknown`. [EXPLICIT]
- Source boundary: what facts, files, policies, or retrieved snippets the assistant may rely on. [EXPLICIT]
- Output contract: expected format, required fields, and refusal or coverage-gap behavior. [EXPLICIT]
- Constraints: safety, brand, tone, workflow, and tool boundaries. [EXPLICIT]

If input is incomplete, ask only the missing questions that affect the Playbook contract. Do not ask a broad interview before producing a useful draft or review. [EXPLICIT]

**Default when underspecified (do not block):** mode = review for a pasted prompt, else create; platform = `unknown` (write portable, flag platform-specific lines); source boundary = "model's own knowledge only, no invention"; output contract = the format the user's example implies, or prose if none. State each assumed default explicitly in the Source Boundary section so the user can correct it. [INFERRED]

**Only these gaps justify a blocking question** (they change the contract, not just the wording): unstated source boundary when the prompt is clearly RAG/tool-grounded; a machine-readable output contract whose exact field names you cannot infer; a safety/brand constraint the user implied but did not specify. Everything else: draft with a stated assumption. [INFERRED]

## Deterministic Contract

- Do not invent domain facts, platform limits, policies, citations, tools, or source material. [EXPLICIT]
- Treat current platform limits as unknown unless supplied by the user or cited from a dated source. Token windows, model names, and feature availability drift; never hard-code them into a generated prompt — reference them as a parameter the deployer fills. [EXPLICIT]
- Keep hidden reasoning private. Use concise rationale, decision trace, or checklist evidence instead of exposed reasoning transcripts. [EXPLICIT]
- Make every source-grounded prompt define unsupported-source behavior, usually `coverage_gap` or refusal. [EXPLICIT]
- Preserve machine-readable output contracts exactly when evolving or repairing prompts. A field rename, reorder, or type change is a breaking change — flag it and get confirmation before emitting. [EXPLICIT]
- For porting, state source platform, target platform, mapped features, unsupported features, and losses. [EXPLICIT]
- Run `scripts/validate_forge_packet.py` for JSON forge packets when producing or changing a structured artifact. [EXPLICIT]

**Conflict resolution order** when inputs collide: explicit user safety/brand constraint > preserved output contract > Playbook canonical structure > density/brevity preference. Never trade away a safety constraint for terseness. [INFERRED]

## Assets And Scripts

Use these local assets before drafting. Treat them as the source of truth; if a generated artifact disagrees with `playbook-contract.json`, the contract wins. [EXPLICIT]

- `assets/prompt-forge-checklist.md` - deterministic review checklist. [EXPLICIT]
- `assets/playbook-contract.json` - required Playbook sections, modes, platforms, rubric criteria, and test coverage. [EXPLICIT]
- `assets/platform-portability-matrix.json` - local platform mapping for Claude Project, Custom GPT, Gemini Gem, and API deployment. [EXPLICIT]
- `scripts/validate_forge_packet.py` - deterministic forge packet validator. Exit non-zero means do not deliver; fix and re-run rather than overriding. [INFERRED]

## Operation Modes

| Mode | Trigger | Deterministic Output |
|------|---------|----------------------|
| Create | "Create a prompt for...", "I need an assistant that..." | Full Playbook plus source boundary, output contract, rubric, tests, and risks. |
| Review | "Review this prompt", "Is this any good?" | Rubric scorecard, blockers, prioritized fixes, and validation gaps. |
| Evolve | "Make this better", "Optimize this prompt" | Before/after changes, preserved contracts, rubric delta, and regression tests. |
| Repair | "This is not working", "The AI keeps doing X" | Failure diagnosis, surgical fix, self-correction trigger, and adversarial test. |
| Port | "Convert this for Claude/GPT/Gemini/API" | Platform mapping, adapted prompt, unsupported features, losses, and validation checklist. |

Default pasted-prompt behavior is review mode unless the user explicitly asks to create, evolve, repair, or port. [EXPLICIT]

**Per-mode acceptance criteria** (a mode's output is done only when): [INFERRED]

- **Create** — every Playbook section present (or omission documented), rubric scored, all 3 test classes written, source boundary explicit. [INFERRED]
- **Review** — every rubric criterion scored, each score <8 has a named blocker and a concrete fix, validation gaps listed. A review with no actionable fix on a low score is incomplete. [INFERRED]
- **Evolve** — before/after diff is line-addressable, the original output contract is byte-preserved or its revision is justified, a regression test proves old behavior still holds. [INFERRED]
- **Repair** — diagnosis names the *observable* failure (not a guess), the fix is the smallest change that removes it, a Self-Correction Trigger and an adversarial test that previously failed are added. [INFERRED]
- **Port** — every source feature is mapped, dropped, or substituted with a named loss; an unsupported feature silently omitted is a defect. [INFERRED]

**Failure modes to self-check before delivery:** over-engineering (adding sections the use case does not need — non-conversational batch prompts may legitimately omit Interaction Flow); contract drift (silently changing field names in evolve/repair); platform leakage (baking a current token limit or model name into the artifact); refusal-gap (a source-grounded prompt with no coverage_gap behavior); rubric theater (scores with no evidence). [INFERRED]

## Playbook Format

Generated prompts use this canonical section set unless a non-conversational batch/API use case requires an explicitly documented omission. Omitting a section without documenting why is a defect, not a simplification. [EXPLICIT]

```markdown
# [Assistant Name] - v[X.Y]

## Role & Archetype
[Composite expert identity: domain + method + communication style]

## Objective
[What the user achieves]

## Parameters
- Platform:
- Source boundary:
- Output contract:
- Temperature or determinism note:

## Interaction Flow
### Phase 1: Discovery
### Phase 2: Execution
### Phase 3: Delivery

## Constraints
[Hard boundaries, including what the assistant must not do]

## Key Questions
[Only questions needed to complete the contract]

## Output Template
[Exact format with placeholders]

## Self-Correction Triggers
[Observable failure patterns and recovery actions]
```

## Evaluation Rubric

Score every generated or reviewed prompt on these criteria. Scores below 8 require a repair note.

| Criterion | Measures |
|---|---|
| Foundation | Clear archetype, objective, and constraints. |
| Accuracy | Claims, sources, and methods are supported. |
| Quality | Professional, precise, filler-free writing. |
| Density | High value per token without losing constraints. |
| Simplicity | Structure remains understandable. |
| Clarity | Instructions have one practical interpretation. |
| Precision | Boundaries are enforceable. |
| Depth | Edge cases and failure modes are handled. |
| Coherence | Sections reinforce each other. |
| Value | User receives a materially better prompt. |

Scores are 1–10. A criterion scores <8 when it has a concrete, nameable defect, not merely "could be better"; otherwise it is filler and must be cut. [INFERRED]

## Worked Example (Repair mode, abbreviated)

Input: "My support bot keeps inventing refund amounts." [EXPLICIT]

- **Diagnosis (observable):** prompt grants the bot a refund *goal* but no *source boundary* for dollar figures, so it fabricates. [INFERRED]
- **Surgical fix:** add to Constraints — "Quote refund amounts only from the `order.refund_eligible` field. If absent, respond `coverage_gap` and route to a human." [INFERRED]
- **Self-Correction Trigger:** "If about to state a dollar amount not present in the supplied order record, stop and emit coverage_gap." [INFERRED]
- **Adversarial test:** user asks "what's my refund?" with no order record attached → expected: coverage_gap + human handoff, never a number. [INFERRED]

This is the whole repair: one constraint, one trigger, one failing-then-passing test — not a rewrite. [INFERRED]

## Output Packet

When responding, include: [EXPLICIT]

1. Mode and activation decision. [EXPLICIT]
2. Source boundary and assumptions (including any defaults you assumed for unstated inputs). [EXPLICIT]
3. Playbook or scorecard. [EXPLICIT]
4. Rubric scores and required repairs. [EXPLICIT]
5. Test cases: happy path, edge case, adversarial. [EXPLICIT]
6. Platform notes when applicable. [EXPLICIT]
7. Validation result from checklist or script. [EXPLICIT]
8. Risks and coverage gaps. [EXPLICIT]

## Validation Gate

Before delivery, confirm: [EXPLICIT]

- Playbook sections match `assets/playbook-contract.json`. [EXPLICIT]
- Source boundary and unsupported-source behavior are explicit. [EXPLICIT]
- Constraints include no-invention and hidden-reasoning privacy. [EXPLICIT]
- Output contract is preserved or intentionally revised with rationale. [EXPLICIT]
- Rubric has all criteria and every score below 8 has a repair. [EXPLICIT]
- Test cases include happy path, edge case, and adversarial coverage. [EXPLICIT]
- Porting outputs document unsupported features and losses. [EXPLICIT]
- No remote assets, unstated current-platform claims, or hidden reasoning transcripts are included. [EXPLICIT]

If any line fails, the artifact is not deliverable — fix the gap, do not annotate it as a known issue and ship anyway. A single unchecked box blocks the packet. [INFERRED]

## References

- `assets/prompt-forge-checklist.md`
- `assets/playbook-contract.json`
- `assets/platform-portability-matrix.json`
- `references/design-principles.md`
- `references/evaluation-rubric.md`
- `references/playbook-template.md`
- `references/platform-guides.md`
- `references/context-engineering.md`
- `references/domain-knowledge.md`
