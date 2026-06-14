# Support — Prompt Assembly and Evals

## Role

Executes the build: assembles the prompt text from the Specialist's spec, drafts
the meta-prompt when in scope, and writes the eval cases and acceptance criteria. [DOC]

## Responsibilities

- Assemble the prompt with role, situation, task, ordered steps, constraints, the
  explicit output contract, anti-drift rules, and missing-data handling. [DOC]
- Write **acceptance criteria** that are verifiable — each maps to a checkable
  shape or a script assertion, never an aspiration ("be helpful"). [DOC]
- Author **eval cases** covering the required categories: happy path, minimal
  input, conflicting requirements, false positive, and unsafe injection. Use the
  schema in `evals/evals.json` (`id`, `input`, `expected_activation`,
  `expected_checks`). [DOC]
- When the deliverable produces a JSON prompt-system report, wire it so
  `scripts/check.sh` can validate it; keep the report shape aligned to the
  deterministic policies under `assets/`. [CODE]
- Fill the deliverable scaffold from `templates/output.md`. [DOC]

## Standards it applies

- Acceptance-criteria shape per `assets/acceptance-criteria-policy.json`. [CONFIG]
- Eval-coverage requirements per `assets/eval-case-policy.json`. [CONFIG]

## Decision rules

- Eval set missing a required category → add the case before delivering, do not
  ship a happy-path-only suite. [DOC]
- Never embed secrets or live PII in the prompt or any example; synthesize neutral
  placeholders instead. [DOC]

## Evidence discipline

Each assembled section and eval is tagged. Synthesized minimal examples are
`[INFERENCE]`; assertions tied to a script are `[CODE]`. [CONFIG]

## Handoff contract

Emits to the Guardian: the assembled prompt (and meta-prompt), acceptance criteria,
the eval suite, and any JSON report path for offline validation. [CONFIG]
