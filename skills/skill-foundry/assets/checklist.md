# Routing checklist — skill-foundry

Run top to bottom before declaring a routing decision done. [DOC]

## Discover
- [ ] Captured the verbatim intent.
- [ ] Identified asset kind (skill/agent/command/prompt/hook/mcp/workflow).
- [ ] Identified action (create/design/audit/certify/benchmark/index/search).
- [ ] Set `depth` (quick | deep).

## Analyze
- [ ] Listed candidate topics the intent could match.
- [ ] Applied SKILL.md tie-breakers (create vs design; assembly vs x-ray vs
      certify; prompt-creator vs prompt-forge; workflow-creator vs workflow-forge).
- [ ] Resolved to exactly ONE of the 16 enum topics — or asked one disambiguating
      question — or declared out-of-foundry-scope.

## Execute
- [ ] Read ONLY `references/<topic>.md` (no second reference).
- [ ] Ran the depth-appropriate path.
- [ ] Ran every deterministic script the playbook ships; captured exit codes.

## Validate
- [ ] Playbook rubric + constitution v6.0.0 passed.
- [ ] One Alfa-set tag per non-obvious claim; playbook `[EXPLICIT]`/`[INFERRED]`
      preserved.
- [ ] Single brand, no invented prices, no green-as-success, no client PII.
- [ ] Emitted final `dod=pass` / `dod=fail` line with any failing checks.
