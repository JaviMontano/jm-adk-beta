---
name: ux-research
version: 1.0.0
description: "User research and validation router: route to interviews, surveys, usability testing, or prototyping. Topics: prototyping, survey-design, user-research, user-testing."
params:
  topic:
    enum: [prototyping, survey-design, user-research, user-testing]
    required: true
    infer: from user request; ask only if ambiguous
  depth:
    enum: [quick, deep]
    default: quick
routes:
  prototyping: references/prototyping.md
  survey-design: references/survey-design.md
  user-research: references/user-research.md
  user-testing: references/user-testing.md
---

# ux-research

Router skill. Resolve `topic`, then Read EXACTLY ONE playbook from `routes:`.
Never load the whole cluster — one route per invocation keeps context lean. [INFERENCIA]

## When to use
A UX/discovery task that maps to one route. NOT for build/UI work (frontend
skills), product strategy, or analytics instrumentation. [INFERENCIA]

## Inputs → Outputs
- **In**: `topic` (required), `depth` (quick|deep), the request + any artifacts. [DOC]
- **Out**: the routed playbook's deliverable (interview guide, survey, test plan,
  prototype spec) with evidence tags and an explicit next step. [DOC]

## Route selection
- **user-research** — generative: interviews, contextual inquiry, "why/what do users need". [DOC]
- **survey-design** — quantitative attitudes/segmentation at scale. [DOC]
- **user-testing** — evaluate an existing flow/prototype: usability, task success. [DOC]
- **prototyping** — produce a testable artifact before build. [DOC]
Two topics plausible → ask one disambiguating question; never run two routes. [INFERENCIA]

## Depth & spine
`deep` → apply playbook exhaustively, verify each step; `quick` → essentials,
single pass. Spine: Discover → Analyze → Execute → Validate. [DOC]

## Validation gate (before "done")
- Exactly one playbook was read and followed. [DOC]
- Output respects constitution v6.0.0 + script-first rule. [CONFIG]
- Every non-obvious claim carries one Alfa-core tag (references/verification-tags.md). [DOC]
- Each `[SUPUESTO]` is paired with a verification step. [DOC]
- Score against `assets/quality-rubric.json` (universal + route criteria). [CONFIG]

## Anti-patterns
Loading >1 route; inventing a topic outside the enum; skipping tags; emitting
a deliverable with no next step; doing the build instead of the research. [INFERENCIA]