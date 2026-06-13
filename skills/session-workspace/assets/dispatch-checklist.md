# Dispatch Checklist — session-workspace

Deterministic gate the router runs before declaring a dispatch done. Used by the
guardian agent and the `templates/output.md` Guardian section. Every box must be
checked (or its `[OPEN]` named) for a `proceed`.

## Resolve
- [ ] Lifecycle moment restated in one line. [INFERENCE]
- [ ] `topic` is one of the seven enum values. [CONFIG]
- [ ] `topic` resolved from intent OR exactly one clarifying question asked. [INFERENCE]
- [ ] `depth` set (`quick` default unless `deep` warranted). [CONFIG]

## Discriminate (boundary rulings)
- [ ] Any `.specify/context.json` write/compute → routed to `session-manager`. [CONFIG]
- [ ] "Safe to start?" → `session-start-bootstrap`, not `session-protocol`. [INFERENCE]
- [ ] Full load→recover→close→next → `session-protocol`. [DOC]
- [ ] Preserve unfinished work before compaction → `pre-compact-context`,
      not `session-end-cleanup`. [DOC]
- [ ] Close finished/paused session → `session-end-cleanup`. [DOC]

## Load
- [ ] Exactly ONE `references/<topic>.md` Read (path from `routes.json`). [CONFIG]
- [ ] No sibling playbook loaded. [CONFIG]
- [ ] Playbook's `assets/*.json` policies + `scripts/check.sh` surfaced. [CONFIG]

## Anti-scope
- [ ] No content authoring by the router. [INFERENCE]
- [ ] No `.specify/context.json` write outside the manager route. [CONFIG]
- [ ] No multi-topic merge / fan-out. [INFERENCE]

## Governance
- [ ] Every claim has one Alfa-core tag, one family, consistent spelling. [DOC]
- [ ] No prices, no PII, single brand. [DOC]

## Guardian
- [ ] Decision emitted: `proceed` | `blocked` | `needs-confirmation`. [DOC]
- [ ] Non-`proceed` names the failing gate + corrective next step. [DOC]
