# Market Intelligence Deliverable — {{TOPIC}}

> Snapshot as of {{DATE}}. Point-in-time; competitor and regulatory facts decay.

## Routing decision

- **Topic:** {{TOPIC}} (∈ enum)
- **Depth:** {{quick | deep}}
- **Playbook loaded:** references/{{TOPIC}}.md
- **Evidence family:** {{Alfa core | OSINT [EXPLICIT]/[INFERRED]/[OPEN] | CI/benchmark local}}
- **Why this topic:** {{one line — the cue that resolved routing}}

## Executive summary

- {{3–5 tagged bullets: the decision this informs and the headline finding}}

## Discover — inputs & provenance

| Input | Source (URL) | As-of date | Tag |
|---|---|---|---|
| {{e.g. competitor pricing page}} | {{url}} | {{YYYY-MM-DD}} | {{[DOC]}} |
| {{e.g. ICP / segment}} | {{artifact}} | {{date}} | {{[CONFIG]}} |

## Analyze — core artifact

> Use the artifact the loaded playbook requires. Examples:

**Competitive-intelligence / positioning — comparison matrix**

| Axis / Capability | Us | Comp-A | Comp-B | Evidence |
|---|---|---|---|---|
| {{buyer criterion}} | {{Yes/Partial/No/Unknown}} | {{...}} | {{...}} | {{[DOC] src+date}} |

**Benchmarking — gap table**

| Metric | Subject | Reference (src + date) | Gap (abs / %) | Impact × closability |
|---|---|---|---|---|

**Partnership — fit score**

| Candidate | Overlap (.30) | Reach (.20) | Fit (.20) | Effort (.15) | Reputation (.15) | Score | Verdict |
|---|---|---|---|---|---|---|---|

**Pricing — tier architecture** (ranges/placeholders only, no concrete price)

| Tier | Segment | Anchor role | Value-metric framing |
|---|---|---|---|

**Market-intelligence — entity + sizing**

| Field | Value | Tag |
|---|---|---|
| Entity type | {{company/person/territory/sector}} | [EXPLICIT] |
| TAM / SAM / SOM | {{figure + vintage year}} | {{[INFERRED]}} |

## Findings

- {{Each finding one line, exactly one evidence tag, actionable}}

## Recommendations / next steps

1. {{actionable, tied to a finding}}

## Evidence summary

- {{% by tag type}}. WARNING banner if >30% [ASSUMPTION]/[OPEN]. [OPEN] items
  list a resolution path below.

| [OPEN] / gap | How to resolve |
|---|---|

## Validation (run on depth=deep)

- [ ] One playbook loaded; topic ∈ enum
- [ ] Every claim tagged, single family, no mixing
- [ ] No invented price; single brand; no PII; not green-as-success
- [ ] Playbook acceptance criteria satisfied
