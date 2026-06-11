---
name: kata
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

Router skill. Resolve `topic` from the request, then Read EXACTLY ONE playbook
from `routes:`. Never load the whole cluster. `depth=deep` → apply the playbook
exhaustively with verification at each step; `quick` → essentials only.

Spine: Discover → Analyze → Execute → Validate.
Quality gates: constitution v6.0.0 (enforcement), evidence tags, script-first rule.
