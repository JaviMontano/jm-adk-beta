<!-- distilled from alfa skills/iikit-00-constitution -->
<!-- >- -->
# Intent Integrity Kit Constitution

Create or update the project constitution at `CONSTITUTION.md` — the governing principles for specification-driven development.

## Scope

**MUST contain**: governance principles, non-negotiable development rules, quality standards, amendment procedures, compliance expectations, quality governance section referencing QA-PLAN.md.

**Quality Governance section** (MUST be included in every constitution):
```markdown
### Quality Governance
QA-PLAN.md is the authoritative quality artifact for this project. It aggregates:
- Global Definition of Done and acceptance criteria (derived from this constitution)
- Per-feature qa/ subdirectories (created emergently by /sdd:spec and /sdd:test)
- Quality gate status (updated by /sdd:analyze)
- Feature quality registry (AC coverage, test coverage, checklist completion)
Run /sdd:qa to generate or refresh. Auto-invoked by /sdd:analyze.
```

**MUST NOT contain**: technology stack, frameworks, databases, implementation details, specific tools or versions. These belong in `/iikit-02-plan`. See `phase-separation-rules.md`.

**Anti-scope** (explicitly out of bounds, do not generate): feature requirements (→ `/iikit-01-specify`), task breakdowns (→ `/iikit-05-tasks`), test plans (→ `/iikit-04-testify`), CI/deploy config, license text, code of conduct. A constitution is *principles*, not *plans*. [EXPLICIT]

**Decision — why principles stay tech-agnostic**: separating governance from stack lets `/iikit-02-plan` swap implementations without amending the constitution (a MAJOR bump). Trade-off: principles read more abstractly and need rationale to stay testable; mitigated by requiring each principle declare a checkable rule. [EXPLICIT]

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Prerequisites Check

1. **Check PREMISE.md exists**: `test -f PREMISE.md`. If missing: ERROR — "PREMISE.md not found. Run `/iikit-core init` first to create it." Do NOT proceed without PREMISE.md.
2. **Validate PREMISE.md**:
   ```bash
   bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/validate-premise.sh --json
   ```
   If FAIL (missing sections or placeholders): ERROR — show details, suggest re-running init.
3. Check if constitution exists: `cat CONSTITUTION.md 2>/dev/null || echo "NO_CONSTITUTION"`
4. If missing, copy from `constitution-template.md`

**Gate decision — fail closed**: any prerequisite miss (no PREMISE.md, validation FAIL) STOPS the workflow with a remediation message; never auto-create PREMISE.md or proceed on a partial premise. Rationale: the constitution inherits scope and intent from PREMISE.md — proceeding without it produces a constitution that silently contradicts the project's actual intent, the exact failure this kit exists to prevent. [EXPLICIT]

## Execution Flow

1. **Load existing constitution** — identify placeholder tokens `[ALL_CAPS_IDENTIFIER]`. Adapt to user's needs (more or fewer principles than template).

2. **Collect values for placeholders**:
   - From user input, or infer from repo context
   - `RATIFICATION_DATE`: original adoption date
   - `LAST_AMENDED_DATE`: today if changes made
   - `CONSTITUTION_VERSION`: semver (MAJOR: principle removal/redefinition, MINOR: new principle, PATCH: clarifications)

3. **Draft content**: replace all placeholders, preserve heading hierarchy, ensure each principle has name + rules + rationale, governance section covers amendment/versioning/compliance.

4. **Consistency check**: validate against `plan-template.md`, `spec-template.md`, `tasks-template.md`.

5. **Sync Impact Report** (HTML comment at top): version change, modified principles, added/removed sections, follow-up TODOs.

6. **Validate**: no remaining bracket tokens, version matches report, dates in ISO format, principles are declarative and testable. Constitution MUST have at least 3 principles — if fewer, add more based on the project context.

7. **Phase separation validation**: scan for technology-specific content per `phase-separation-rules.md`. Auto-fix violations, re-validate until clean.

8. **Write** to `CONSTITUTION.md`

