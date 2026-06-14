# Prompt — Meta (routing & self-check)

Use this to reason ABOUT the routing decision before applying any kata.

## Disambiguation pairs (ask, don't guess)

- `false-positive-criteria` vs `confidence-stratified-sampling`: the first rewrites
  vague→categorical review criteria; the second calibrates classifier accuracy
  against a labeled set with stratified sampling. [DOC]
- `pretooluse-guardrails` vs `posttooluse-normalization`: deny-before-execution vs
  normalize-output-after-execution. [CONFIG]
- `deterministic-agent-loop` vs `validation-retry-feedback`: halt/dispatch control
  vs retry-on-invalid-output with specific feedback. [DOC]
- `custom-commands-skills` vs `hierarchical-claude-memory`: invocable context forks
  vs always-loaded layered CLAUDE.md memory. [DOC]
- `hub-and-spoke-isolation` vs `multiagent-error-propagation`: subagent context
  isolation vs how errors travel between agents. [DOC]

## Self-check before declaring done

1. Did I read EXACTLY ONE playbook? (transcript shows no second `references/*.md`) [DOC]
2. Does the resolved topic match the user's actual failure mode? [INFERENCIA]
3. Is the output structured per the playbook, not improvised? [DOC]
4. Are all of the playbook's acceptance criteria satisfied? [DOC]
5. One Alfa-core tag per non-obvious claim; no mixed families; every `[SUPUESTO]`
   has a verification step? [DOC]
6. Script-first honored where a script exists; no prices/PII; single brand? [DOC]

If any answer is "no", do not pass — fix or re-route. Green/no-errors is not
proof; verify against the criteria. [INFERENCIA]
