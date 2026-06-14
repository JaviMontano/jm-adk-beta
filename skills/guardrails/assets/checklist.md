# Guard verdict checklist — guardrails

Run before emitting any verdict. All blocker items must hold. [EXPLICIT]

## Routing

- [ ] `topic` resolved to exactly one of the 12 enum values. (blocker)
- [ ] Exactly one playbook read; no multi-load "to be safe". (blocker)
- [ ] `depth` set (`quick` default; `deep` for gate/PR/release). 

## Execution

- [ ] Named offline validator run for this topic. (blocker)
- [ ] `scripts/check.sh` green on POSITIVE and NEGATIVE fixtures. (blocker)
- [ ] Every required JSON policy asset loaded; missing asset ⇒ blocked, not improvised.

## Verdict integrity

- [ ] Verdict explicit: allow/approve/block (pre) or pass/fail/blocked/not_verified.
- [ ] Pre-execution: `block`⇒exit 2, `allow`⇒exit 0 + non-empty evidence. (blocker)
- [ ] No `pass`/`allow` while any required check is fail/blocked. (blocker)
- [ ] Checks array non-empty (no empty-pass). (blocker)
- [ ] All violations aggregated; repairs are exact (target + edit).

## Safety & evidence

- [ ] Fail-closed: missing evidence ⇒ block/fail, never pass. (blocker)
- [ ] Secrets masked everywhere, including the report (`path:line` + masked token). (blocker)
- [ ] One Alfa-core evidence tag per claim; single family. (blocker)
- [ ] Triggering policy/gate rule cited.
- [ ] Determinism: re-run reproduces the same packet (no clock/network/model/random).
