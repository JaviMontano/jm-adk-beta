# Assets — Official Source Verifier

This bundle holds the stable contracts and policies that make a verification report
certifiable. SKILL.md and the guardian load them as the rubric; the deterministic scripts
validate reports against them.

## Files

- `official-source-verifier-contract.json` — required report fields, enums, and invariants
  (status, source registry entry shape, claim shape, decision shape). Used by `SKILL.md`.
- `source-priority-policy.json` — the fixed hierarchy official > vendor > spec > repo >
  secondary, which tiers may be authority, and the conflict-escalation rule. Used by
  `SKILL.md`.
- `citation-policy.json` — URL + ISO `accessed_date` + extract requirements and the
  date/secondary self-correction triggers. Used by `SKILL.md`.
- `quality-rubric.json` — scored, mostly-blocking acceptance criteria mapped to the
  validation gate. Used by `agents/guardian.md`.
- `verification-checklist.md` — human pre-delivery checklist mirroring the gate, with
  evidence tags. Used by `knowledge/body-of-knowledge.md` and this `README.md`.

## How they connect

`SKILL.md` names the contract and policies in its "Contrato determinístico" section. The
guardian scores the report against `quality-rubric.json`; a human runs
`verification-checklist.md` before delivery. When the deliverable is JSON, the assets are
the schema the deterministic scripts enforce.

Governance: harness voice; evidence tags on every claim; no invented prices; green is not
success by default; no client PII; single brand (JM Labs).
