<!-- distilled from alfa skills/internal-memo -->
# Internal Memo
> "Method over hacks."
## TL;DR
Executive memo structure for decision briefs, status updates, and action items. One memo = one decision or one status. If it needs two, write two. [EXPLICIT]

## Anatomy (in order)
1. **Subject line** — verb + object + outcome ("Approve Q3 vendor switch"), not a topic ("Vendor"). [SUGGESTED]
2. **Bottom line up front (BLUF)** — the ask/decision in ≤2 sentences, before any context. [EXPLICIT]
3. **Context** — only what's needed to act; link the rest. [EXPLICIT]
4. **Options + recommendation** — each option with its JUSTIFIED trade-off. [INFERRED]
5. **Action items** — owner + deadline + done-criteria per line. [EXPLICIT]

## Procedure
### Step 1: Discover
- Gather context, the decision owner, and the deadline. No owner/deadline ⇒ it's a discussion, not a memo. [EXPLICIT]
### Step 2: Analyze
- Evaluate options per Constitution XIII/XIV; record the trade-off you accepted, not just the winner. [EXPLICIT]
### Step 3: Execute
- Draft BLUF-first; tag every non-obvious claim with evidence ([EXPLICIT]/[INFERRED]/[SUGGESTED]). [EXPLICIT]
### Step 4: Validate
- Verify quality criteria; a reader skimming only BLUF + action items must still act correctly. [EXPLICIT]

## Quality Criteria
- [ ] BLUF answers the ask in the first 2 sentences
- [ ] Evidence tags applied to every non-obvious claim
- [ ] Constitution-compliant (no prices; single brand; no client PII)
- [ ] Every action item has owner + deadline + done-criteria
- [ ] Recommendation states the trade-off accepted

## Worked Example (BLUF block)
> **Decision needed by Fri:** approve migrating CI from Jenkins to GitHub Actions. [EXPLICIT]
> **Recommendation:** approve. Saves ~6 FTE-hrs/wk maintenance; trade-off is a 2-week parallel-run cost. [INFERRED]
> **Action:** @lead spikes the runner config by Wed; @ops confirms secrets parity by Thu. [EXPLICIT]

## Usage

Example invocations:

- "/internal-memo" — Run the full internal memo workflow
- "internal memo on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Anti-scope: not a spec, RFC, or post-mortem — those have their own skills [INFERRED]
- Single decision/status per memo; split compound asks [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| No decision owner or deadline | Downgrade to FYI note or send back for an owner [INFERRED] |
| Price/cost requested | Refuse figures; express effort in FTE-months with disclaimer [EXPLICIT] |
| Multiple decisions bundled | Split into one memo per decision [EXPLICIT] |

## Failure Modes
- **Buried lede** — context before the ask; reader misses the decision. Fix: BLUF first. [EXPLICIT]
- **Unowned actions** — "we should…" with no owner; nothing happens. Fix: name a person. [EXPLICIT]
- **Untagged claims** — assertions read as fact; erodes trust. Fix: tag or cut. [EXPLICIT]
