# iikit Routing Checklist

Run top-to-bottom before declaring any iikit invocation done.

## Resolve
- [ ] `topic` mapped to a single enum value (named stage or `00`–`08` number).
- [ ] Described intent → earliest **unmet** stage, not the most convenient one.
- [ ] Ambiguity → asked one consolidated question; no fan-out.
- [ ] Bug-fix intent → rerouted to `bugfix`; unresolved unknowns → `clarify`.

## Depend
- [ ] Predecessor artifact present, or explicitly created (no stage on a missing
  predecessor).
- [ ] For testify/implement: assertion hash present in BOTH context.json and git note.

## Execute
- [ ] Exactly one `references/*.md` playbook read.
- [ ] Prescribed `iikit-core` scripts run; JSON parsed; failures surfaced verbatim.
- [ ] `depth` applied (`quick` essentials / `deep` full gate verification).

## Validate
- [ ] Stage Validation-Gate acceptance criteria all hold.
- [ ] One evidence-tag family; zero placeholder tokens.
- [ ] No invented prices; no client PII; single brand.
- [ ] Next-step suggestion + dashboard link emitted.
