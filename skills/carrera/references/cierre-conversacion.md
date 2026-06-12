<!-- distilled from alfa skills/cierre-conversacion -->
<!-- Cosecha aprendizajes, valida evidencia y produce un cierre de conversacion reproducible con handoff, riesgos y plan de actualizaciones durables. -->
# Cierre Conversacion

## Purpose

Use this skill to close a long or explicitly ended conversation without losing useful state. It turns the session into a deterministic closeout packet: what was decided, what changed, what remains open, which learnings are reusable, which validations are real, and which durable updates are only proposed unless authority is explicit.

Scope boundary: this skill **reports and proposes**; it is not a write executor. Durable writes happen only under explicit authority (see Procedure 4). It does not implement code, run deployments, or resolve open tasks — it captures their state so the next session can act.

## Activation

Activate when any of these conditions is true:

- The user explicitly asks for `cierre-conversacion`, `session-audit`, closeout, retrospective, handoff, or learning harvest.
- The conversation is long enough that decisions, risks, or next steps may be lost across sessions. Threshold heuristic: 3+ durable decisions, OR 1+ unresolved blocker, OR files/branches/PRs touched, OR context approaching compaction. [INFERENCIA]
- A process requires a final packet before merge, handoff, archive, or thread cleanup.

Do not activate for generic filesystem cleanup, unrelated summarization, or requests to erase history without preserving required evidence. If the request is "just summarize" with no decisions/risks/handoff, defer to a plain summary instead of a full packet (avoids ceremony overhead). [CONFIG]

## Inputs Expected

- Current objective and scope.
- Known files, branches, PRs, commands, or artifacts touched.
- Validation results, blockers, and unresolved risks.
- Explicit authority status for tasklog, changelog, memory, or other durable writes.

Missing-input policy: if objective is absent, ask once; if still absent, emit a minimal blocked packet (Edge Cases) rather than inventing scope. Never fabricate validation results or authority status — absent authority defaults to report-only.

## Outputs Expected

- Conversation closeout summary with evidence tags.
- Decisions, tasks, learnings, risks, and validation evidence.
- Durable update plan that separates confirmed writes from proposals.
- Next handoff with the safest next action.
- Guardian decision: `pass` when closure evidence is enough, `block` when it is not.

## Procedure

### 1. Detect Closure Mode

Classify the trigger as explicit, threshold-based, or manual audit. If activation is ambiguous, produce a short proposal rather than claiming a completed closeout. Mode affects depth only, never evidence rigor: an explicit trigger does not license skipping validation.

### 2. Harvest Evidence

Collect only observable facts from the conversation, files, commands, PRs, or user-provided context. Tag every claim as `[CÓDIGO]`, `[CONFIG]`, `[DOC]`, `[INFERENCIA]`, `[SUPUESTO]`, or `[POR_CONFIRMAR]`.

Per-section minimum evidence:

| Section | Strongest tag required to claim "done/confirmed" |
|---|---|
| Completed work | `[CÓDIGO]` (file, command, PR, diff, or CI output) |
| Validation evidence | `[CÓDIGO]` — command/artifact; never `[INFERENCIA]` alone |
| Decisions | `[CÓDIGO]` or `[CONFIG]` for the decision basis |
| Merge / deploy claim | `[CÓDIGO]` from CI/remote, else `[POR_CONFIRMAR]` |
| Durable update plan | `[CONFIG]` proving authority, else proposal-only |

### 3. Build Closeout Packet

Fill the required sections in this order:

1. Summary.
2. Decisions.
3. Completed work.
4. Open tasks.
5. Learnings and reusable patterns.
6. Risks and blockers.
7. Validation evidence.
8. Durable update plan.
9. Next handoff.
10. Guardian decision.

### 4. Control Writes

Do not update tasklog, changelog, memory, or skill assets unless the current authority is explicit. When authority is missing, return the proposed update text and mark it `[POR_CONFIRMAR]`.

Decision — report-only default. Trade-off: a forgotten durable write costs one follow-up; an unauthorized write to shared memory/changelog is hard to detect and erodes trust in the record. The asymmetry justifies defaulting closed. [CONFIG]

### 5. Validate

Before declaring pass, ensure no completed task relies only on `[SUPUESTO]` or `[POR_CONFIRMAR]`, every validation claim has command or artifact evidence, and no failed validation is hidden behind a pass decision.

## Acceptance Criteria

A closeout packet is acceptable only when ALL hold:

