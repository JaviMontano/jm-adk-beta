<!-- distilled from alfa skills/assembly-skill -->
<!-- Use when the user asks to run the full skill quality pipeline, improve a skill end to end, take a skill to production, run x-ray plus surgeon plus certify, or assembly-line one skill. Orchestrates one target skill through deterministic diagnostic, intervention, certification, and optional trigger optimization gates. -->
# Skill Assembly Line

Run the skill-quality pipeline for exactly one target skill: Phase A diagnostic, Phase B intervention, Phase C certification, optional Phase C+ trigger optimization, and Phase D report. [EXPLICIT]

Part of the Skill Quality Suite: x-ray-skill → surgeon-skill → certify-skill (+ trigger-skill, benchmark-skill, **assembly-skill**). Each suite skill is standalone; assembly-skill orchestrates them in one run rather than reimplementing their logic. [EXPLICIT]

## When to Activate

Activate when the user asks to: [EXPLICIT]

- run the full skill pipeline
- improve this skill end to end
- take this skill to production
- run x-ray -> surgeon -> certify
- assembly-line a skill
- make one skill production-ready without separately invoking each phase

Do not activate for general "assembly" work such as assembling a deck, product, CI pipeline, package, or document bundle. [EXPLICIT] These collide on the word "assembly" but share no contract; route them to their own skills. [INFERRED]

## Scope Assumptions and Anti-Scope

- Assumes the target is a Claude Code skill directory containing a `SKILL.md`. A bare file, a plugin, or an agent is out of scope. [EXPLICIT]
- Assumes x-ray-skill, surgeon-skill, and certify-skill logic are reachable; if any is unavailable, the dependent phase reports `BLOCKED` rather than approximating it. [INFERRED]
- Anti-scope: never refactor skill *content* for taste, never batch-process a directory of skills, never invent fixtures or durations, never ship without certification evidence. [EXPLICIT]
- Out of scope: publishing, installing, or registry indexing the certified skill — those are separate skills. [EXPLICIT]

## Deterministic Contract

- Scope is one target skill directory. Never process multiple skills in one run. [EXPLICIT]
- Read `assets/mode-policy.json` before selecting a mode. [EXPLICIT]
- Read `assets/assembly-report-contract.json` before producing the final report. [EXPLICIT]
- Use `assets/assembly-report-template.md` for report shape. [EXPLICIT]
- Run `scripts/validate_assembly_contract.py` against any final report before delivery. [EXPLICIT]
- Use caller-supplied elapsed buckets or `not-measured`; do not derive durations from wall-clock time. [EXPLICIT] Rationale: wall-clock varies by host and context load, so it is not reproducible evidence. [INFERRED]
- Use only fixed trigger-query fixtures for deep mode, or record generated query sets before scoring. [EXPLICIT] Unrecorded generated queries make a score impossible to reproduce or audit. [INFERRED]
- Do not modify files before Gate B approval is explicit. [EXPLICIT]
- Determinism check: two runs of the same mode on an unchanged skill must yield the same scorecard, mode, and verdict. A diff means non-determinism leaked in (time, randomness, or unrecorded queries) — treat as a defect, not noise. [INFERRED]

## Required Inputs

1. Exactly one target skill path. [EXPLICIT]
2. Mode: `quick`, `standard`, `deep`, or absent for deterministic auto-selection. [EXPLICIT]
3. User intent: diagnostic-only, improve, certify, or optimize triggers. [EXPLICIT]
4. Write approval for Phase B if files may change. [EXPLICIT]

If the target path is missing, multiple skill paths are supplied, or `SKILL.md` is absent, return `BLOCKED` and do not proceed. [EXPLICIT] Fail closed: ambiguous scope is a stop condition, never a best-guess pick. [INFERRED]

## Modes

| Mode | Phases | Writes | Use |
|---|---|---|---|
| quick | A + D | No | Diagnostic snapshot only |
| standard | A + B + C + D | After Gate B | Production-readiness repair |
| deep | A + B + C + C+ + re-certify + D | After Gate B | Trigger optimization after structural repair |

Decision — why deep gates trigger optimization behind structural repair: optimizing a description against a skill whose body is still broken tunes activation toward content that may change in Phase B, wasting the optimization. Trade-off: deep costs the most context and time, so reserve it for skills already near-passing (score 7–8). [INFERRED]

## Auto-Selection

Use the Phase A scorecard as the only score source: [EXPLICIT]

| Condition | Mode |
|---|---|
| score < 5 | standard |
| score >= 5 and score < 7 | standard |
| score >= 7 and score < 8 | deep |
| score >= 8 and gate 13/13 and user did not request changes | quick |
| score >= 8 and user requested changes | standard |

Boundary rules (avoid off-by-one drift): bands are half-open `[low, high)`; a score of exactly 7 is deep, exactly 8 with 13/13 is quick. [INFERRED] A high score with an explicit change request never auto-selects quick — user intent outranks the score. [EXPLICIT]

If context pressure is high, fall back to `standard` and report the fallback. [EXPLICIT] Standard is the safe default because it both repairs and certifies without the extra deep-mode budget. [INFERRED]

## Phase Protocol

### Phase A: Diagnostic

Apply `x-ray-skill` logic to produce a scorecard, gate count, top gaps, and recommended mode. If Phase A cannot run, report `BLOCKED`. [EXPLICIT] Phase A is read-only and is the single source of the score every later gate consumes. [INFERRED]

