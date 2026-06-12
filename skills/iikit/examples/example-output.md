# Example Output — iikit routing (password-reset → 01-specify)

## 1. Resolution
- **Requested:** "Let users reset their password via an emailed link that expires in 1 hour."
- **Resolved topic:** `01-specify` [CONFIG]
- **Resolution basis:** inferred earliest-unmet stage — constitution present, no spec → specify [INFERENCE]
- **Depth:** quick (default) [CONFIG]
- **Playbook read (exactly one):** references/01-specify.md [INFERENCE]

## 2. Predecessor check
| Required predecessor | Present? | Action |
|----------------------|----------|--------|
| CONSTITUTION.md (soft-loaded) | yes (v1.0.0) | proceed |
| PREMISE.md | yes, validated | proceed |

## 3. Determinism (scripts run)
| Script | Phase | Key JSON fields | Result |
|--------|-------|-----------------|--------|
| create-new-feature.sh --json "..." --short-name password-reset | 01 | BRANCH_NAME, SPEC_FILE, FEATURE_NUM | ok |
| next-step.sh --phase 01 --json | 01 | next_step, alt_steps, clear_after | ok |

## 4. Stage artifact produced
- **Paths:** `specs/001-password-reset/spec.md`,
  `specs/001-password-reset/checklists/requirements.md`,
  `specs/001-password-reset/qa/acceptance-criteria.md`
- **Summary:** branch `001-password-reset`; actor = registered user; actions =
  request reset, follow emailed link, set new password; entity = reset token
  (TTL 1h). Step 0 classified the request as a new feature, not a bug fix. [EXPLICIT]
- **Integrity controls:** SC→FR traceability enforced; phase-separation scan
  clean (no HOW); one `[NEEDS CLARIFICATION]` candidate (account lockout policy)
  defaulted to "no lockout in v1" so no marker emitted. [EXPLICIT]

Representative spec fragment:
- FR-001: System issues a single-use reset token bound to the account.
- FR-002: System emails the reset link to the account's verified address.
- SC-001: ≥95% of valid reset requests deliver an email within 60s → links FR-001, FR-002. [EXPLICIT]

## 5. Validation gate
- [x] spec.md passes phase-separation scan (no implementation detail) [EXPLICIT]
- [x] Every FR independently testable; every SC measurable and tech-agnostic [EXPLICIT]
- [x] Every SC traces to ≥1 FR (no orphan criteria) [INFERENCE]
- [x] No surviving `[NEEDS CLARIFICATION]` markers [EXPLICIT]
- [x] Branch, SPEC_FILE, dashboard exist; commit landed [INFERENCE]
- [x] One evidence-tag family; zero placeholders; no prices; no PII [CONFIG]

## 6. Next step
- **Primary:** `/iikit-02-plan` (model: standard)
- **Alternatives:** `/iikit-clarify` — if the lockout default needs review (model: standard)
- **Dashboard:** file://.../.specify/dashboard.html

## 7. Assumptions & limits
- Constitution was soft-loaded; its `tdd_determination = optional` will be
  re-read by `04-testify`, not enforced here. [ASSUMPTION]
