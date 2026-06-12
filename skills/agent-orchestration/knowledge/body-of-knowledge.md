# Body of Knowledge — agent-orchestration

Domain knowledge for routing and running multi-agent orchestration under
PRISTINO. Scoped to this skill's 10 topics; not a general agents primer. [DOC]

## 1. Core concept: the router

`agent-orchestration` is a **dispatch skill**, not a doer. Its only job is to
resolve a single `topic` and hand off to exactly one playbook. Loading the whole
cluster defeats the router and dilutes context. [CONFIG]

The 10 topics and their playbooks:

| Topic | Owns |
|---|---|
| `triad-composition` | Lead/Support/Guardian role selection |
| `multi-model-routing` | which model per task |
| `intelligent-routing` | which skill/agent handles a request |
| `workflow-orchestration` | end-to-end resumable run |
| `parallel-workflow` | concurrent fan-out |
| `subagent-monitor` | live subagent status |
| `socratic-debate` | multi-perspective reasoning |
| `continuous-learning` | harvesting debate/discovery insights |
| `error-recovery-automation` | safe recovery of a failed step |
| `task-automation` | schedule / trigger work |

## 2. The spine

Every run follows **Discover → Analyze → Execute → Validate**. Discover gathers
inputs; Analyze applies the playbook's policy and records the trade-off rejected;
Execute produces the deliverable (script-first where available); Validate runs
the Guardian gate. [DOC]

## 3. Evidence taxonomy (Alfa core set)

`[CODE]` (from source), `[CONFIG]` (from config/frontmatter/policy JSON),
`[DOC]` (from a playbook or canon doc), `[INFERENCE]` (reasoned, not stated),
`[ASSUMPTION]` (unverified premise). One family per output; EN/ES tag usage must
stay consistent. Never assert success-as-green before the Guardian runs. [DOC]

## 4. Decision rules

- **Narrowest match wins.** Use the disambiguation table; prefer the most
  specific topic (e.g. live status → `subagent-monitor`, not the broader
  `workflow-orchestration`). [DOC]
- **Confidence bands (triad-composition).** `>=0.85` auto-select; `0.60–0.84`
  present top 3 and ask; `<0.60` clarify. Bands inclusive at the lower bound. [CONFIG]
- **Stable tie-breakers.** exact phrase → keyword hits → score → earliest matrix
  order (final). Guarantees identical requests yield identical routes. [CONFIG]
- **Rollback before retry (error-recovery-automation).** Never retry into a
  state not first made safe; escalation overrides both. [INFERENCE]
- **Checkpoint per durable stage (workflow-orchestration).** A single trailing
  checkpoint forces full replay on failure. [INFERENCE]
- **Idempotency gate.** Retry only when re-execution is idempotent or no partial
  write occurred. [INFERENCE]
- **Committee is the exception.** Each escalation states why a triad cannot own
  the decision. [DOC]

## 5. Standards / canon

- **Constitution v6.0.0** — enforcement gate before "done" (referenced by
  SKILL.md). [CONFIG]
- **PRISTINO** — triad pattern, composition matrix, confidence bands, degraded
  mode, G0–G3 gates. [DOC]
- **Script-first rule** — when a topic ships a deterministic `scripts/check`,
  run it instead of hand-asserting validity. [CONFIG]

## 6. Failure modes and guards

| Failure mode | Guard |
|---|---|
| Multiple playbooks loaded | Router discipline: one playbook or ask [CONFIG] |
| Guessed topic on a genuine tie | Ask one clarifying question [ASSUMPTION] |
| Invented topic outside enum | Catalog parser rejects it [CONFIG] |
| Premature "complete" | Guardian gate is mandatory [DOC] |
| Blind retry on failure | Classify first; rollback if state may be corrupt [INFERENCE] |
| Silent stage failure | Declare failureSignals per stage [DOC] |
| Wrong-playbook stretch mid-run | Self-correct: stop, re-resolve, switch [INFERENCE] |

## 7. Definition of done

One playbook loaded; spine completed; constitution + evidence + script-first
gates passed; tags single-family and EN/ES consistent; resumable/recovery topics
carry their required state/ordering. [DOC]
