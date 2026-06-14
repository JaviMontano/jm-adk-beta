# ux-research

Router skill for **user research and validation**. One invocation resolves a
`topic` and reads **exactly one** playbook — never the whole cluster — then drives
the Discover → Analyze → Execute → Validate spine to a tagged deliverable. [DOC]

## What it does

Maps a UX/discovery request to one of four routes and runs that playbook to
produce a research deliverable: an interview/persona study, a survey instrument,
a usability test plan, or a prototype spec. Each output carries Alfa-core evidence
tags and an explicit next step. [DOC]

## When to use

Use when the task is to **learn from or validate with users** before or around a
build. Do **not** use for production UI/build work (frontend skills), product
strategy, or analytics instrumentation. [INFERENCIA]

## Routes

| Topic | Use when | Playbook |
|-------|----------|----------|
| `user-research` | Generative: interviews, contextual inquiry, personas, journey maps — the *why/what users need* | `references/user-research.md` |
| `survey-design` | Quantitative attitudes/segmentation at scale; NPS/CSAT/CES — *how many/how often* | `references/survey-design.md` |
| `user-testing` | Evaluate an existing flow/prototype: task success, severity-rated usability findings | `references/user-testing.md` |
| `prototyping` | Produce a testable artifact on the fidelity ladder before build | `references/prototyping.md` |

## How it routes and executes

1. **Resolve `topic`** from the request; if two routes are plausible, ask one
   disambiguating question — never run two playbooks. [INFERENCIA]
2. **Resolve `depth`** (`quick` = essentials, single pass; `deep` = exhaustive,
   verify each step). Default `quick`. [DOC]
3. **Read exactly one** playbook from `routes:` and follow its four-step spine. [DOC]
4. **Gate** before "done": one playbook read, evidence tags present, every
   `[SUPUESTO]` paired with a verification step. [DOC]

Method-to-question rule: *why/how* → `user-research`; *how many* → `survey-design`;
*can they do the task* → `user-testing`; *is the concept right before build* →
`prototyping`. [INFERENCIA]

## Map of this bundle

- `SKILL.md` — router contract, params, validation gate.
- `references/*.md` — the four playbooks (one read per invocation).
- `agents/` — lead, specialist, support, guardian role contracts.
- `knowledge/` — body of knowledge + concept knowledge graph.
- `prompts/` — primary, meta, and quick/deep variations.
- `templates/output.md` — research deliverable scaffold.
- `evals/evals.json` — scenario suite with expected checks.
- `examples/` — a worked input/output pair.
- `assets/` — quality rubric + route-selection checklist (see `assets/README.md`).

## Evidence convention

Alfa-core family only, one tag per claim:
`[CODE]` `[CONFIG]` `[DOC]` `[INFERENCIA]` `[SUPUESTO]` (playbooks may also use
`[EXPLICIT]`). Never assert a status green; pair every `[SUPUESTO]` with the step
that would confirm it. No invented prices, no client PII. [CONFIG]
