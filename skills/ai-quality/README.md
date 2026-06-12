# ai-quality

A **router skill** for AI and code quality work. It resolves exactly one
`topic` from the user request, reads only that topic's playbook from
`references/`, and executes the playbook's Discover → Analyze → Execute →
Validate spine. It never preloads the whole cluster — single-route loading is
the design, because token waste and cross-topic bleed are the failure modes
this router exists to prevent. [DOC]

## What it does

Given a quality request, `ai-quality` maps intent to one of nine fixed topics
and delegates to the matching playbook:

| Topic | Playbook | Use when… |
|-------|----------|-----------|
| `ai-testing-strategy` | `references/ai-testing-strategy.md` | Defining the 6×6 test-type×layer strategy for an AI system (model, data, fairness, CI/CD). |
| `ai-assisted-testing` | `references/ai-assisted-testing.md` | AI proposes test cases, fuzz specs, mutation plans, coverage targets. |
| `ai-code-review` | `references/ai-code-review.md` | AI-assisted review of a diff with file-line evidence and a JSON packet. |
| `code-review` | `references/code-review.md` | Human/tool review of a diff with fixed severities and a release decision. |
| `llm-evaluation` | `references/llm-evaluation.md` | Scoring model output: hallucination/groundedness, LLM-judge, benchmarks. |
| `ai-safety` | `references/ai-safety.md` | Risk taxonomy → controls → jailbreak tests → metrics → escalation packet. |
| `ai-content-detection` | `references/ai-content-detection.md` | Likelihood that content is AI-generated; watermark/provenance; hybrid policy. |
| `ai-documentation` | `references/ai-documentation.md` | Source-backed README/API/architecture docs and drift audits. |
| `ai-workflow-automation` | `references/ai-workflow-automation.md` | LLM-in-the-loop workflow plans with human gates, handoffs, bounded retries. |

## When to use

Any request to **assess, test, review, evaluate, or harden** code or AI output:
test plans, LLM-judge evaluation, human or AI code review, model safety,
AI-vs-human content detection, quality documentation, or QA automation. [DOC]

Not for: building features, prompt authoring, or deployment — route those
elsewhere.

## How it routes and executes

1. Map intent → exactly one `topic` (enums in `SKILL.md` are fixed; never invent
   one). [CÓDIGO]
2. Disambiguate near-collisions with the rules in `SKILL.md`: AI **scores**
   output → `llm-evaluation`; AI **writes/runs** tests → `ai-assisted-testing`;
   AI **reviews a diff** → `ai-code-review`; **human/tool** review of a diff →
   `code-review`. [INFERENCIA]
3. Read that **one** playbook (`depth=quick` = essentials, `depth=deep` =
   exhaustive with verification per step). [CONFIG]
4. Run the playbook's Discover → Analyze → Execute → Validate spine and pass its
   offline validation gate before "done". [DOC]

## Evidence taxonomy

This is a kit-facing router; every non-obvious claim carries one tag from the
**Alfa core set** — `[CÓDIGO]` `[CONFIG]` `[DOC]` `[INFERENCIA]` `[SUPUESTO]` —
and tag families are never mixed inside a single deliverable. A `[CÓDIGO]` tag
with no in-repo referent downgrades to `[SUPUESTO]`. [DOC]

## Bundle map

- `SKILL.md` — the router contract (params, routes, validation gate).
- `references/*.md` — the nine topic playbooks (read one, not the cluster).
- `routes.json` — machine-readable topic → playbook map.
- `agents/` — role contracts (lead, specialist, support, guardian).
- `knowledge/` — body of knowledge + concept graph for the router domain.
- `prompts/` — primary, meta, and quick/deep variation prompts.
- `templates/output.md` — the routing-and-execution deliverable scaffold.
- `evals/evals.json` — routing and gate-discipline test cases.
- `examples/` — a worked routing example (ambiguous request → resolved topic).
- `assets/` — the deterministic asset bundle (routing matrix + quality rubric);
  see `assets/README.md`.
