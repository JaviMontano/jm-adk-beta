# Example input — business-analysis

A worked engagement that routes to `requirements-engineering`.

## Request (verbatim)

> "We're adding self-service password reset to our customer portal. Product says 'users
> should be able to reset their password if they forget it.' Security cares about account
> enumeration and abuse. Turn this into proper user stories with testable acceptance
> criteria, and show me how each maps back to our objectives. Keep it to the requirements —
> don't design the screens or estimate hours."

## Context provided

- System-of-record for accounts: existing identity service (`auth-svc`). [DOC]
- Constraint: portal is on the Firebase/Google stack. [CONFIG]
- Objective O-1: reduce password-related support tickets. [DOC]
- Objective O-2: no new account-enumeration surface. [DOC]
- Not provided: reset-link TTL, rate-limit thresholds (must be confirmed with security). [ASSUMPTION]

## How the router resolves it

- Signals: "user stories", "testable acceptance criteria", "maps back to objectives" →
  dominant match is `requirements-engineering`. No tie. [DOC]
- `depth = quick` — one feature, well-scoped; headline stories with happy + negative AC
  and a traceability matrix. [DOC]
- Out of scope, redirected: screen design and hour estimates (phase separation). [CONFIG]
