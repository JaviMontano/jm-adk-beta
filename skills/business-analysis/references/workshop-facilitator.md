<!-- distilled from alfa skills/workshop-facilitator -->
<!-- Workshop design — event storming, impact mapping, user story mapping, design sprints. [EXPLICIT] -->
# Workshop Facilitator: Collaborative Discovery & Design Techniques

Workshop facilitation designs and runs structured collaborative sessions to extract knowledge, align stakeholders, and produce actionable artifacts. Covers technique selection, session design, facilitation guides, and synthesis — from event storming to design sprints. [EXPLICIT]

## Principio Rector

> Un taller mal facilitado no solo desperdicia tiempo — destruye la confianza del equipo en los procesos colaborativos. La facilitación excelente es la diferencia entre alineamiento genuino y consenso superficial.

1. **Descubrimiento colaborativo sobre presentación unilateral.** El conocimiento tácito solo emerge cuando las personas hacen, no cuando escuchan. Cada minuto de un taller debe diseñarse para extraer, no para transmitir. [EXPLICIT]
2. **Estructura al servicio de la creatividad.** Los time-boxes, las técnicas y las reglas de participación no limitan la creatividad — la potencian. Sin estructura, dominan las voces más fuertes y se pierden las ideas más valiosas. [EXPLICIT]
3. **Artefactos vivos sobre actas muertas.** El valor de un taller no está en el documento de síntesis — está en los modelos mentales compartidos que se construyen. Los artefactos deben ser herramientas de trabajo, no archivos de evidencia. [EXPLICIT]

## Inputs

The user provides a project or workshop goal as `$ARGUMENTS`. Parse `$1` as the **project/workshop name** used throughout all output artifacts. [EXPLICIT]

Before generating workshop design, detect project context:

```
find . -name "*.md" -o -name "*.miro" -o -name "*.figjam" -o -name "*.pdf" -o -name "workshop*" | head -20
```

**Parameters:**
- `{MODO}`: `piloto-auto` (default) | `desatendido` | `supervisado` | `paso-a-paso`
  - **piloto-auto**: Auto para diseño de agenda y selección de técnicas, HITL para validación de participantes y decisiones de formato. [EXPLICIT]
  - **desatendido**: Cero interrupciones. Diseño completo auto-generado. Supuestos documentados. [EXPLICIT]
  - **supervisado**: Autónomo con checkpoints en selección de técnica y diseño final. [EXPLICIT]
  - **paso-a-paso**: Confirma antes de cada decisión de diseño. [EXPLICIT]
- `{FORMATO}`: `markdown` (default) | `html` | `dual`
- `{VARIANTE}`: `ejecutiva` (~40%) | `técnica` (full, default)

## When to Use

- Kicking off a new project and needing shared understanding
- Exploring a complex domain before designing solutions
- Aligning cross-functional teams on scope, priorities, or architecture
- Breaking down epics into deliverable slices
- Running rapid prototyping and validation cycles
- Resolving conflicting mental models among team members
- Extracting tacit knowledge from domain experts

## Delivery Structure: 6 Sections

### S1: Workshop Selection & Design

Matches the right technique to the workshop goal, selects participants, and designs the agenda. [EXPLICIT]

**Technique selection matrix:**

| Goal signal | Technique | Min participants | Typical duration |
|---|---|---|---|
| "Understand the domain" | Event Storming | 2+ domain experts | 3-6h |
| "Define impact and scope" | Impact Mapping | 1 goal owner + delivery | 2-3h |
| "Plan releases and slices" | User Story Mapping | PO + 3-5 team | 3-4h |
| "Prototype and validate" | Design Sprint | 5-7 cross-functional | 1-5 days |
| "Prioritize and decide" | Dot Voting, MoSCoW, WSJF | any | 30-60 min |
| "Retrospect and improve" | Sailboat, 4Ls, Start/Stop/Continue | the team | 60-90 min |

