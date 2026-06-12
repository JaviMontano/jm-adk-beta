<!-- distilled from alfa skills/context-window-management -->
<!-- > -->
# Context Window Management

> "Method over hacks."

## Purpose

Manages context-window pressure with deterministic token budgets, priority tiers,
compression rules, and eviction boundaries. It protects high-priority session
state while reducing lower-priority context into verifiable summaries or
references. [EXPLICIT]

It is read-only over project state: it produces a *plan plus machine report*, never
mutates files, and never silently drops active context. [EXPLICIT]

## When to Activate

- The user asks for context window management, token budgeting, context trimming,
  compression, summarization priority, or what to preserve before a large task.
- A session is approaching context limits and needs an explicit keep/compress/evict
  plan.
- A handoff or compact operation needs a deterministic context budget report.

Do not activate for browser window sizing, UI layout windows, operating-system
window management, or generic text summarization without context-budget pressure.

## Deterministic Resources

- `assets/budget-policy.json` defines budget fields and response reserve rules.
- `assets/priority-policy.json` defines P0/P1/P2/P3 retention tiers.
- `assets/compression-policy.json` defines allowed compression methods and
  preservation requirements.
- `assets/eviction-policy.json` defines safe eviction order and P0 protection.
- `assets/report-contract.json` defines the machine-checkable budget report.
- `scripts/validate_context_window_report.py` validates reports offline.
- `scripts/check.sh` runs deterministic positive and negative fixtures.

Policies are the source of truth: when this doc and a policy disagree, the policy
wins and this doc is the defect. [EXPLICIT]

## Procedure

### Step 1: Discover

1. List context items with stable IDs, source names, and estimated token counts.
2. Record `max_context_tokens`, `reserved_response_tokens`, and computed
   `available_context_tokens`.
3. Classify each context item as P0, P1, P2, or P3.

If any item lacks a token estimate, stop here and request estimates — never guess a
budget, because one wrong estimate can silently push the post-plan total over the
limit. [EXPLICIT]

### Step 2: Analyze

1. Sum current estimated tokens.
2. Keep all P0 items in full.
3. Prefer compressing P2/P3 before evicting.
4. Evict only the lowest-priority eligible items when compression is insufficient.
5. Require compression output to preserve IDs, paths, decisions, blockers,
   validation evidence, and open questions when present.

Decision — *compress before evict*: compression keeps recoverable signal (decisions,
IDs) at a fraction of the tokens, while eviction is lossy and irreversible within the
session. Trade-off: compression costs model effort and can distort nuance, so P0 is
never compressed and P1 only via structured summary that preserves durable facts. [EXPLICIT]

Decision — *P1 eviction needs Guardian warning*: P1 is active work; dropping it risks
correctness, so it is gated rather than automatic. Trade-off: a session may stay over
budget and block rather than auto-trim active context — blocking is the safer
failure. [EXPLICIT]

### Step 3: Execute

Create a plan with:

- context budget
- item-level keep/compress/evict actions
- compression method and before/after estimates
- eviction reasons
- final post-plan token estimate
- Guardian decision

### Step 4: Validate

- `available_context_tokens = max_context_tokens - reserved_response_tokens`.
- `post_plan_estimated_tokens <= available_context_tokens`.
- P0 items are never evicted.
- Compression never increases estimated tokens.
- Compression preserves required durable facts.
- Eviction order starts at P3, then P2, then P1 only with Guardian warning.
- Run `bash skills/context-window-management/scripts/check.sh`; a plan is not done
  until the machine report passes.

## Priority Tiers

| Tier | Meaning | Default Action |
|---|---|---|
| P0 | Active user instructions, repo status, open PR/blocker, current branch, validation evidence. | keep |
| P1 | Active task files, recently edited code, current skill contract. | keep or structured-summary |
| P2 | Supporting docs, examples, adjacent context. | compress |
| P3 | Historical or redundant context. | reference or evict |

