<!-- distilled from alfa skills/ai-workflow-automation -->
<!-- > -->
# AI Workflow Automation
> "Method over hacks."
## TL;DR
Design deterministic LLM-in-the-loop workflow plans where AI steps, human
approval gates, handoff artifacts, retries, fallbacks, and validation evidence
are explicit and offline-checkable *before* any execution. [DOC]

**Output is a plan, not a running system.** This skill emits a bounded plan
artifact; it does not orchestrate, call models, or mutate external state. [DOC]

## Procedure
### Step 1: Discover
- Identify workflow goal, trigger, actors, inputs, outputs, risk level, and
  approval boundaries.
- Capture existing constraints, required human decisions, and source artifacts.
- Classify each step's risk: external side effect (send/write/pay/delete),
  irreversibility, and data sensitivity drive gate placement. [INFERENCE]
### Step 2: Analyze
- Classify actors with `assets/actor-taxonomy.json` (`human`/`ai`/`system`).
- Model steps with `assets/workflow-schema.json`.
- Map approvals with `assets/approval-gate-policy.json`.
- Define handoffs with `assets/handoff-policy.json`.
- Define retries/fallbacks with `assets/failure-policy.json`.
### Step 3: Execute
- Produce a bounded plan using `assets/report-contract.json` containing: AI
  prompt input contracts, output contracts, human approval criteria, handoff
  packets, fallback paths, and deterministic validation checks.
### Step 4: Validate
- Verify all Quality Criteria below are met.
- For JSON plans, run `bash skills/ai-workflow-automation/scripts/check.sh`.
- A plan that fails `check.sh` is not shippable — fix, do not waive. [DOC]

## Deterministic Assets

- `assets/manifest.json` lists local assets and consumers.
- `assets/workflow-schema.json` defines required workflow plan fields.
- `assets/actor-taxonomy.json` defines `human`, `ai`, and `system` actor rules.
- `assets/approval-gate-policy.json` defines gate criteria and decision values.
- `assets/handoff-policy.json` defines handoff packet requirements.
- `assets/failure-policy.json` defines bounded retry and fallback behavior.
- `assets/report-contract.json` defines the offline-validatable workflow plan.

## Design Decisions & Trade-offs
- **Gate before effect, not after.** Approval gates precede any external-effect
  step so a rejection blocks the side effect entirely. Trade-off: adds latency
  and a human dependency; accepted because an un-gated irreversible action
  cannot be undone by a later check. [INFERENCE]
- **Bounded retries over open loops.** Every retry carries a max count + a
  fallback. Trade-off: a transient failure past the limit escalates to a human
  instead of self-healing; accepted to guarantee termination. [DOC]
- **Offline-validatable plans.** Validation forbids live network and
  current-time inputs. Trade-off: cannot assert against live systems in
  `check.sh`; accepted so plan review is reproducible and CI-stable. [DOC]
- **Contracts on both sides of every AI step.** Input + output contract are
  mandatory. Trade-off: more upfront spec work; accepted because an untyped AI
  output is the most common silent-failure source in handoffs. [INFERENCE]

## Worked Example (support triage)
Trigger: new ticket. Plan skeleton (abbreviated): [DOC]
1. `ai` classify — input contract `{ticket_text}` → output contract
   `{category∈enum, severity∈1..4, pii_flag:bool}`.
2. Gate (auto): `severity<=2 && !pii_flag` → continue; else route to step 3.
3. Gate (`human`, owner=on-call lead): approve auto-reply or take over.
   Acceptance: decision recorded with reviewer id + timestamp-placeholder.
4. `system` send reply — retry max 2, fallback = queue for manual send.
5. Handoff packet on takeover: ticket id, classification, draft reply, reason.

Anti-example: a single `ai` step that classifies *and* sends the reply with no
gate and "retry until sent" — blocked by Edge Cases rows 4 and 6. [INFERENCE]

## Quality Criteria
- [ ] Evidence tags applied (single Alfa family; see references/verification-tags.md)
- [ ] Constitution-compliant
- [ ] Actionable output
- [ ] AI steps include prompt input contract and output contract
- [ ] High-risk or external-effect steps have approval gates before execution
- [ ] Human handoffs include artifact, owner, acceptance criteria, and evidence
- [ ] Retries are bounded and fallback paths are explicit
- [ ] Validation is reproducible without live network or current-time dependency

## Usage

Example invocations:

- "/ai-workflow-automation" — Run the full ai workflow automation workflow
- "ai workflow automation on this project" — Apply to current context
- "Design an LLM workflow with approval gates for support triage"
- "Create a human-AI handoff plan for invoice review automation"

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs). [DOC]
- Output is English unless otherwise specified. [DOC]
- Does not replace domain-expert judgment for final decisions. [DOC]
- **Anti-scope:** does not execute, schedule, or monitor workflows; does not
  pick or call a model provider; does not estimate cost or pricing. [DOC]
- Plan correctness is bounded by input completeness — a plan can be internally
  valid yet wrong if Discover inputs were wrong. [INFERENCE]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| AI step lacks output contract | Block plan until contract exists |
| Approval owner missing | Mark as blocked; do not auto-approve |
| Retry policy says "until it works" | Replace with bounded retry + fallback |
| Gate placed after the side effect | Reorder so gate precedes the effect [INFERENCE] |
| Circular handoff (A→B→A, no exit) | Reject; require a terminal owner/state |
| Two AI steps chained, no contract between | Insert intermediate output contract |
| Validation needs live API or now() | Reject; stub to fixed inputs for `check.sh` |

## Failure Modes
- **Silent contract drift:** AI output shape changes, downstream still consumes
  it. Mitigation: output contract is validated, not assumed. [INFERENCE]
- **Auto-approval creep:** a gate's criteria widen until it never blocks.
  Mitigation: gate criteria are explicit data, reviewable in the plan. [DOC]
- **Unbounded retry storm:** "retry until success" against a flapping
  dependency. Mitigation: bounded retries + fallback are mandatory. [DOC]
- **Orphaned handoff:** packet emitted with no owner to receive it. Mitigation:
  handoff policy requires a named owner + acceptance criteria. [DOC]
