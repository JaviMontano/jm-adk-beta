---
name: kata
version: 1.0.0
description: "Agentic engineering katas: proven prompt/loop/tooling patterns from JM Labs. Topics: adaptive-investigation, builtin-tool-selection, confidence-stratified-sampling, context-dilution-mitigation, critical-self-correction, custom-commands-skills, defensive-structured-extraction, deterministic-agent-loop, false-positive-criteria, fewshot-edge-calibration, headless-code-review, hierarchical-claude-memory, hub-and-spoke-isolation, human-handoff-protocol, independent-reviewer-multipass, mcp-server-configuration, mcp-structured-errors, message-batch-processing, multiagent-error-propagation, multipass-prompt-chaining, path-conditional-rules, persistent-scratchpad, plan-mode-exploration, posttooluse-normalization, prefix-caching, pretooluse-guardrails, provenance-preservation, session-resume-fork, tool-description-quality, validation-retry-feedback."
params:
  topic:
    enum: [adaptive-investigation, builtin-tool-selection, confidence-stratified-sampling, context-dilution-mitigation, critical-self-correction, custom-commands-skills, defensive-structured-extraction, deterministic-agent-loop, false-positive-criteria, fewshot-edge-calibration, headless-code-review, hierarchical-claude-memory, hub-and-spoke-isolation, human-handoff-protocol, independent-reviewer-multipass, mcp-server-configuration, mcp-structured-errors, message-batch-processing, multiagent-error-propagation, multipass-prompt-chaining, path-conditional-rules, persistent-scratchpad, plan-mode-exploration, posttooluse-normalization, prefix-caching, pretooluse-guardrails, provenance-preservation, session-resume-fork, tool-description-quality, validation-retry-feedback]
    required: true
    infer: from user request; ask only if ambiguous
  depth:
    enum: [quick, deep]
    default: quick
routes:
  adaptive-investigation: references/adaptive-investigation.md
  builtin-tool-selection: references/builtin-tool-selection.md
  confidence-stratified-sampling: references/confidence-stratified-sampling.md
  context-dilution-mitigation: references/context-dilution-mitigation.md
  critical-self-correction: references/critical-self-correction.md
  custom-commands-skills: references/custom-commands-skills.md
  defensive-structured-extraction: references/defensive-structured-extraction.md
  deterministic-agent-loop: references/deterministic-agent-loop.md
  false-positive-criteria: references/false-positive-criteria.md
  fewshot-edge-calibration: references/fewshot-edge-calibration.md
  headless-code-review: references/headless-code-review.md
  hierarchical-claude-memory: references/hierarchical-claude-memory.md
  hub-and-spoke-isolation: references/hub-and-spoke-isolation.md
  human-handoff-protocol: references/human-handoff-protocol.md
  independent-reviewer-multipass: references/independent-reviewer-multipass.md
  mcp-server-configuration: references/mcp-server-configuration.md
  mcp-structured-errors: references/mcp-structured-errors.md
  message-batch-processing: references/message-batch-processing.md
  multiagent-error-propagation: references/multiagent-error-propagation.md
  multipass-prompt-chaining: references/multipass-prompt-chaining.md
  path-conditional-rules: references/path-conditional-rules.md
  persistent-scratchpad: references/persistent-scratchpad.md
  plan-mode-exploration: references/plan-mode-exploration.md
  posttooluse-normalization: references/posttooluse-normalization.md
  prefix-caching: references/prefix-caching.md
  pretooluse-guardrails: references/pretooluse-guardrails.md
  provenance-preservation: references/provenance-preservation.md
  session-resume-fork: references/session-resume-fork.md
  tool-description-quality: references/tool-description-quality.md
  validation-retry-feedback: references/validation-retry-feedback.md
---

# kata

Router skill: one entry, 30 agentic-engineering playbooks. Resolve `topic`, Read
EXACTLY ONE playbook from `routes:`, apply it. [DOC]

## When to use

Trigger when the request maps to a known agentic pattern — building a Claude
agent loop, MCP server, hook, structured extraction, code-review harness, memory
hierarchy, multi-agent topology, or prompt/sampling/context tactic — and you want
the proven JM Labs recipe instead of improvising. [INFERENCIA]
Do NOT use as a generic chat or to answer questions that no playbook covers; if
no `topic` fits, say so and route the user elsewhere rather than guessing. [DOC]

## Inputs

- `topic` (required): one of the 30 `routes:` keys. Infer from the request; ask
  only when two topics are genuinely plausible. [DOC]
- `depth` (default `quick`): `quick` → essentials + the validation gate only;
  `deep` → apply exhaustively, verifying at each step. [DOC]

## Procedure

1. Map request → `topic`. If ambiguous, present the 2 closest keys and ask. [DOC]
2. Read EXACTLY ONE playbook (its `routes:` path). Never load the whole
   cluster — that dilutes context and defeats hub-and-spoke isolation. [INFERENCIA]
3. Execute along the spine: Discover → Analyze → Execute → Validate. [DOC]
4. Apply the playbook's own acceptance criteria before declaring done. [DOC]

## Validation gate (acceptance)

- Exactly one playbook was read; topic matches the user's actual intent. [DOC]
- Output follows the chosen playbook's structure, not improvised prose. [DOC]
- Every non-obvious claim carries an evidence tag from the kit (Alfa/bracket)
  family per `../../references/verification-tags.md` — never mix tag families. [DOC]
- Constitution v6.0.0 gates honored: enforcement, evidence tags, script-first
  (prefer a script over manual steps when one exists). [DOC]
- Score the result with `assets/quality-rubric.json` and run `assets/routing-checklist.md`
  before declaring done (see `assets/README.md`). [DOC]

## Anti-patterns

- Loading several playbooks "to compare" — pick one; re-route if wrong. [DOC]
- Guessing a `topic` silently when the request is ambiguous. [DOC]
- Answering from memory of a pattern instead of reading its current
  playbook — recipes drift; the file is the source of truth. [INFERENCIA]
- Emitting `quick` depth but skipping the validation gate. [DOC]

## Self-correction

If mid-task the evidence contradicts the chosen topic (wrong failure mode, the
playbook's preconditions don't hold), STOP, name the mismatch, and re-resolve
`topic` — do not force-fit the original playbook. [INFERENCIA]