9. **Store TDD determination** in `.specify/context.json` so all skills read from here instead of re-parsing the constitution:
   ```bash
   TDD_DET=$(bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/testify-tdd.sh get-tdd-determination "CONSTITUTION.md")
   ```
   Write to `.specify/context.json` using `jq` (merge, don't overwrite):
   ```bash
   jq --arg det "$TDD_DET" '. + {tdd_determination: $det}' .specify/context.json > .specify/context.json.tmp && mv .specify/context.json.tmp .specify/context.json
   ```
   If `.specify/context.json` doesn't exist, create it: `echo '{}' | jq --arg det "$TDD_DET" '{tdd_determination: $det}' > .specify/context.json`

10. **Git init** (if needed): `git init` to ensure project isolation

11. **Commit**: `git add CONSTITUTION.md .specify/context.json && git commit -m "Add project constitution"`

12. **Dashboard Refresh** (optional, never blocks):
```bash
bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/generate-dashboard-safe.sh
```
Windows: `pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/generate-dashboard-safe.ps1`

13. **Report**: version, bump rationale, TDD determination, git status, suggested next steps

### Versioning — worked example

| Change made | Bump | Resulting version (from 1.2.0) |
|---|---|---|
| Reworded a principle for clarity, no rule change | PATCH | 1.2.1 |
| Added a new principle | MINOR | 1.3.0 |
| Removed a principle or redefined its rule | MAJOR | 2.0.0 |

First-ever ratification is `1.0.0` with `RATIFICATION_DATE = LAST_AMENDED_DATE = today`. When in doubt between two bump levels, choose the higher — under-bumping hides a breaking change from downstream `/iikit-02-plan` consumers. [EXPLICIT]

### Failure modes

| Failure | Detection | Handling |
|---|---|---|
| Placeholder token survives to output (`[ALL_CAPS]`) | Step 6 bracket scan | Block write; list each token; collect value or remove principle |
| Version in body ≠ Sync Impact Report | Step 6 cross-check | Reconcile to the intended bump before writing |
| Tech-specific content leaks in (stack, tool, version) | Step 7 scan | Auto-fix, re-validate until clean; if irreducible, move to plan phase |
| Fewer than 3 principles | Step 6 count | Derive additional principles from PREMISE.md / repo context |
| `.specify/context.json` malformed or absent | Step 9 `jq` | Create with `echo '{}'`; merge, never overwrite |

## Formatting

- Markdown headings per template, lines <100 chars, single blank line between sections, no trailing whitespace.

## Next Steps

Run: `bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/next-step.sh --phase 00 --json`
Windows: `pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/next-step.ps1 -Phase 00 -Json`

Parse the JSON and present:
1. If `clear_after` is true: suggest `/clear` before proceeding
2. Present `next_step` as the primary recommendation
3. If `alt_steps` non-empty: list as alternatives
4. For `next_step` and each `alt_step`, include the `model_tier` from the JSON so the user knows which model is best for each option. Look up tiers in `model-recommendations.md` for agent-specific switch commands.
5. Append dashboard link

Format:
```
Constitution ready!
Next: [/clear → ] <next_step> (model: <tier>)
[- <alt_step> — <reason> (model: <tier>)]

- Dashboard: file://$(pwd)/.specify/dashboard.html (resolve the path)
```

## Usage

Example invocations:

- "/iikit-00-constitution" — Run the full iikit 00 constitution workflow
- "iikit 00 constitution on this project" — Apply to current context


## Validation Gate

- [ ] Output follows the defined structure and format [EXPLICIT]
- [ ] All claims are tagged with evidence markers [EXPLICIT]
- [ ] No placeholder content (TBD, TODO) [EXPLICIT]
- [ ] Actionable recommendations with priority levels [EXPLICIT]
- [ ] Assumptions explicitly documented [EXPLICIT]

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Assumes PREMISE.md exists and passed validation; this skill does not author it [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Operates on the current working directory as the project root; `git init` runs there if absent [EXPLICIT]
- Writes exactly two tracked artifacts (`CONSTITUTION.md`, `.specify/context.json`); dashboard is best-effort and never blocks [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

**Acceptance criteria** (constitution is "done" when all hold): [EXPLICIT]
- Zero remaining bracket placeholders in the written file. [EXPLICIT]
- ≥3 principles, each with name + checkable rule + rationale. [EXPLICIT]
- Body version == Sync Impact Report version; all dates ISO-8601. [EXPLICIT]
- No tech-stack / tool / version content (phase-separation clean). [EXPLICIT]
- Quality Governance section present and references QA-PLAN.md verbatim. [EXPLICIT]
- `tdd_determination` persisted in `.specify/context.json`. [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Infer principles from PREMISE.md + repo; request clarification only if intent is unrecoverable |
| Conflicting requirements | Flag conflicts explicitly, propose resolution, do not silently pick one |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Constitution already exists | Treat as amendment: compute correct semver bump, write Sync Impact Report, do not reset to 1.0.0 |
| User asks for tech/stack principle | Decline at constitution layer; route the item to `/iikit-02-plan` |
| Non-empty `$ARGUMENTS` conflicts with PREMISE.md | Surface the divergence; PREMISE.md is the intent baseline unless the user overrides explicitly |