**Worked example (selection):** Goal = "reduce checkout abandonment, unclear why." Domain is known but the failure mechanism is not, and a clear measurable target exists → start with **Impact Mapping** (goal → actors → impacts → deliverables to test the abandonment hypotheses), not Event Storming (domain already understood) nor Design Sprint (no prototype-worthy solution yet). [INFERENCIA]

**Sticky-note color legend (Event Storming canon, reuse across artifacts):** orange = domain event (past tense), blue = command, yellow = aggregate, pink = hot spot / external system, purple = policy, green = read model / view. Fix the legend on the board before starting; color drift mid-session destroys the timeline's readability. [EXPLICIT]

**Core facilitation principles:**
- **Diverge-Converge rhythm:** Every activity follows Generate > Cluster > Vote > Decide. Never skip clustering.
- **Silent-before-spoken rule:** Start ideation with 5-10 min of silent individual writing. Solo ideation produces broader, more creative input. Discussion follows to combine and build.
- **Energizer techniques:** Quick creative prompts at session start and after breaks to reset attention.

**Key decisions (with justified trade-offs):**
- **Duration** — half-day caps cognitive load at ~1 technique; full-day fits 2-3 with breaks; multi-day only for Design Sprints. Trade-off: longer sessions deepen output but decay attention after 90 min without a break. [EXPLICIT]
- **In-person vs. remote vs. hybrid** — hybrid is the worst default: remote participants become second-class. Choose all-in-person or all-remote unless tooling guarantees equal floor. [INFERENCIA]
- **Participant count** — 5-8 ideal; below 4 loses divergence, above 8 needs breakouts (each breakout needs a sub-facilitator). [EXPLICIT]
- **Facilitation style** — structured (strict time-boxes) for mixed-seniority or conflict-prone groups; emergent (follow the energy) only with a mature, trusting team. [INFERENCIA]

**Standard agenda block (reusable unit, ~50 min):** 5 min frame the question → 7 min silent individual generation → 10 min round-robin share (no debate) → 10 min cluster affinities → 8 min dot-vote → 7 min decide + capture owner → 3 min buffer. Repeat per topic; insert a break every two blocks. [INFERENCIA]

### S2: Event Storming

Discovers domain knowledge by exploring events, commands, aggregates, and bounded contexts. [EXPLICIT]

**Includes:**
- Domain event discovery: past-tense verbs on orange stickies (OrderPlaced, PaymentReceived)
- Timeline construction: events arranged chronologically left-to-right
- Command identification: what triggers each event (blue stickies)
- Aggregate clustering: grouping events around domain entities (yellow stickies)
- Bounded context identification: drawing boundaries around related aggregates
- Hot spot marking: conflicts, unknowns, areas needing deeper exploration (pink stickies)
- Temporal modeling: parallel streams, eventual consistency points, saga boundaries
- Policy identification: automated reactions between events ("when X happens, then Y")

**Failure modes:** events written as present tense or as commands (must be past-tense facts); jumping to aggregates before the timeline is complete (model the flow first); one expert dominating the wall (enforce silent-write start). **Done when:** timeline has no unexplained gaps, every hot spot has an owner, bounded-context boundaries are drawn and named. [INFERENCIA]

### S3: Impact Mapping

Connects business goals to deliverables through actors and impacts. [EXPLICIT]

**Includes:**
- Goal definition: measurable business objective at the center
- Actor identification: who can help or hinder the goal
- Impact discovery: what behavior changes in actors would achieve the goal
- Deliverable brainstorming: what can we build/do to create those impacts
- Assumption testing: which impacts are assumptions vs. validated knowledge
- Scope negotiation: using the map to cut scope while preserving goal achievement