Tie-break when an item fits two tiers: assign the **higher** tier (lower number). A
file that is both "recently edited" (P1) and "open blocker" (P0) is P0. [EXPLICIT]

## Worked Example

Budget: `max_context_tokens=8000`, `reserved_response_tokens=2000` →
`available_context_tokens=6000`. Current items total 9200, so the plan is 3200 over.

| ID | Item | Tier | Before | Action | After | Reason |
|---|---|---|---|---|---|---|
| c1 | User task + acceptance criteria | P0 | 600 | keep | 600 | active instruction |
| c2 | Current branch + PR/blocker status | P0 | 400 | keep | 400 | repo state |
| c3 | File under edit | P1 | 2200 | keep | 2200 | active work |
| c4 | Skill contract | P1 | 1500 | structured-summary | 600 | preserves IDs/decisions |
| c5 | Adjacent design doc | P2 | 2000 | compress | 500 | supporting only |
| c6 | Old chat transcript | P3 | 2500 | evict (→ reference) | 0 | historical/redundant |

Post-plan estimate = 600+400+2200+600+500+0 = **4300 ≤ 6000**. Guardian: PASS (no P0
evicted, no P1 forced-evict, total fits). Order respected: P3 (c6) evicted, P2 (c5)
compressed, P1 (c4) summarized — no P1 eviction needed. [EXPLICIT]

## Failure Modes

| Failure | Symptom | Recovery |
|---|---|---|
| Phantom savings | Compressed item's "after" ≥ "before". | Reject method; pick a real reducer or evict instead. |
| Silent over-budget | Post-plan ≤ available but an estimate was a guess. | Re-estimate flagged items; rerun validation. |
| Durable-fact loss | Summary drops an ID, path, decision, or blocker. | Block; re-run compression preserving required fields. |
| P0 starvation | P0 alone exceeds `available_context_tokens`. | Block and escalate; raise budget or split the task — do not evict P0. |
| Guardian bypass | P1 evicted without warning recorded. | Reject plan; require explicit Guardian decision. |

## Quality Criteria

- [ ] Budget fields are explicit and arithmetically consistent.
- [ ] Every item has ID, priority, estimate, action, rationale, and evidence tag.
- [ ] P0 items are kept.
- [ ] Compression methods are allowed and reduce token estimates.
- [ ] Compression preservation fields are non-empty.
- [ ] Eviction targets lowest-priority eligible items first.
- [ ] Final estimate fits the available budget.
- [ ] Machine report passes `bash skills/context-window-management/scripts/check.sh`.

## Usage

Example invocations:

- `/context-window-management`
- `Plan context trimming before this large refactor.`
- `Create a keep/compress/evict plan for these sources with an 8000-token budget.`

## Assumptions & Limits

- Token counts are estimates unless a tokenizer is explicitly provided. [EXPLICIT]
- The skill does not delete source files or mutate project state. [EXPLICIT]
- The skill does not replace user confirmation for dropping active context. [EXPLICIT]
- Anti-scope: it does not raise `max_context_tokens`, summarize for delivery, or
  decide task priority — only keep/compress/evict against a given budget. [EXPLICIT]

## Acceptance Criteria

- Given items with estimates and a budget, the plan emits an action + rationale per
  item and a post-plan total that satisfies every Step 4 check. [EXPLICIT]
- Given a missing estimate or a P0 eviction, the skill blocks with a stated reason
  rather than producing a plan. [EXPLICIT]
- The emitted report passes `validate_context_window_report.py` and `check.sh`
  fixtures (positive and negative). [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|---|---|
| Missing token estimates | Block or request estimates. |
| Over budget after compression | Evict eligible P3/P2 items or block. |
| P0 proposed for eviction | Block. |
| Compression loses IDs or decisions | Block. |
| P0 alone exceeds available budget | Block and escalate; never evict P0. |
| Ties between two tiers | Assign the higher (lower-numbered) tier. |
| Browser window request | Do not activate. |
