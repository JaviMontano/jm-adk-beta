# Example output — business-analysis (requirements-engineering)

> Skill: `business-analysis` · Topic: `requirements-engineering` · Depth: `quick`
> Spine: Discover → Analyze → Execute → Validate

## 1. Routing record
- **Resolved topic:** `requirements-engineering` — request asks for INVEST stories,
  testable AC, and objective traceability. No tie. [DOC]
- **Playbook loaded:** `references/requirements-engineering.md` (one only). [DOC]
- **Out of scope (redirected):** screen design, hour estimates (phase separation). [CONFIG]

## 2. Discover
- System-of-record: `auth-svc` identity service. [DOC]
- Objectives: O-1 reduce password tickets; O-2 no new enumeration surface. [DOC]
- Open gaps: reset-link TTL and rate-limit thresholds unprovided → `[ASSUMPTION]`,
  confirm with security owner. [ASSUMPTION]

## 3. Execute — stories + acceptance criteria

### US-1 — Request a reset link
> As a registered user, I want to request a password-reset link by email, so that I regain
> access without contacting support. [DOC]

- **AC-1.1 (happy)** — Given a registered email, When I request a reset, Then a single-use
  link valid for 15 min is sent. [ASSUMPTION: 15-min TTL — confirm with security]
- **AC-1.2 (negative, anti-enumeration)** — Given an unregistered email, When I request a
  reset, Then the UI shows the same generic confirmation as the registered case. [INFERENCE]
- **AC-1.3 (boundary, abuse)** — Given >5 requests for one email within an hour, When I
  request again, Then the request is throttled. [ASSUMPTION: threshold — confirm with platform]

### US-2 — Complete the reset
> As a user with a valid reset link, I want to set a new password, so that I can log in
> again. [DOC]

- **AC-2.1 (happy)** — Given an unused, unexpired link, When I submit a compliant new
  password, Then the password is updated and all active sessions are revoked. [INFERENCE]
- **AC-2.2 (boundary)** — Given an expired or already-used link, When I open it, Then the
  reset is refused and a re-request is offered. [DOC]

## 4. Traceability matrix
| Requirement | Acceptance criteria | Objective |
|-------------|---------------------|-----------|
| US-1 request link | AC-1.1, AC-1.2, AC-1.3 | O-1, O-2 |
| US-2 complete reset | AC-2.1, AC-2.2 | O-1 |

Orphan check: every requirement maps to ≥1 objective and ≥1 AC; O-1 and O-2 both covered.
No orphans. [DOC]

## 5. Validate (acceptance gate)
- [x] Exactly one playbook loaded; topic matches intent. [DOC]
- [x] Stories INVEST-compliant; AC includes negative + boundary, not just happy. [DOC]
- [x] Traceability matrix has no orphan requirements or objectives. [DOC]
- [x] Assumptions tagged and paired with a verification step. [ASSUMPTION]
- [x] No screen design or hour estimates (phase separation). [CONFIG]

## 6. Evidence-tag summary
`[DOC] 45% · [INFERENCE] 25% · [ASSUMPTION] 20% · [CONFIG] 10%`
> `[ASSUMPTION]` at 20% (<30%) — no warning banner required; two items pending security
> confirmation (TTL, rate-limit threshold).