**Worked example:** Goal = "+15% trial-to-paid in Q3" → Actor "trial admin" → Impact "completes setup in <10 min" → Deliverable "guided onboarding checklist." The deliverable is justified only by its branch back to the measurable goal; orphan deliverables (no actor/impact path) get cut. **Failure mode:** goal stated as a feature ("ship onboarding"), not an outcome — re-anchor on a metric before mapping. [INFERENCIA]

### S4: User Story Mapping

Organizes user activities into a backbone and plans releases as horizontal slices. [EXPLICIT]

**Includes:**
- Backbone construction: high-level user activities across the top (left to right = user journey)
- Walking skeleton: the minimum set of stories that deliver end-to-end value
- Vertical slicing: each column is an activity; stories arranged top-to-bottom by priority
- Release planning: horizontal lines across the map define release boundaries
- MVP identification: the thinnest horizontal slice that delivers a testable product
- Dependency flagging: stories that block others, requiring sequencing

**Failure mode:** the first release line drawn so high it is no longer a *walking* skeleton (can't be demoed end-to-end). Force the slice to touch every backbone activity at least once. [INFERENCIA]

### S5: Design Sprint

Compressed prototyping and validation cycle — understand, sketch, decide, prototype, test. [EXPLICIT]

**Includes:**
- Day 1 — Understand: map the challenge, interview experts, set sprint goal, pick target
- Day 2 — Sketch: lightning demos, individual solution sketching, Crazy 8s, solution sketch
- Day 3 — Decide: art museum, heat map voting, speed critique, storyboard the winner
- Day 4 — Prototype: realistic facade prototype (Figma, HTML, slide deck), assign roles
- Day 5 — Test: 5 user interviews, structured observation, pattern identification
- Compressed formats: 3-day sprint, 1-day lightning sprint, async sprint

**Why 5 testers:** ~85% of usability problems surface by the fifth user; more testers yield diminishing returns for a single prototype. **Failure mode:** prototype fidelity too high (team defends sunk effort) or too low (testers can't react) — aim for a believable facade, not working code. **Decider must be present Day 3**; a sprint without a single empowered decider produces a storyboard nobody owns. [INFERENCIA]

### S6: Synthesis & Handoff

Consolidates workshop outputs into actionable artifacts and establishes follow-up cadence. [EXPLICIT]

**Includes:**
- Insight consolidation: key findings, decisions made, open questions
- Artifact packaging: photographs, digital boards, structured documents
- Action item extraction: who does what by when
- Decision log: what was decided, by whom, with what rationale
- Follow-up cadence: next workshop, check-in meeting, async review
- Knowledge transfer: how to bring non-attendees up to speed

## Trade-off Matrix

| Decision | Enables | Constrains | When to Use |
|---|---|---|---|
| **Event Storming** | Deep domain understanding, DDD alignment | Requires domain experts, time-intensive | Complex domains, DDD projects |
| **Impact Mapping** | Goal alignment, scope negotiation | Abstract, requires clear business goal | Strategy-to-execution alignment |
| **User Story Mapping** | Release planning, shared understanding | Requires known user journey | Agile planning, MVP definition |
| **Design Sprint** | Fast validation, reduced risk | Requires 5 days, facilitator skill | New products, risky features |
| **Full-Day Workshop** | Deep exploration, relationship building | Calendar cost, energy management | Kickoffs, complex problems |
| **Compressed Format** | Time-efficient, lower commitment | Shallow output, risk of rushing | Follow-ups, well-scoped questions |

## Assumptions & Limits

- Workshop participants are available and empowered to contribute
- Facilitator has access to collaboration tools (physical or digital)
- Workshop goal is defined, even if broadly
- Outputs will be used — workshops without follow-through waste trust
- Does not produce technical specifications — produces inputs for them
- Cannot force stakeholder alignment — surfaces disagreements, doesn't resolve politics

## Edge Cases

**Remote-Only Team:** Use Miro, FigJam, or Excalidraw. Shorter sessions (2-3 hours max). More structured facilitation. Breakout rooms for parallel work. Maintain dual-agenda: external schedule for participants and internal facilitator script.

**Remote Facilitation Anti-Patterns (avoid):**
- Death by screen-share: make participants DO things on the board
- Phantom consensus: silence does not equal agreement — use explicit polls
- Breakout abandonment: always provide clear instructions, time limit, and a template
- Energy blindness: build breaks at 40 min intervals
- Over-tooling: consolidate to one collaboration surface

**Large Group (15+):** Split into breakout groups of 4-6. Assign sub-facilitators. Gallery walks and dot voting for convergence.

**Conflicting Stakeholders:** Surface conflicts explicitly. Use structured techniques (silent brainstorming, anonymous voting) to reduce power dynamics. Facilitator must be neutral.

**Domain Experts Unavailable:** Event storming without domain experts produces developer assumptions. Either postpone or run preliminary session marking assumptions explicitly.

**Workshop Fatigue:** Demonstrate follow-through. Keep session shorter, action-oriented. Show how prior outputs were used.

**HiPPO in the room (highest-paid person's opinion anchors the group):** route ideation through silent-write + anonymous voting so the first idea on the wall isn't theirs; seat the senior person to listen, not open. [INFERENCIA]

**Goal drifts mid-session:** if the real problem surfaces is different from the stated goal, stop and re-contract explicitly rather than finishing a session that answers the wrong question. Park the original goal visibly; don't silently abandon it. [INFERENCIA]

## Pre-Work Packet (distribute ≥48h before)

Anti-scope: do not start a session whose pre-work was skipped — cold rooms waste the first hour. [INFERENCIA]

- **Goal + non-goals:** one sentence each. Non-goals prevent scope creep on the day.
- **Technique + why:** so participants arrive in the right mode (diverge vs. decide).
- **Roles requested:** who must attend (decider, domain expert) vs. optional.
- **Pre-read:** ≤2 pages or 1 diagram; never a 30-page deck.
- **One async question** answered before arrival, to prime thinking.
- **Logistics:** board link, break schedule, "you will be asked to write, not just talk."

## Validation Gate

Before finalizing delivery, verify:

- [ ] Workshop technique matches the stated goal
- [ ] Participant list includes the right roles (domain experts, decision-makers)
- [ ] Agenda is time-boxed with clear activities per block
- [ ] Pre-work is defined and distributed
- [ ] Success criteria are explicit and measurable
- [ ] Facilitation approach accounts for remote/in-person dynamics
- [ ] Synthesis plan is defined (who packages, when, in what format)
- [ ] Action items have owners and deadlines
- [ ] Follow-up cadence is agreed upon
- [ ] Workshop outputs feed into downstream activities

**Measurable acceptance criteria (a design passes only if all hold):** every agenda block has an owner, a time-box, and a named output artifact; ≥1 convergence step (vote/decide) per divergence step; participant list covers every role the technique requires (e.g., Event Storming has ≥1 domain expert, Design Sprint has 1 decider); ≤8 active participants per facilitator or a sub-facilitator is assigned; every decision in the log carries who + rationale; every action item carries owner + date. [INFERENCIA]

## Output Format Protocol

| Format | Default | Description |
|--------|---------|-------------|
| `markdown` | ✅ | Rich Markdown + Mermaid diagrams. Token-efficient. |
| `html` | On demand | Branded HTML (Design System). Visual impact. |
| `dual` | On demand | Both formats. |

Default output is Markdown with embedded Mermaid diagrams. HTML generation requires explicit `{FORMATO}=html` parameter. [EXPLICIT]

## Output Artifact

**Primary:** `A-01_Workshop_Design.html` — Technique selection rationale, detailed agenda, facilitation guide, participant briefing, synthesis template, action item tracker.

### Diagrams (Mermaid)
- Flowchart: workshop agenda flow with decision points
- Mindmap: workshop outputs and their connections to deliverables

---
**Author:** Javier Montano | **Last updated:** 2026-03-12
