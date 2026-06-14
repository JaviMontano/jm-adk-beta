# Body of Knowledge — Agentic Engineering Katas

Domain knowledge for the `kata` router: the concepts, standards, and decision
rules that govern when and how to apply each of the 30 JM Labs katas. [DOC]

## 1. Core thesis

A "kata" is a distilled, certified pattern for one recurring failure mode in
Claude agent engineering. The skill is a HUB that routes to exactly one SPOKE
(playbook). The discipline is: read one recipe, apply it, validate against its
own criteria — never improvise from memory, because recipes drift and the file is
the source of truth. [DOC]

## 2. The six clusters

| Cluster | Katas | Governing idea |
|---|---|---|
| Loop & control | deterministic-agent-loop, validation-retry-feedback, human-handoff-protocol | Control lives in typed API fields + bounded budgets, not model prose. [CÓDIGO] |
| Tools & MCP | builtin-tool-selection, tool-description-quality, mcp-server-configuration, mcp-structured-errors | Tool descriptions are selection contracts; errors are typed; retry policy lives in the client. [DOC] |
| Extraction & review | defensive-structured-extraction, false-positive-criteria, fewshot-edge-calibration, headless-code-review, independent-reviewer-multipass, critical-self-correction, confidence-stratified-sampling | Force structure; measure accuracy/FP per-category; keep humans as final gate. [DOC] |
| Context & memory | context-dilution-mitigation, hierarchical-claude-memory, persistent-scratchpad, prefix-caching, session-resume-fork, provenance-preservation | Place critical rules at edges; curate durable state; no claim without source. [DOC] |
| Hooks & config | pretooluse-guardrails, posttooluse-normalization, path-conditional-rules, custom-commands-skills, plan-mode-exploration | Determinism belongs in hooks/policy, not the system prompt. [CONFIG] |
| Multi-agent | hub-and-spoke-isolation, multiagent-error-propagation, multipass-prompt-chaining, adaptive-investigation, message-batch-processing | Isolate context per subagent; distinguish access-failure from valid-empty. [DOC] |

## 3. Key concepts

- **Typed-field control.** Route the agent loop on `stop_reason` (`tool_use` vs
  `end_turn`), never on heuristic text like "done"/"task complete". Unhandled
  values `raise`; the loop is bounded by `max_iterations` → `BudgetExceeded`. [CÓDIGO]
- **Categorical criteria over adjectives.** "report only when comment claims X but
  code does Y" beats "report high-confidence findings". Measure FP rate per
  category; one toxic category erodes trust across all. [DOC]
- **Forced structure.** For extraction, use JSON Schema + forced `tool_choice`,
  enums with an escape valve, explicit nullable — never parse prose. [CÓDIGO]
- **Hub-and-spoke isolation.** Each subagent starts with empty context and its own
  model via `AgentDefinition` + the built-in Task tool. [CÓDIGO]
- **Edge placement.** Softmax attention dilutes the middle of long context; place
  critical rules at the start/end and compact when crossing ~50–60% context. [INFERENCIA]
- **Provenance.** No claim without a source; conflicts are flagged (`conflict: true`)
  and escalated, never averaged. [DOC]

## 4. Standards honored

- **Evidence tagging.** Alfa-core family only inside this kit: `[CÓDIGO]`,
  `[CONFIG]`, `[DOC]`, `[INFERENCIA]`, `[SUPUESTO]`. ES/EN spellings are aliases;
  pick one per document; never mix with the Jarvis operator family. [DOC]
- **Constitution v6.0.0.** Enforcement, evidence tags, and script-first execution
  are mandatory gates, not suggestions. [DOC]
- **Single-brand, no invented prices, no client PII** in any kata output. [DOC]

## 5. Decision rules (routing)

1. If the request names a failure mode that matches exactly one kata's "Por qué
   importa" → route there. [DOC]
2. If two katas plausibly fit (e.g. `false-positive-criteria` vs
   `confidence-stratified-sampling`): the former rewrites vague→categorical
   criteria; the latter calibrates against a labeled set with stratified sampling.
   Ask which problem the user has. [INFERENCIA]
3. If the request is about WHERE determinism lives (prompt vs hook) → `pretooluse-guardrails`
   or `posttooluse-normalization`, not an extraction kata. [DOC]
4. If no kata fits → say so; do not force the nearest match. [DOC]

## 6. Anti-patterns at the router level

- Loading several playbooks "to compare" — pick one; re-route if wrong. [DOC]
- Answering from memory of a pattern instead of reading its current playbook. [INFERENCIA]
- Emitting `quick` depth but skipping the validation gate. [DOC]
- Mixing tag families in one output. [DOC]
