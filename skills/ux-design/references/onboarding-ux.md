<!-- distilled from alfa skills/onboarding-ux -->
<!-- > -->
# Onboarding Ux

> "Method over hacks. Evidence over assumption."

## TL;DR

Design user onboarding flows that maximize activation and minimize time-to-value
(TTV): the elapsed time from first session to the user's first real outcome.
Outputs follow MetodologIA brand standards and Alfa-core evidence tags. [DOC]
Scope is the *first-N-sessions* journey, not lifecycle retention or re-engagement. [SUPUESTO]

## Definitions

- **Activation**: user reaches the "aha" moment — the first action that delivers
  the product's core value (not signup completion). Define it per product. [DOC]
- **Time-to-value (TTV)**: minutes/steps from entry to activation. The metric
  onboarding optimizes; lower is better. [INFERENCIA]
- **Aha moment**: the specific event correlated with retention (e.g. "first
  document shared", not "account created"). Must be evidence-backed. [SUPUESTO]

## Procedure

### Step 1: Discover
- Capture the activation event and current TTV baseline from product/analytics. [CONFIG]
- Read existing flows, empty states, and instrumentation; map the current path. [CÓDIGO]
- Identify drop-off steps and the gap between signup and first value. [INFERENCIA]

### Step 2: Analyze
- Pick a flow pattern (see table) against Constitution XIII Think First, XIV Simple First. [DOC]
- Cut steps that do not move the user toward activation; defer the rest. [INFERENCIA]
- Document trade-offs: friction added vs. drop-off risk vs. value clarity. [DOC]

### Step 3: Execute
- Implement the chosen pattern; instrument each step so TTV is measurable. [INFERENCIA]
- Write microcopy that states the *next action*, not feature tours. [DOC]
- Use the brand template for HTML outputs (references/brand/). [CONFIG]

### Step 4: Validate
- Confirm the activation event fires and is tracked end-to-end. [INFERENCIA]
- Check evidence-tag coverage and Constitution compliance. [DOC]

## Flow Pattern Selection

| Pattern | Use when | Trade-off |
|---------|----------|-----------|
| Progressive disclosure | Complex product, many features | Slower to full power; lowest cognitive load [INFERENCIA] |
| Setup wizard | Config required before any value | High up-front friction; clear path [INFERENCIA] |
| Empty-state guidance | Value visible without setup | Cheapest; weak for config-heavy tools [INFERENCIA] |
| Sample/demo data | Value needs content to be seen | Risks "fake" feel; instant aha [SUPUESTO] |
| Checklist | Multi-step, self-paced activation | Can feel like homework; high completion when short [INFERENCIA] |

Default to the *fewest steps that reach activation*; add a step only when it
removes a larger downstream drop-off. [INFERENCIA]

## Activation Metrics

- **Activation rate**: % of new users who hit the activation event. [DOC]
- **TTV (median)**: prefer median over mean — onboarding times are right-skewed. [INFERENCIA]
- **Step completion / drop-off**: per-step funnel; the largest drop is the target. [INFERENCIA]
- **Counter-metric**: do not trade short-term completion for long-term retention;
  watch day-7/day-30 retention of activated cohorts. [SUPUESTO]

## Quality Criteria

- [ ] Activation event is explicitly defined and instrumented. [DOC]
- [ ] Every step maps to progress toward activation (no orphan steps). [INFERENCIA]
- [ ] TTV is measurable before and after the change. [INFERENCIA]
- [ ] Evidence tags on all claims; output actionable and specific. [DOC]
- [ ] No redundancy or padding.

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do This Instead |
|-------------|-------------|-----------------|
| Feature tour as onboarding | Shows UI, not value; high skip rate | Drive to the first real action [INFERENCIA] |
| Signup = activation | Vanity metric; hides drop-off | Define a value-based activation event [DOC] |
| Mandatory full setup | Friction before any value | Defer non-blocking config [INFERENCIA] |
| Acting without understanding | Wastes effort on wrong solution | Think First (XIII) |
| Over-engineering | Complexity without value | Simple First (XIV) |
| Missing evidence tags | Claims without basis | Tag every assertion |

## Related Skills

- `first-use-onboarding` (cold-start / system onboarding), `empty-states`,
  `microcopy-writing`, `error-messaging`, `notification-ux`. [CONFIG]

## Usage

Example invocations:

- "/onboarding-ux" — Run the full onboarding ux workflow
- "onboarding ux on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs, analytics). [CONFIG]
- Requires a defined or definable activation event; if absent, surface it as the
  first gap before designing flows. [SUPUESTO]
- English-language output unless otherwise specified. [SUPUESTO]
- Does not cover retention/re-engagement loops or pricing/paywall UX. [SUPUESTO]
- Does not replace domain-expert judgment for final activation definition. [SUPUESTO]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding. |
| No analytics / unknown TTV | Proceed on qualitative flow review; mark numbers `[SUPUESTO]`, propose instrumentation. |
| Activation event undefined | Stop and propose 1–2 candidate events with rationale before flow design. [INFERENCIA] |
| Multi-persona product | Define activation per persona; do not force one flow on all. [INFERENCIA] |
| Conflicting requirements | Flag conflicts explicitly, propose resolution. |
| Out-of-scope request (retention, paywall) | Redirect to the appropriate skill or escalate. |

## Failure Modes

- Optimizing completion rate while retention drops → re-anchor on the value-based
  activation event, not step completion. [INFERENCIA]
- Adding "helpful" steps that raise TTV → every added step must remove a larger
  downstream drop-off or be cut. [INFERENCIA]
- Tour/checklist that users skip → replace with in-context guidance at the moment
  of need (empty states, inline microcopy). [SUPUESTO]

## Acceptance Criteria

- Activation event named, value-based, and instrumented end-to-end. [DOC]
- Chosen flow pattern justified against alternatives with a stated trade-off. [DOC]
- TTV and activation-rate baselines captured (or instrumentation proposed). [INFERENCIA]
- Counter-metric (retention of activated cohort) identified. [SUPUESTO]
- Every non-obvious claim carries one Alfa-core tag; no foreign taxonomy. [DOC]

## Examples

- SaaS doc tool: activation = "first doc shared", not signup. Replace 5-screen
  tour with empty-state + sample doc → drives the share action; TTV measured
  from signup to first share. [INFERENCIA]
- Config-heavy B2B: value blocked until integration connected → setup wizard with
  a short checklist; defer all non-blocking settings to post-activation. [INFERENCIA]
