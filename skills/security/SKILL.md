---
name: security
version: 1.0.0
description: "Router for application security playbooks: auth, RBAC, input sanitization, headers/CORS, rate limiting, audits, security testing. Resolve one topic, load one reference. Topics: architecture, audit-security, auth-architecture, cors-configuration, dual-layer-verification, http-headers, input-sanitization, rate-limiting, rbac-patterns, testing."
params:
  topic:
    enum: [architecture, audit-security, auth-architecture, cors-configuration, dual-layer-verification, http-headers, input-sanitization, rate-limiting, rbac-patterns, testing]
    required: true
    infer: from user request; ask only if ambiguous
  depth:
    enum: [quick, deep]
    default: quick
routes:
  architecture: references/architecture.md
  audit-security: references/audit-security.md
  auth-architecture: references/auth-architecture.md
  cors-configuration: references/cors-configuration.md
  dual-layer-verification: references/dual-layer-verification.md
  http-headers: references/http-headers.md
  input-sanitization: references/input-sanitization.md
  rate-limiting: references/rate-limiting.md
  rbac-patterns: references/rbac-patterns.md
  testing: references/testing.md
---

# security

Router skill. Use when a request touches authn/authz, RBAC, input handling,
HTTP headers, CORS, rate limiting, a security audit, or security testing. [DOC]

## Contract
- **Input**: one `topic` (enum) + `depth`; infer `topic`, ask only when two
  routes are equally plausible. [DOC]
- **Output**: resolved playbook applied to context, claims tagged per
  `references/verification-tags.md` (Alfa core set, one spelling). [DOC]

## Procedure
1. Resolve `topic`. Map intent → route: login/MFA/claims → `auth-architecture`;
   who-can-do-what → `rbac-patterns`; sanitize/escape input →
   `input-sanitization`; CSP/HSTS → `http-headers`; whole posture →
   `architecture`; find vulns → `audit-security`; verify a fix holds →
   `dual-layer-verification`. [INFERENCE]
2. Read EXACTLY ONE playbook from `routes:`. Never load the cluster — context
   bloat degrades precision. [INFERENCE]
3. `depth=deep` → apply the playbook exhaustively with verification at each step;
   `quick` → essentials only. [DOC]

Spine: Discover → Analyze → Execute → Validate.
Quality gates: constitution v6.0.0 (enforcement), evidence tags, script-first rule. [CONFIG]
Gate criteria live in `assets/` (`assets/quality-rubric.json`, `assets/checklist.md`). [CONFIG]

## Topic disambiguation (edge cases)
- Cross-origin policy → `cors-configuration`; CSP/HSTS/X-Frame → `http-headers`. [ASSUMPTION]
- Reviewing existing code → `audit-security`; authoring tests → `testing`. [ASSUMPTION]
- End-to-end posture → `architecture`; auth subsystem alone → `auth-architecture`. [ASSUMPTION]

## Anti-patterns
- Loading multiple playbooks "to be safe" — one topic, one route. [INFERENCE]
- Guessing `topic` when genuinely ambiguous instead of asking. [DOC]
- Inventing routes/topics outside the enum; breaking `routes.json` keys. [DOC]
- Findings without evidence tags, or insecure output marked "passing" —
  never green-as-success. [DOC]

## Done when
One route resolved; playbook applied at requested depth; every non-obvious
claim carries one tag; no unresolved `{VACIO_CRITICO}`. [DOC]