### Gate A: Intervention Decision

Skip intervention only when auto-selection returns `quick` and the user did not ask for changes. [EXPLICIT] Any explicit change request forces at least one intervention path even on a high score. [INFERRED]

### Phase B: Intervention

Apply `surgeon-skill` logic only after Gate B approval. Present the intervention plan first: [EXPLICIT]

```markdown
Assembly Line Intervention Plan
Target: {skill}
Current score: {score}
Projected score: {score}
Interventions: {count}
Gate B: approve / trim / reject
```

If Gate B is rejected, stop writes and produce a diagnostic-only report. [EXPLICIT] "trim" means apply a caller-reduced subset of the listed interventions, then continue. [INFERRED]

### Phase C: Certification

Apply `certify-skill` logic to the post-intervention state. The final verdict must come from certification evidence, not from wording. [EXPLICIT] Never report `CERTIFIED` from prose, optimism, or a passing Phase A alone — only from the certify formula output. [EXPLICIT]

### Phase C+: Trigger Optimization

Deep mode only. Apply `trigger-skill` logic with a recorded query set, then re-certify. If trigger optimization degrades certification, report `CONDITIONAL` or `BLOCKED`. [EXPLICIT] Re-certification after C+ is mandatory because the description change can alter activation behavior the earlier certification scored. [INFERRED]

### Phase D: Assembly Report

Use `assets/assembly-report-template.md`. The report must include: [EXPLICIT]

- target skill
- mode
- result
- phase evidence
- before/after score and gate delta
- Gate B status
- certification formula source
- every modified file, or `No files modified`
- specific next step

## Worked Example

Input: `/path/to/my-skill`, no mode, intent improve. [EXPLICIT, illustrative]

1. Phase A: score 7.0, gates 11/13, top gaps = missing failure modes, weak trigger. [EXPLICIT, illustrative]
2. Auto-selection: 7 ≤ score < 8 → **deep**. [EXPLICIT]
3. Gate A: not quick → intervention proceeds; present plan, await Gate B. [EXPLICIT]
4. Gate B approved → Phase B applies surgeon fixes; projected score 8.4. [EXPLICIT, illustrative]
5. Phase C: certify formula → `CERTIFIED`, gates 13/13. [EXPLICIT, illustrative]
6. Phase C+: recorded fixtures, re-certify holds `CERTIFIED`. [EXPLICIT, illustrative]
7. Phase D: report lists 3 modified files, formula source, next step. Run `validate_assembly_contract.py` → pass → deliver. [EXPLICIT]

## Failure Modes and Edge Cases

| Situation | Required behavior |
|---|---|
| No path / multiple paths / no `SKILL.md` | `BLOCKED` before any phase [EXPLICIT] |
| Phase A cannot run | `BLOCKED`; no downstream phases [EXPLICIT] |
| Gate B rejected | Stop writes; diagnostic-only report [EXPLICIT] |
| Phase B writes but Phase C cannot run | `CONDITIONAL` or `BLOCKED`; report partial state, do not claim `CERTIFIED` [INFERRED] |
| C+ degrades certification | `CONDITIONAL` or `BLOCKED` [EXPLICIT] |
| Quick mode tempted to write | Forbidden; quick is read-only [EXPLICIT] |
| Duration unknown | Use `not-measured`, never a wall-clock estimate [EXPLICIT] |
| Generated trigger queries unrecorded | Record set before scoring, else `BLOCKED` [INFERRED] |
| Contract validator fails on final report | Do not deliver; fix report to pass first [EXPLICIT] |

## Validation Gate

- [ ] `scripts/validate_assembly_contract.py` passes for the final report. [EXPLICIT]
- [ ] Mode selection follows `assets/mode-policy.json`. [EXPLICIT]
- [ ] Gate B approval appears before any write action. [EXPLICIT]
- [ ] Quick mode is read-only and does not claim `CERTIFIED`. [EXPLICIT]
- [ ] Standard/deep modes include Phase B and Phase C evidence. [EXPLICIT]
- [ ] Deep mode includes Phase C+ trigger metrics and re-certification. [EXPLICIT]
- [ ] Missing target path or missing `SKILL.md` fails closed. [EXPLICIT]
- [ ] Every reported verdict traces to a certification formula source, not prose. [EXPLICIT]
- [ ] The final report uses `[EXPLICIT]`, `[INFERRED]`, or `[OPEN]` evidence tags. [EXPLICIT]

## Acceptance Criteria

The run is acceptable only when all hold: the selected mode matches the auto-selection table given the Phase A score and user intent; no file was modified before an explicit Gate B approval; the Phase D report contains every required field; the contract validator passes; and the verdict is `CERTIFIED`, `CONDITIONAL`, `BLOCKED`, or a diagnostic-only result consistent with the chosen mode. Any unmet item is a failed run, not a warning. [INFERRED]

## Reference Files

| File | Load When |
|---|---|
| `assets/mode-policy.json` | Always, before mode selection |
| `assets/assembly-report-contract.json` | Always, before reporting |
| `assets/assembly-report-template.md` | Before producing the Phase D report |
| `scripts/validate_assembly_contract.py` | Before delivering any final report |
| `references/pipeline-modes.md` | When explaining mode behavior |
