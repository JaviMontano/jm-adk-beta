# Security Deliverable — {{topic}} ({{depth}})

## Routing
- **Resolved topic**: {{topic}}  (one of: architecture, audit-security,
  auth-architecture, cors-configuration, dual-layer-verification, http-headers,
  input-sanitization, rate-limiting, rbac-patterns, testing)
- **Route loaded**: references/{{topic}}.md  (exactly one)
- **Depth**: {{quick|deep}}
- **Disambiguation note**: <why this route over the nearest alternative, or "none — unambiguous"> [INFERENCE]

## Scope
- **In scope**: <files / surface / invariants under review>
- **Out of scope / not assessed**: <explicit exclusions> [ASSUMPTION]

## Findings
> For `audit-security`/`dual-layer-verification`, IDs are `SEC-NNN`, ascending by
> category then (path, line); `Summary` counts must equal this set.

| ID | Category | Severity | Status | Path:Line | Evidence | Tag |
|----|----------|----------|--------|-----------|----------|-----|
| SEC-001 | <category> | CRITICAL/WARNING/INFO | confirmed/placeholder/review | <path:line> | <masked evidence> | [CODE] |

## False-positive notes
- <placeholder / doc-only example> → INFO, status `placeholder`, reason. [EXPLICIT]

## Recommendations / Remediation plan
| Finding ID | Action | Layer (static/runtime/config) | Tag |
|-----------|--------|------------------------------|-----|
| SEC-001 | <concrete fix> | <where> | [DOC] |

(Every CRITICAL/WARNING above must appear here exactly once.)

## Verification evidence
- Static (Layer 1): <commands run + result> [CODE]
- Runtime (Layer 2, if applicable): <Playwright checks + result, or "skipped — Playwright unavailable"> [CODE]
- Validator exit codes: <verbatim> [CODE]

## Coverage
- Files scanned: <list/count>
- Files skipped: <path — reason (out_of_scope / binary / not human-readable)>

## Quality gate
- [ ] One route resolved; one playbook loaded
- [ ] Every non-obvious claim tagged (Alfa core set, one spelling)
- [ ] Severity keyed on exploitable context; placeholders never CRITICAL
- [ ] IDs ascending/gapless; Summary counts == Findings; no orphan remediation
- [ ] No green-as-success; no mutation of targets; no offensive action
- [ ] No unresolved {VACIO_CRITICO}

## Go / No-Go
**Decision**: <GO / NO-GO>  — <one-line rationale, tagged> [DOC]
