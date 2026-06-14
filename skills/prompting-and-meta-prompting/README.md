# prompting-and-meta-prompting

Turns vague intentions into durable, eval-ready prompts, meta-prompts, acceptance
criteria, and prompt systems with anti-drift and safety gates. [DOC]

## What it does

- Converts a loose request ("make a PR-review prompt") into a structured prompt
  with role, situation, task, ordered steps, constraints, an explicit output
  contract, anti-drift rules, and missing-data handling. [DOC]
- Builds **meta-prompts** — prompts that review or improve other prompts against
  named dimensions (objective alignment, evidence policy, missing-data handling,
  output schema, eval coverage, safety). [DOC]
- Emits **acceptance criteria** that are verifiable (checkable shape) rather than
  aspirational, plus **eval cases** that cover happy path, minimal input,
  conflicting requirements, false positives, and unsafe injection. [DOC]
- Enforces safety boundaries: refuses credential capture, hidden chain-of-thought
  exposure, and unsafe automation; blocks instead of partially complying. [DOC]

## When to use

- The deliverable is a prompt, system prompt, meta-prompt, or prompt evaluation. [DOC]
- A repeated workflow should harden into a reusable instruction, checklist, or eval. [DOC]
- A weak prompt lacks objective, context, constraints, output shape, or anti-drift. [DOC]

Do not use it when the prompt is only a means to a one-off task (just do the task),
when unverified recent facts are needed (verify first), or when the request asks
the prompt to break safety (refuse and route to Safety Limits). [DOC]

## How it routes and executes

Four phases, gated before delivery: [DOC]

1. **Discover** — extract goal, audience, context, constraints, missing data,
   done criteria; flag gaps before drafting. (`agents/lead.md`)
2. **Analyze** — pick a prompt pattern, name likely failure modes (drift,
   ambiguity, over-trigger). (`agents/specialist.md`)
3. **Execute** — assemble the prompt and, when needed, the meta-prompt and evals.
   (`agents/support.md`)
4. **Validate** — run the validation gate and the offline JSON check; deliver only
   on pass, else self-correct. (`agents/guardian.md`)

## Evidence taxonomy

Every claim carries an Alfa-core tag: `[DOC]` `[CODE]` `[CONFIG]` `[INFERENCE]`
`[ASSUMPTION]`. The Guardian blocks delivery if a load-bearing claim is untagged
or if a safety boundary is crossed. [CONFIG]

## References and bundle

- `SKILL.md` — full contract, validation gate, anti-patterns, safety limits.
- `knowledge/body-of-knowledge.md` — prompt-engineering concepts, standards, rules.
- `knowledge/knowledge-graph.json` — concept graph over the skill's key ideas.
- `prompts/` — `primary.md`, `meta.md`, and `variations/{quick,deep}.md`.
- `templates/output.md` — the deliverable scaffold.
- `evals/evals.json` — edge-case eval suite.
- `examples/` — a worked PR-review prompt request and its output.
- `assets/` — deterministic policy contracts and a quality rubric (see
  `assets/README.md`).
