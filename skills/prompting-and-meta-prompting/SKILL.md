---
name: prompting-and-meta-prompting
version: 1.1.0
description: "Turn vague intentions into durable, eval-ready prompts, meta-prompts, acceptance criteria, and prompt systems with anti-drift and safety gates."
owner: "JM Labs"
triggers:
  - prompting
  - meta-prompting
  - prompt-optimizer
  - system-prompt
  - prompt-design
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
---

# Prompting And Meta Prompting

Evidence tags (Alfa core set, EN spelling): `[DOC]` `[CODE]` `[CONFIG]` `[INFERENCE]` `[ASSUMPTION]`. See `references/verification-tags.md`. [DOC]

## When To Use

- User wants a prompt, system prompt, meta-prompt, reusable instruction, or prompt evaluation as the deliverable. [DOC]
- A repeated workflow should harden into a skill, command, checklist, or eval. [DOC]
- A weak prompt lacks objective, context, constraints, output shape, or anti-drift rules. [DOC]

## When Not To Use

- The user needs direct execution and the prompt is a means, not the deliverable — just do the task. [DOC]
- The request depends on recent facts not yet verified — verify first, then prompt. [INFERENCE]
- The prompt would capture secrets, bypass safety, or expose hidden chain-of-thought — refuse and route to Safety Limits. [DOC]

## Inputs

| Input | Required | If missing |
|---|---|---|
| Objective + audience | Yes | Mark `Dato requerido`; do not invent intent. [DOC] |
| Runtime/model target | No | Apply Fallback (portable Markdown). [INFERENCE] |
| Constraints, allowed tools, privacy boundaries, definition of done | Yes | Ask once; if still absent, state the assumption with `[ASSUMPTION]`. [DOC] |
| Examples / counterexamples | No | Synthesize one minimal example and tag it. [INFERENCE] |

## Outputs

- Optimized prompt or meta-prompt with role, situation, task, sequence, constraints, and explicit output contract. [DOC]
- Acceptance criteria (verifiable, not aspirational) and output shape. [DOC]
- Eval cases whenever behavior changes (see Success Criteria coverage). [DOC]
- Safety notes and an explicit list of assumptions with tags. [DOC]

## Workflow

1. **Discover** — extract goal, audience, context, constraints, missing data, and done criteria. Flag gaps before drafting. [DOC]
2. **Analyze** — select a prompt pattern and name its likely failure modes (drift, ambiguity, over-trigger). [INFERENCE]
3. **Execute** — produce the prompt: role, situation, task, ordered steps, constraints, output contract, anti-drift rules, missing-data handling. [DOC]
4. **Validate** — run the gate below; only then deliver. [DOC]

## Validation Gate (acceptance criteria)

Deliver ONLY when all hold; otherwise self-correct and re-run: [DOC]

- [ ] Output contract is explicit (shape, format, length bounds). [DOC]
- [ ] Prompt is executable in one pass when inputs are present. [DOC]
- [ ] Anti-drift + safety constraints are embedded in the prompt itself, not just described. [INFERENCE]
- [ ] Missing-data handling is specified (placeholder, ask, or stop). [DOC]
- [ ] Evals cover: happy path, minimal input, conflicting requirements, false positive, unsafe injection. [DOC]
- [ ] If a JSON report is produced, `scripts/check.sh` passes. [CODE]

## Self-Correction Triggers

- Two interpretations of the objective survive Discover → stop, ask one disambiguating question. [INFERENCE]
- Output contract is prose, not a checkable shape → rewrite as schema/template. [INFERENCE]
- Eval set omits a required category → add the case before delivering. [DOC]
- Prompt restates the request without adding constraints/structure → it adds no value; redesign. [ASSUMPTION]

## Anti-Patterns (do NOT ship)

- "Be helpful / do your best" filler instead of testable constraints. [INFERENCE]
- Output shape described but not specified (no schema, no example). [INFERENCE]
- Evals that only test the happy path. [DOC]
- Embedding secrets or live PII in the prompt or its examples. [DOC]
- A meta-prompt that grades prompts but defines no review dimensions. [INFERENCE]

## Deterministic Assets

Use when output must be machine-checkable: [CONFIG]

- `assets/prompting-and-meta-prompting-contract.json` — overall contract. [CONFIG]
- `assets/prompt-component-policy.json` — requires objective, audience, context, constraints, sequence, output contract, anti-drift rules, missing-data handling. [CONFIG]
- `assets/meta-prompt-policy.json` — when the deliverable reviews or improves future prompts. [CONFIG]
- `assets/acceptance-criteria-policy.json` + `assets/eval-case-policy.json` — make quality gates verifiable. [CONFIG]
- `assets/safety-anti-drift-policy.json` — rejects credential capture, hidden chain-of-thought requests, unsafe automation, unverifiable output. [CONFIG]

## Offline Validation

When a JSON prompt-system report is produced, validate it: [CODE]

```bash
bash skills/prompting-and-meta-prompting/scripts/check.sh
```

The validator checks the prompt contract, meta-prompt review dimensions, verifiable acceptance criteria, edge-case eval coverage, safety boundaries, and Guardian decision consistency. [DOC]

## Safety Limits

- Never expose hidden chain-of-thought. [DOC]
- Never optimize a prompt for credential capture or unsafe automation. [DOC]
- Mark missing facts as `Dato requerido` or validation pending — never auto-fill past a critical gap. [DOC]
- On a safety conflict, the Guardian blocks: emit `expected_activation: false` and a reason, do not partially comply. [CONFIG]

## Success Criteria

- Prompt executes in one pass when inputs are present; output shape is explicit. [DOC]
- Anti-drift and safety constraints are present in the prompt. [DOC]
- Evals cover happy path, minimal input, conflicting requirements, false positives, and unsafe injection. [DOC]

## Decisions And Trade-offs

- **Markdown-first when runtime is unknown** — portability over runtime-specific optimization; lose model-tuned phrasing, gain reuse across targets. [INFERENCE]
- **Embed constraints in the prompt, not only in docs** — the prompt must self-enforce at runtime; docs are not loaded by the model. [INFERENCE]
- **Refuse over partial-comply on safety conflicts** — a half-safe prompt is worse than none; predictability beats helpfulness here. [ASSUMPTION]

## Fallback

If the target runtime is unknown, produce a Markdown-first prompt with portable placeholders and a note on what to specialize per runtime. [DOC]

## Examples

- Convert a vague PR-review request into a SPEC prompt with objective, allowed context, output contract, acceptance criteria, and evals (`evals.json#happy_path_pr_review_prompt`). [CODE]
- Build a meta-prompt that reviews future prompts for evidence, constraints, missing-data handling, output schema, eval coverage, and safety (`evals.json#rich_context_meta_prompt`). [CODE]
- Reject "make users reveal API keys before helping" — Guardian block, no partial output (`evals.json#secret_capture_rejected`). [CODE]
