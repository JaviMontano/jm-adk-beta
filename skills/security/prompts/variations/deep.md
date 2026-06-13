# Deep variation — security router (depth=deep)

Exhaustive path. Resolve one `topic`, load one playbook, apply it in full with
verification at every step.

## Use when
The caller wants a thorough pass — a full static audit, an end-to-end posture
review, or a dual-layer verification of security invariants before a release
gate.

## Do
- Resolve `topic`; load EXACTLY ONE playbook from `routes:`.
- Walk the full spine Discover → Analyze → Execute → Validate, applying every
  step the playbook prescribes.
- For `audit-security`: execute all six scan categories in canonical order even
  when empty; assign deterministic `SEC-NNN` IDs; pair every CRITICAL/WARNING
  with a remediation entry; reconcile `Summary` counts to `Findings`.
- For `dual-layer-verification`: run static (floor) and Playwright runtime
  (ceiling); map each invariant to both layers; apply the layer-disagreement
  protocol to every mismatch; record single-layer gaps.
- Run the relevant offline validators; capture exit codes verbatim.
- Tag every non-obvious claim; resolve all `{VACIO_CRITICO}`.

## Do not
- Load other playbooks for "coverage."
- Treat a zero validator exit as an all-clear — it is a schema/structure gate,
  not a safety guarantee.
- Mark insecure output passing.

## Output
Full deliverable per `templates/output.md`: route, depth, complete
findings/recommendations, validator evidence, coverage, and an explicit go/no-go.
