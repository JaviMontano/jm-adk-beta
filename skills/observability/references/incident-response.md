<!-- distilled from alfa skills/incident-response -->
<!-- > -->
# Incident Response
> "Method over hacks."
## TL;DR
Severity-driven incident lifecycle: classify → declare → mitigate → resolve → learn. Ships a severity matrix, role assignments, comms cadence, and a blameless postmortem template. [EXPLICIT]

## Severity Matrix
Classify on customer impact, not effort. Pick the highest row that fits; ambiguous → round up. [INFERENCIA]

| Sev | Trigger | Response target | Comms cadence | Postmortem |
|-----|---------|-----------------|---------------|------------|
| SEV1 | Full outage, data loss, security breach | Ack <5min, all-hands | Every 30min | Required |
| SEV2 | Major feature down, severe degradation, no workaround | Ack <15min | Every 60min | Required |
| SEV3 | Partial/degraded, workaround exists | Next business hour | At resolution | Optional |
| SEV4 | Cosmetic, low-impact, single user | Backlog | None | No |

## Lifecycle
1. **Detect** — Alert, customer report, or canary fires. Capture first-seen timestamp. [DOC]
2. **Declare** — Assign Incident Commander (IC) + Scribe; open the channel; set severity. One IC owns decisions — do not split command. [DOC]
3. **Mitigate** — Stop the bleeding before root-causing. Prefer reversible actions: roll back, feature-flag off, scale out, failover. [INFERENCIA]
4. **Resolve** — Confirm signals green for ≥1 cadence window; downgrade severity stepwise, never skip to closed. [INFERENCIA]
5. **Learn** — Within 48h for SEV1/2: blameless postmortem, dated action items with owners. [DOC]

## Roles
- **IC** — decides, delegates, holds the timeline. Not the hands-on fixer. [DOC]
- **Ops/Fixer** — executes mitigations, reports back to IC only. [DOC]
- **Scribe** — timestamps every action/decision in the channel for the postmortem. [DOC]
- **Comms** — owns stakeholder/status-page updates on cadence. [SUPUESTO]

## Postmortem Template
- **Summary** — one paragraph: what broke, blast radius, duration.
- **Timeline** — UTC, detect → declare → mitigate → resolve, with who/what.
- **Root cause** — contributing factors, not a single person. [DOC]
- **Detection gap** — why it wasn't caught sooner.
- **Action items** — each owned + dated; tracked to closure, not just listed. [INFERENCIA]

## Acceptance Criteria
- [ ] Severity assigned from the matrix, not by gut feel
- [ ] IC + Scribe named before mitigation starts
- [ ] Mitigation precedes root-cause analysis
- [ ] Resolution confirmed across a full cadence window before close
- [ ] SEV1/2 postmortem has dated, owned action items
- [ ] Evidence tags applied; output blameless and Constitution-compliant

## Usage

Example invocations:

- "/incident-response" — Run the full incident response workflow
- "incident response on this project" — Apply to current context, infer severity from impact

## Assumptions & Limits

- Assumes alerting/observability exists to detect incidents; this skill does not stand up monitoring [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace IC judgment or on-call escalation policy for final decisions [EXPLICIT]
- Anti-scope: not a paging/on-call scheduler, not a status-page integration, not a chaos-engineering harness [SUPUESTO]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request impact + first-seen time before classifying |
| Unclear severity | Round up; downgrade once impact is bounded |
| Multiple concurrent incidents | One IC each; designate a cross-incident coordinator |
| Mitigation makes it worse | Roll back the mitigation first; IC re-evaluates |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
