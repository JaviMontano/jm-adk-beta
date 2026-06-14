<!-- distilled from alfa skills/meta-skill-creator -->
<!-- Create new 10x skills using the skill-forge protocol. Loads reference sub-repo, applies Trinity (Alfa-Atoms-Beta), validates with 10/10 rubric. [DOC] -->
# meta-skill-creator {Meta} (v1.1)

> **"Skills that create, review, search, and deploy other skills."**

## Purpose
Factory for new skills. Follows the skill-forge Trinity: load context (Alfa) → manufacture (Atoms) → verify (Beta). Every skill must score 10/10 before ship. [DOC]

**When to use:** `/jm:create-skill "skill description"`
**When NOT to use:** editing an existing skill (use skill-improver), or one-off prompts that will never be reused — the MOAT scaffold is overhead below ~2 reuses. [INFERENCIA]

## Core Principles
1. **Law of Context-First:** Read reference/ before writing. Order: knowledge_graph → best_practices → output_template → self_evaluation. Skipping it is the top cause of off-taxonomy skills. [DOC]
2. **Law of 10/10:** No skill ships below 10/10 on the self-evaluation rubric. A 9/10 is a failed build, not a near-miss — fix and re-score, never round up. [DOC]
3. **Law of MOAT:** Every skill gets SKILL.md + reference/ + prompts/ + examples/ + tests/. Trade-off: heavier than a bare SKILL.md, justified because reference/ + tests/ are what make a skill reviewable and improvable later. [INFERENCIA]

## Core Process
### Phase 1: Context Loading
1. Read skill-forge reference files (knowledge_graph, best_practices, output_template, self_evaluation). [DOC]
2. Decompose user request into the knowledge graph taxonomy. If it maps to no node, STOP and propose adding the node — do not invent an ad-hoc category. [SUPUESTO]

### Phase 2: Manufacture
1. Draft SKILL.md using output_template scaffold. [DOC]
2. Create reference/ files if skill has >3 laws or >5 steps; otherwise inline to avoid empty stubs. [DOC]
3. Create at least one prompt in prompts/ and one example in examples/. [DOC]

### Phase 3: Verify
1. Score against self_evaluation rubric — must achieve 10/10. [DOC]
2. Run 5 adversarial tests (ambiguity, edge case, contradiction, stress, security). [DOC]
3. Update skills_index.json via meta-skill-indexer. [DOC]

## Worked Example
Input: `/jm:create-skill "summarize a PR diff into release notes"`. [DOC]
1. **Alfa** — load 4 reference files; map request to taxonomy node `dev-workflow/changelog`. [INFERENCIA]
2. **Atoms** — draft SKILL.md; 2 laws + 4 steps → inline reference (under thresholds); add `prompts/summarize-diff.md` + `examples/sample-release-notes.md`. [INFERENCIA]
3. **Beta** — score 10/10; adversarial set catches an empty-diff case → add handling; index. Result: shippable skill, no human edit. [INFERENCIA]

## Validation Gate
- [ ] Operation completed and self-evaluation scored exactly 10/10
- [ ] skills_index.json updated (and re-read to confirm the new entry resolves)
- [ ] context.json reflects current state
- [ ] No stack violations (R-002, R-003)
- [ ] All 5 adversarial tests pass, including the security probe

## 4. Self-Correction Triggers
> [!WARNING]
> IF skills_index.json is stale THEN regenerate before searching.
> IF deploying a skill with status != production THEN WARN user.
> IF self-evaluation < 10/10 THEN fix and re-score; never ship a partial.
> IF the request maps to no taxonomy node THEN stop and propose the node.

## Usage

Example invocations:

- "/meta-skill-creator" — Run the full meta skill creator workflow
- "meta skill creator on this project" — Apply to current context

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs) and the skill-forge reference sub-repo. [SUPUESTO]
- Requires English-language output unless otherwise specified. [DOC]
- Does not replace domain expert judgment for final decisions. [DOC]
- **Anti-scope:** does not edit/refactor existing skills, deploy to production registries, or author cross-skill orchestration — those are separate skills. [DOC]
- Single skill per invocation; batch creation is out of scope (loop the command instead). [SUPUESTO]

## Edge Cases & Failure Modes

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding; never auto-fill a skill spec. |
| Conflicting requirements | Flag conflicts explicitly, propose resolution, wait for confirmation. |
| Out-of-scope request | Redirect to appropriate skill or escalate. |
| Request maps to no taxonomy node | Stop; propose adding the node before manufacturing. [SUPUESTO] |
| reference/ files missing or unreadable | Abort Phase 1; do not manufacture from memory — risks off-taxonomy output. [INFERENCIA] |
| Skill name collides with existing index entry | Halt; prompt for rename or confirm intentional supersede. [INFERENCIA] |
| Self-evaluation stalls below 10/10 | Surface the failing rubric dimensions; do not ship a partial skill. |
| skills_index.json write fails | Treat skill as not-shipped; the un-indexed skill is undiscoverable. [INFERENCIA] |

## Acceptance Criteria
- A new skill directory exists with all five MOAT components populated (no empty stubs). [DOC]
- Self-evaluation recorded at 10/10 with the rubric snapshot retained. [DOC]
- skills_index.json contains a resolvable entry for the new skill. [INFERENCIA]
- All claims in the generated SKILL.md carry a single tag from the Alfa core family (see references/verification-tags.md). [DOC]
