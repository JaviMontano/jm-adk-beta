# Foundry Routing Decision

## Request
- **Intent (verbatim):** <user's request in one line>
- **Asset kind:** <skill | agent | command | prompt | hook | mcp | workflow>
- **Action:** <create | design | audit | certify | benchmark | index | search>
- **Depth:** <quick | deep>

## Resolution
- **Candidate topics considered:** <list, or "single obvious match">
- **Resolved topic:** `<one of 16 enum values>`
- **Rationale:** <which routes.json trigger / SKILL.md tie-breaker decided it> [DOC]
- **Rejected candidates:** <topic — reason rejected> [INFERENCE]
- **Reference read:** `references/<topic>.md` (exactly one)

## Execution
- **Depth path run:** <essentials | exhaustive + verification>
- **Deterministic scripts run:** <script — exit code> [DOC]
- **Artifact / verdict produced:** <agent def | prompt | audit scorecard |
  certification verdict | benchmark diff | index | search results>

## Gate results
| Gate | Check | Status |
|------|-------|--------|
| Routing integrity | valid enum topic; exactly one playbook read | pass / fail |
| Playbook acceptance | route rubric + constitution v6.0.0 | pass / fail |
| Governance | one Alfa tag/claim; single brand; no prices; no green-as-success; no PII | pass / fail |

**Verdict:** `dod=pass` / `dod=fail` — <failing checks if any>

## Evidence
- <claim> [DOC]
- <derived statement> [INFERENCE]
- <unverified item> [ASSUMPTION]

## Next action
<ship | fix listed blockers and re-run gate | redirect (out of foundry scope)>
