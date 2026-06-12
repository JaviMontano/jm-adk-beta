# Quick variation — security router (depth=quick)

Fast path. Resolve one `topic`, load one playbook, apply the essentials only.

## Use when
The caller wants a focused answer on a single security concern — e.g. "is this
CORS config safe?", "where do I put the XSS escape?", "which claim gates the
admin route?" — and does not need an exhaustive pass.

## Do
- Infer `topic`; if a true tie, ask one disambiguating question and stop.
- Load EXACTLY ONE playbook from `routes:`.
- Apply only the playbook essentials: the decision rule and the one or two
  highest-leverage actions for the concern.
- Tag claims with the Alfa core set; flag anything that needs `deep` follow-up.

## Do not
- Load multiple playbooks.
- Mark insecure output passing.
- Produce a full audit report when a targeted answer suffices — but if you find a
  CRITICAL, surface it and recommend escalating to `deep`.

## Output
Short: resolved route, the essential recommendation, evidence tags, and an
explicit "escalate to deep?" flag when warranted.
