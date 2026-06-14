<!-- distilled from alfa skills/workshop-design -->
<!-- > -->
# Workshop Design

> "None of us is as smart as all of us." — Ken Blanchard

## TL;DR

Designs structured collaborative workshops — event storming, impact mapping, design sprints, inception — with timeboxed agendas, facilitation scripts, and artifact templates. Use to align a group, explore a domain, or make collaborative decisions efficiently.

## Scope & Anti-Scope

- **In scope**: agenda design, format selection, facilitation guide, artifact templates, pre-work, energizers.
- **Out of scope**: running the live session (see `workshop-facilitator`), producing the downstream deliverable itself, scheduling/logistics booking, recruiting participants.

## Assumptions

- A named objective and at least a draft participant list exist before design starts. If absent, run Step 1 first and do not proceed without them.
- A digital whiteboard (Miro/FigJam) or physical space is available; remote/hybrid is the default unless stated otherwise.

## Procedure

### Step 1: Discover
- Define the workshop objective as a decision or artifact (the exit condition), not a topic.
- Identify participants: roles, count, experience level, remote/in-person mix. **Cap working groups at 7–8**; split larger groups into parallel tracks with a shared readout.
- Assess constraints: duration, tools (Miro, FigJam, physical), prep lead time, time zones.

### Step 2: Analyze — select format by objective

| Format | Best for | Typical length | Trade-off |
|--------|----------|----------------|-----------|
| **Event Storming** | Domain/process discovery | 2–4 h | High insight density; needs a domain expert present or it stalls. |
| **Impact Mapping** | Goal→actors→impacts→deliverables alignment | 1.5–3 h | Fast scope alignment; weak on technical/process depth. |
| **Design Sprint** | Rapid prototyping + user validation | 5 days (or 2-day compressed) | Strong validation; expensive in calendar/headcount, needs real users to test. |
| **Inception** | Project kickoff: scope, risks, team agreements | 1–2 days | Broad shared context; shallow on any single domain. |

- When objectives are mixed, pick the **dominant** one and sequence the rest as later sessions — do not merge formats into one bloated agenda.
- Design the agenda with timeboxed activities, explicit synthesis steps, and energy management (vary divergent/convergent, sitting/standing).

### Step 3: Execute
- Produce a facilitation guide: per-activity timing, verbatim instructions, transition scripts, and a **contingency activity** for over/under-runs.
- Create and **dry-run** artifact templates (boards, canvases, voting sheets) before the session.
- Write pre-work for participants; gate the session on critical pre-work being done.
- Design warm-ups and energizers sized to group and culture.

### Step 4: Validate
- Verify the agenda achieves the objective within the timebox, including buffer.
- Confirm activities match participant experience level.
- Check remote/hybrid participants have equal voice (parallel digital input, not just a camera).
- Validate every output maps to a named downstream deliverable; cut activities whose output goes nowhere.

## Quality Criteria

- [ ] Objective stated as a decision/artifact with an explicit exit condition.
- [ ] Agenda timeboxed with ≥15% buffer and at least one contingency activity.
- [ ] Facilitation guide includes transition scripts and per-activity owner.
- [ ] Artifact templates prepared and dry-run.
- [ ] Each output traced to a downstream deliverable.
- [ ] Provenance/evidence tags applied to all claims (see `references/verification-tags.md`).

## Edge Cases

- **Hybrid sessions**: default to all-digital artifacts so remote and in-person share one source of truth; avoid physical-only stickies.
- **Cross-timezone**: prefer two shorter async-bridged sessions over one session outside someone's working hours.
- **Hostile/misaligned stakeholders**: front-load an objective-alignment activity; do not start divergent work until alignment is confirmed.
- **No domain expert available** for Event Storming: defer or switch to Impact Mapping rather than guessing the domain.

## Anti-Patterns

- **Death by sticky notes** → every divergent activity is followed by an explicit synthesis/convergence step.
- **No follow-up** → close with owner + due date per output; the session is not done until actions are assigned.
- **Facilitator-as-participant** → separate the facilitator from content contributors; if the facilitator holds key content, add a co-facilitator.
- **Over-stuffed agenda** → cut to the dominant objective; a workshop that ends one activity early beats one that runs out of time mid-synthesis.

## Worked Example

Objective: "Decide the bounded contexts for the new claims platform." Participants: 6 (2 domain experts, 2 engineers, 1 PO, 1 facilitator), 3 h remote. Format: **Event Storming** (domain discovery, expert present). Agenda: chaotic exploration (40 m) → timeline enforcement (30 m) → break → pivotal-event identification (30 m) → context boundary voting (30 m) → synthesis + owner assignment (20 m). Output: a Miro context map feeding the `architecture-tobe` deliverable, owned by the PO, due +3 days.

## Related Skills

- `workshop-facilitator` — runs the live session this skill designs
- `domain-driven-design` — event storming is a DDD discovery technique
- `stakeholder-mapping` — identifies who should participate
- `flow-mapping` — captures process flows discovered during workshops
