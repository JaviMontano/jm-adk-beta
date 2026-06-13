# Example output

Routing decision produced for the `cold-call-prep` request in `example-input.md`.

## Request
- **Intent (verbatim):** "take it all the way to production… run the audit, fix
  what's broken, give me a shippable verdict… prove the quality actually went up."
- **Asset kind:** skill
- **Action:** production-ize end-to-end + prove gain
- **Depth:** deep

## Resolution
- **Candidate topics considered:** `assembly-skill`, `x-ray-skill`,
  `certify-skill`, `benchmark-skill`.
- **Resolved topic:** `assembly-skill`
- **Rationale:** SKILL.md tie-breaker "improve/production-ize end-to-end →
  assembly-skill". The request asks for audit + fix + verdict in one pass, which is
  exactly the pipeline assembly orchestrates (x-ray → surgeon → certify). [DOC]
- **Rejected candidates:** `x-ray-skill` (audit only, no fix/verdict);
  `certify-skill` (verdict only, read-only, no fix); `benchmark-skill` folded in by
  assembly's optional gate rather than run standalone. [INFERENCE]
- **Reference read:** `references/assembly-skill.md` (exactly one)

## Execution
- **Depth path run:** exhaustive + verification
- **Deterministic scripts run:** `scripts/check.sh` → 0;
  `scripts/validate_certification_report.py` → 0 [DOC]
- **Artifact / verdict produced:** assembly pipeline result — diagnostic gaps,
  applied interventions, certification verdict, and before/after delta.

## Gate results
| Gate | Check | Status |
|------|-------|--------|
| Routing integrity | valid enum topic; exactly one playbook read | pass |
| Playbook acceptance | assembly rubric + constitution v6.0.0 | pass |
| Governance | one Alfa tag/claim; single brand; no prices; no green-as-success; no PII | pass |

**Verdict:** `dod=pass` — certification level CONDITIONAL: two non-blocking
findings logged; net quality delta positive versus the prior version. [DOC]

## Next action
Ship after clearing the two CONDITIONAL findings, or accept them with the logged
rationale. No invented prices were attached; the verdict is not auto-green — it
rests on the script exit codes and the certification policy. [DOC]
