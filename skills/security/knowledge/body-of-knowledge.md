# Security — Body of Knowledge

Domain knowledge for the `security` router skill: the concepts, standards, and
decision rules that govern routing and applying its ten playbooks. [DOC]

## Core concept: router, not monolith
This skill resolves ONE `topic` to ONE reference and applies that playbook. The
governing invariant is **one topic → one route**; loading multiple playbooks
degrades precision by flooding context. Topics are a closed enum mirrored between
`SKILL.md` `routes:` and `routes.json`. [DOC]

## The ten routes and their domains

### Authentication & authorization
- **auth-architecture** — Firebase Auth provider selection, custom claims as the
  RBAC carrier, session lifetime, MFA enrollment. Identity is established here. [DOC]
- **rbac-patterns** — who-can-do-what. Authorization decisions are enforced
  server-side from verified claims, never trusted from the client. [DOC]

### Input & rendering safety
- **input-sanitization** — escape vs strip at every trust boundary; XSS sinks
  (`innerHTML`, `outerHTML`, `insertAdjacentHTML`), `eval`/implied-eval, and
  injection into templated queries. Sanitize at the boundary, not deep inside. [DOC]

### Transport & browser policy
- **http-headers** — CSP, HSTS, X-Frame-Options, X-Content-Type-Options. These
  defend the rendered page; verify them on the environment users actually hit. [DOC]
- **cors-configuration** — cross-origin allow-lists, credentialed requests,
  preflight. A wildcard origin with credentials is a defect, not a convenience. [DOC]

### Abuse resistance
- **rate-limiting** — token-bucket / fixed-window throttles to blunt brute-force,
  credential-stuffing, and scraping. Limit by the strongest stable identity
  available (auth subject, then IP). [DOC]

### Posture, audit & verification
- **architecture** — end-to-end posture, trust boundaries, defense-in-depth.
- **audit-security** — read-only static audit; six canonical scan categories in
  order: `secret_exposure`, `path_security`, `hook_injection`, `sensitive_files`,
  `script_safety`, `external_network`. [EXPLICIT]
- **dual-layer-verification** — verify each invariant at two independent layers,
  static (floor) and Playwright runtime (ceiling); the layers fail differently. [DOC]
- **testing** — authoring security tests and fixtures.

## Standards & references
- **OWASP Top 10** and **OWASP ASVS** for the vulnerability classes the input,
  auth, and header routes defend against. [DOC]
- **CSP Level 3 / HSTS (RFC 6797)** for `http-headers`. [DOC]
- **Fetch CORS spec** semantics for `cors-configuration`. [DOC]
- **Constitution v6.0.0** quality gates: enforcement, evidence tags, script-first
  rule; **Constitution VII** mandates dual-layer defense-in-depth. [CONFIG]

## Decision rules
1. **Route disambiguation** — cross-origin policy → `cors-configuration`;
   CSP/HSTS/X-Frame → `http-headers`; reviewing existing code → `audit-security`;
   authoring tests → `testing`; end-to-end → `architecture`; auth subsystem alone
   → `auth-architecture`. Ask only on a true tie. [ASSUMPTION]
2. **Severity by context, not shape** — classify on *exploitable context*. A
   secret-shaped string in a doc fence is INFO/`placeholder`; in an executed
   script it is CRITICAL/`confirmed`. Placeholders are never CRITICAL. [EXPLICIT]
3. **Determinism** — `SEC-NNN` IDs ascending by category then `(path, line)`;
   `Summary` counts equal the `Findings` set; no orphan remediation. [EXPLICIT]
4. **Never green-as-success** — a passing validator confirms structure, not
   safety. Insecure output is never marked passing. [EXPLICIT]
5. **Read-only / no offense** — never mutate target files; refuse exploit/bypass
   work while still returning the read-only audit for a valid target. [EXPLICIT]
6. **Layer disagreement** — apply the disagreement protocol; clean-static +
   flagging-runtime is a real bug, not noise. Never mute the noisier check. [DOC]

## Evidence taxonomy
Alfa core set: `[CODE] [CONFIG] [DOC] [INFERENCE] [ASSUMPTION]`, plus `[EXPLICIT]`
for route descriptors. One spelling, one tag per claim. No invented prices; no
client PII; single-brand output. [DOC]
