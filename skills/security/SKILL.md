---
name: security
description: "Application security: auth, RBAC, input sanitization, headers/CORS, rate limiting, audits, and security testing. Topics: architecture, audit-security, auth-architecture, cors-configuration, dual-layer-verification, http-headers, input-sanitization, rate-limiting, rbac-patterns, testing."
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

Router skill. Resolve `topic` from the request, then Read EXACTLY ONE playbook
from `routes:`. Never load the whole cluster. `depth=deep` → apply the playbook
exhaustively with verification at each step; `quick` → essentials only.

Spine: Discover → Analyze → Execute → Validate.
Quality gates: constitution v6.0.0 (enforcement), evidence tags, script-first rule.