- All 10 sections present and ordered (empty sections say "none", not omitted).
- Every non-obvious claim carries exactly one evidence tag from the canonical set.
- No "done" or "validated" claim rests solely on `[SUPUESTO]`/`[INFERENCIA]`/`[POR_CONFIRMAR]`.
- Durable writes are either executed-under-authority or listed as proposals — never silently applied.
- Open tasks each have an owner or a next action when known.
- Guardian decision is justified by the evidence shown, and `block` names the specific failing item.

## Quality Criteria

- Closure packet is deterministic and section-complete.
- Evidence tags are present on all non-obvious claims.
- Durable updates are separated from unapproved proposals.
- Open tasks have owners or next actions when known.
- Guardian blocks false completion, contradictory CI/validation evidence, and unrelated local changes.

## Worked Example (abbreviated)

```
Summary: Fixed auth token refresh; one test still flaky. [INFERENCIA]
Decisions: Refresh window set to 60s. [CONFIG]
Completed work: token.ts retry loop landed; `npm test auth` 12/13 pass. [CÓDIGO]
Open tasks: stabilize flaky test t-7 — owner: next session; action: add fake clock.
Learnings: jitter on retry avoids thundering herd (reusable). [CÓDIGO]
Risks: 13th test flaky → may mask a real race. [SUPUESTO]
Validation: `npm test auth` ran locally; CI not yet run. [POR_CONFIRMAR]
Durable update plan: append to changelog — PROPOSED, no write authority. [POR_CONFIRMAR]
Next handoff: run flaky test under fake clock before merge.
Guardian: block — one validation pending CI; one test failing.
```

## Failure Modes

| Failure | Symptom | Correct handling |
|---|---|---|
| Green-washing | "All done" with no `[CÓDIGO]` | Downgrade to `[POR_CONFIRMAR]`, Guardian `block`. |
| Phantom write | Claims tasklog/changelog updated, no authority | Convert to proposal, mark `[POR_CONFIRMAR]`. |
| Lost blocker | Risk dropped to look clean | Preserve risk verbatim; never erase. |
| Scope creep | Unrelated local changes bundled in | Flag as out-of-scope; Guardian `block`. |
| Stale handoff | Next action references resolved state | Recompute from current evidence only. |

## Assets

Use `assets/activation-policy.json`, `assets/output-contract.json`, `assets/evidence-policy.json`, `assets/harvest-checklist.json`, and `assets/durable-update-policy.json` as the deterministic source of truth for activation, output shape, evidence tags, harvest checks, and durable update authority. On conflict, these JSON assets win over this prose. [CONFIG]

## Edge Cases

- Empty closeout request: ask for the objective or produce a minimal blocked packet.
- Conflicting evidence: preserve both claims and block green completion until resolved.
- No durable-write authority: output proposed updates only.
- Long conversation with many details: prioritize durable decisions, blockers, and next five actions.
- Merge or deployment claim without evidence: mark `[POR_CONFIRMAR]` and keep Guardian blocked.
- Partial authority (e.g. tasklog yes, memory no): execute only the authorized writes; list the rest as proposals.
- User asks to skip validation: refuse silent pass — emit packet with Guardian `block` and the skipped item named.

## Scripts

Deterministic checks live in `scripts/`. Run:

```bash
bash skills/cierre-conversacion/scripts/check.sh
```

The script validates closeout report fixtures offline and requires invalid fixtures to fail. Run it before declaring `pass` on any packet that touches fixtures; a non-zero exit blocks closure. [CÓDIGO]

## Related Skills

- `session-end-cleanup`
- `tasklog-management`
- `changelog-management`
- `pre-compact-context`

## Evidence Requirements

- `[CÓDIGO]`: local files, commands, PR metadata, CI output, or diff evidence.
- `[CONFIG]`: user instructions, repository policy, or workflow contract.
- `[DOC]`: stable project documentation.
- `[INFERENCIA]`: derived conclusion from evidence.
- `[SUPUESTO]`: unverified assumption.
- `[POR_CONFIRMAR]`: pending user, CI, remote, or external confirmation.

Precedence when tags conflict on one claim: `[CÓDIGO]` > `[CONFIG]` > `[DOC]` > `[INFERENCIA]` > `[SUPUESTO]` > `[POR_CONFIRMAR]`. A claim never carries two tags; pick the strongest *justified* one. [CONFIG]

## Update-Safety Notes

- Default mode is report-only.
- Durable writes require explicit authority and must be listed in `durable_update_plan`.
- Never erase unresolved risks or failed validation evidence during closure.
- Re-running closure must be idempotent: identical inputs yield the same packet and never double-apply a durable write. [INFERENCIA]
