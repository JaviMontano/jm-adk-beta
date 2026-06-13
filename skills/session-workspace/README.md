# session-workspace

Router skill for the **agent session lifecycle**. It does no lifecycle work
itself — it reads the user's intent, resolves a single `topic`, and dispatches to
exactly one playbook under `references/`. Loading the whole cluster is a defect;
this router exists to prevent that. [DOC]

## What it does

Given a session-lifecycle moment (cold start, in-session discipline, state
read/write, context-budget pressure, pre-compaction snapshot, inbound
notification, or clean teardown), it picks the matching playbook and hands off.
It emits no artifacts of its own — the routed playbook owns the deliverable. [INFERENCE]

## When to use

Use when the task is about *running the session*, not the content inside it:

- Starting or resuming a session, or recovering after a compaction.
- Reading or writing `.specify/context.json` stage/artifact state.
- Approaching the context-window limit and needing a keep/compress/evict plan.
- Snapshotting state *before* auto-compaction or `/clear`.
- Triaging or routing an inbound notification mid-run.
- Closing a session with a handoff a cold reader can act on.

Do **not** use for content authoring, code edits, or any single-domain task — that
is a different skill. If two topics seem to apply, ask one clarifying question
rather than fanning out. [INFERENCE]

## How it routes

`topic` (required, one of seven) selects the playbook; `depth` (`quick` | `deep`)
controls thoroughness. Resolution: infer `topic` from the request, ask only if
ambiguous, then Read exactly one route file. [CONFIG]

| topic | playbook | owns |
|---|---|---|
| `session-start-bootstrap` | `references/session-start-bootstrap.md` | safe start packet + Guardian gate |
| `session-protocol` | `references/session-protocol.md` | 4-step init: load → recover → close → next |
| `session-manager` | `references/session-manager.md` | `.specify/context.json` stage tracking |
| `context-window-management` | `references/context-window-management.md` | token budget keep/compress/evict plan |
| `pre-compact-context` | `references/pre-compact-context.md` | rehydration packet before compaction |
| `notification-handler` | `references/notification-handler.md` | severity routing + dedupe |
| `session-end-cleanup` | `references/session-end-cleanup.md` | closeout + durable-log handoff |

Route table of record: `routes.json`. [CONFIG]

## Spine & gates

Discover → Analyze → Execute → Validate. Every routed playbook carries Alfa-core
evidence tags (`[CODE]` `[CONFIG]` `[DOC]` `[INFERENCE]` `[ASSUMPTION]` `[OPEN]`),
a Guardian decision, and a `scripts/check.sh` fixture gate. The router enforces
single-route dispatch and `depth` honoring; the playbook enforces its own
acceptance criteria. [DOC]

## Bundle map

- Role contracts: `agents/lead.md`, `agents/specialist.md`, `agents/support.md`, `agents/guardian.md`.
- Domain knowledge: `knowledge/body-of-knowledge.md`, `knowledge/knowledge-graph.json`.
- Prompts: `prompts/primary.md`, `prompts/meta.md`, `prompts/variations/quick.md`, `prompts/variations/deep.md`.
- Deliverable scaffold: `templates/output.md`.
- Worked example: `examples/example-input.md`, `examples/example-output.md`.
- Evals: `evals/evals.json`.
- Deterministic assets: `assets/` (routing rubric + dispatch checklist) — see `assets/README.md`.
