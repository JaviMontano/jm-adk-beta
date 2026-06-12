# Meta prompt — security router self-check

Run this before emitting any `security` deliverable. It checks the routing and
governance discipline, not the security content itself.

## Routing checks
- [ ] Exactly one `topic` resolved, and it is inside the enum.
- [ ] Exactly one playbook from `routes:` was loaded — no cluster-load.
- [ ] If two routes were equally plausible, I asked instead of guessing.
- [ ] `routes.json` keys were not broken or invented.

## Depth checks
- [ ] `depth` chosen explicitly (`quick`/`deep`); `deep` applied the playbook
      exhaustively with verification at each step.

## Governance checks
- [ ] Every non-obvious claim carries exactly one Alfa-core tag, one spelling.
- [ ] No insecure output marked passing (no green-as-success).
- [ ] Audit work stayed read-only; any exploit/bypass ask was refused while the
      read-only audit still returned.
- [ ] No invented prices, no client PII, single-brand.
- [ ] No unresolved `{VACIO_CRITICO}`.

## Determinism checks (audit/verification routes)
- [ ] `SEC-NNN` IDs ascending, gapless; `Summary` counts equal `Findings`.
- [ ] Every CRITICAL/WARNING has a matching remediation entry.
- [ ] Placeholders/example secrets classified INFO, never CRITICAL.

If any box is unchecked, fix before emitting. A failing self-check blocks "done."
