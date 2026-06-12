# Body of Knowledge — Prompting and Meta-Prompting

Domain knowledge for designing durable, eval-ready prompts and meta-prompts.
Evidence tags: `[DOC]` `[CODE]` `[CONFIG]` `[INFERENCE]` `[ASSUMPTION]`. [DOC]

## 1. Core concepts

- **Prompt** — an instruction set that drives a single model behavior. A durable
  prompt carries objective, audience, context, constraints, an ordered task
  sequence, an explicit output contract, anti-drift rules, and missing-data
  handling. [DOC]
- **System prompt** — a persistent instruction layer that frames role, boundaries,
  and defaults across turns; it should encode safety and anti-drift, not just tone. [DOC]
- **Meta-prompt** — a prompt whose subject is another prompt: it reviews, scores,
  or improves prompts against named review dimensions. A meta-prompt with no
  dimensions is non-functional. [DOC]
- **Output contract** — the verifiable shape of the response: schema, format,
  length bounds, plus a minimal example. Prose descriptions are not contracts. [DOC]
- **Anti-drift rule** — a constraint embedded in the prompt that resists scope
  creep, tone slippage, and silent assumption-filling across long interactions. [INFERENCE]

## 2. Prompt component policy (required structure)

A shippable prompt must contain, in order: objective → audience → context →
constraints → sequence → output contract → anti-drift rules → missing-data
handling. Enforced by `assets/prompt-component-policy.json`. Omitting any
component is an anti-pattern. [CONFIG]

## 3. Patterns and when to use them

| Pattern | Use when | Primary risk |
|---|---|---|
| Role-Situation-Task-Sequence | General single-pass tasks | Drift if sequence unbounded [INFERENCE] |
| Few-shot / example-led | Output shape is hard to describe | Examples leak into output [INFERENCE] |
| Schema-constrained output | Machine consumption downstream | Over-rigid, brittle to edge inputs [INFERENCE] |
| Plan-then-execute | Multi-step or tool-using tasks | Plan/execution divergence [INFERENCE] |
| Meta-prompt | Reviewing/improving other prompts | No review dimensions defined [DOC] |

## 4. Failure modes to name before drafting

- **Drift** — behavior wanders from objective over turns. [INFERENCE]
- **Ambiguity** — two valid interpretations of the objective survive Discover. [INFERENCE]
- **Over-trigger / false activation** — prompt fires on out-of-scope requests. [INFERENCE]
- **Instruction collision** — constraints contradict (e.g. deterministic yet may
  invent facts). [INFERENCE]
- **Output-shape leakage** — the model emits scaffolding or chain-of-thought. [DOC]

## 5. Decision rules

- Runtime unknown → portable Markdown with placeholders; note per-runtime
  specialization. Portability over model-tuned phrasing. [INFERENCE]
- Embed constraints in the prompt, not only in docs — docs are not loaded at
  runtime. [INFERENCE]
- Refuse over partial-comply on safety conflicts — a half-safe prompt is worse
  than none; predictability beats helpfulness here. [ASSUMPTION]
- If the prompt only restates the request without adding structure/constraints, it
  adds no value — redesign. [ASSUMPTION]

## 6. Acceptance criteria standard

Each criterion maps to a checkable shape or a script assertion. Verifiable, not
aspirational. "Be helpful / do your best" is rejected. Enforced by
`assets/acceptance-criteria-policy.json`. [CONFIG]

## 7. Eval coverage standard

A behavior change requires evals covering, at minimum: happy path, minimal input,
conflicting requirements, false positive, and unsafe injection. Happy-path-only
suites are rejected. Enforced by `assets/eval-case-policy.json`. [CONFIG]

## 8. Safety boundaries

- Never expose hidden chain-of-thought. [DOC]
- Never optimize a prompt for credential capture or unsafe automation. [DOC]
- Never embed live PII or secrets in the prompt or examples. [DOC]
- On safety conflict, the Guardian blocks: emit `expected_activation: false` and a
  reason; do not partially comply. Enforced by
  `assets/safety-anti-drift-policy.json`. [CONFIG]

## 9. Evidence taxonomy (Alfa core set)

`[DOC]` documented/known; `[CODE]` verified in code or script output; `[CONFIG]`
declared in a config/policy file; `[INFERENCE]` reasoned from evidence;
`[ASSUMPTION]` stated assumption to be confirmed. Every load-bearing claim carries
one tag. [DOC]
