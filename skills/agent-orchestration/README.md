# agent-orchestration

Router skill for multi-agent orchestration under PRISTINO. It resolves a single
`topic` and dispatches the request to exactly one playbook — never the whole
cluster. [DOC]

## What it does

Takes an orchestration request (compose a triad, route a request, run an
end-to-end workflow, recover a failed step, monitor live subagents, run a
multi-perspective debate, harvest its insights, fan out work in parallel, pick a
model, or schedule a job) and applies the one matching playbook through the
Discover → Analyze → Execute → Validate spine. [DOC]

## When to use

- Any request to **compose / route / run / recover / monitor** a multi-agent
  workflow under PRISTINO. [DOC]
- NOT for single-agent tasks, content generation, or domain skills — those route
  to their own skill, not here. [INFERENCE]

## How it routes

1. Resolve `topic` from the request against the 10-value enum. Ask only when two
   routes genuinely tie. [CONFIG]
2. Read **exactly one** playbook from `routes:` in `SKILL.md`. Loading several
   "to be safe" defeats the router. [CONFIG]
3. `depth=deep` → apply exhaustively and verify at each step; `quick` →
   essentials only (default). [CONFIG]
4. Run the spine, then pass the acceptance gate (one playbook loaded, spine
   complete, constitution v6.0.0 + evidence-tag + script-first gates met). [DOC]

## Topic → playbook map

| Topic | Playbook | Use when |
|---|---|---|
| `triad-composition` | `references/triad-composition.md` | Pick Lead/Support/Guardian roles |
| `multi-model-routing` | `references/multi-model-routing.md` | Pick which model per task |
| `intelligent-routing` | `references/intelligent-routing.md` | Pick which skill/agent handles a request |
| `workflow-orchestration` | `references/workflow-orchestration.md` | Run an end-to-end, resumable workflow |
| `parallel-workflow` | `references/parallel-workflow.md` | Fan out concurrent work |
| `subagent-monitor` | `references/subagent-monitor.md` | Track live subagent status |
| `socratic-debate` | `references/socratic-debate.md` | Multi-perspective reasoning |
| `continuous-learning` | `references/continuous-learning.md` | Harvest insights from debates/discoveries |
| `error-recovery-automation` | `references/error-recovery-automation.md` | Recover a failed step safely |
| `task-automation` | `references/task-automation.md` | Schedule or trigger work |

## Evidence taxonomy

Every non-obvious claim carries one tag from the Alfa core set:
`[CODE]` / `[CONFIG]` / `[DOC]` / `[INFERENCE]` / `[ASSUMPTION]`. Never mix tag
families; keep EN/ES tag usage consistent within an output. [DOC]

## References

- Playbooks: `references/*.md` (one per topic above).
- Route catalog: `routes.json`.
- Agent role contracts: `agents/lead.md`, `agents/support.md`,
  `agents/specialist.md`, `agents/guardian.md`.
- Domain knowledge: `knowledge/body-of-knowledge.md`, `knowledge/knowledge-graph.json`.
- Prompts: `prompts/primary.md`, `prompts/meta.md`, `prompts/variations/*.md`.
- Output scaffold: `templates/output.md`.
- Reusable gates/rubrics: `assets/` (see `assets/README.md`).
