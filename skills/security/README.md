# security — skill overview

Router skill for application security playbooks. It takes one `topic` (and an
optional `depth`), resolves exactly one route, loads exactly one reference, and
applies that playbook to the caller's context. It does not load the whole
cluster — one topic, one route — because context bloat degrades precision. [DOC]

## What it does

Maps a security intent to one of ten playbooks and executes it at the requested
depth, tagging every non-obvious claim with the Alfa core evidence set. [DOC]

| topic | route | covers |
|---|---|---|
| `architecture` | `references/architecture.md` | end-to-end security posture, trust boundaries, defense-in-depth |
| `audit-security` | `references/audit-security.md` | read-only static audit, six scan categories, `SEC-NNN` findings |
| `auth-architecture` | `references/auth-architecture.md` | Firebase Auth, custom claims, sessions, MFA, provider choice |
| `cors-configuration` | `references/cors-configuration.md` | cross-origin allow-lists, credentials, preflight |
| `dual-layer-verification` | `references/dual-layer-verification.md` | static + Playwright runtime invariant checks |
| `http-headers` | `references/http-headers.md` | CSP, HSTS, X-Frame-Options, X-Content-Type-Options |
| `input-sanitization` | `references/input-sanitization.md` | escape/strip at boundaries, XSS/injection sinks |
| `rate-limiting` | `references/rate-limiting.md` | throttles, token buckets, abuse/brute-force defense |
| `rbac-patterns` | `references/rbac-patterns.md` | who-can-do-what, claim-based authorization |
| `testing` | `references/testing.md` | authoring security tests and fixtures |

## When to use

Use when a request touches authn/authz, RBAC, input handling, HTTP headers,
CORS, rate limiting, a security audit, or security testing. Do not use for
generic cybersecurity advice with no concrete target, or for offensive/exploit
work — those are refused or redirected. [DOC]

## How it routes and executes

1. Resolve `topic`. Infer from intent (login/MFA/claims → `auth-architecture`;
   who-can-do-what → `rbac-patterns`; sanitize/escape → `input-sanitization`;
   CSP/HSTS → `http-headers`; cross-origin → `cors-configuration`; whole posture
   → `architecture`; find vulns → `audit-security`; verify a fix holds →
   `dual-layer-verification`). Ask only when two routes are equally plausible. [INFERENCE]
2. Read EXACTLY ONE playbook from `routes:`. Keys are mirrored in `routes.json`;
   never invent a topic outside the enum. [DOC]
3. Apply the spine **Discover → Analyze → Execute → Validate** at the requested
   depth: `quick` = essentials; `deep` = exhaustive with verification at each step. [DOC]
4. Tag every non-obvious claim. Never mark insecure output as passing —
   green-as-success is forbidden. [DOC]

## References

- All playbooks live under `references/` (see the table above).
- Evidence taxonomy: Alfa core set `[CODE] [CONFIG] [DOC] [INFERENCE] [ASSUMPTION]`
  plus `[EXPLICIT]` for route descriptors, one spelling, one tag per claim.

## DoD bundle

This skill ships a Definition-of-Done bundle: role contracts in `agents/`,
domain knowledge in `knowledge/`, prompts in `prompts/`, a deliverable scaffold
in `templates/output.md`, eval cases in `evals/evals.json`, a worked example in
`examples/`, and deterministic assets in `assets/` (see `assets/README.md`).
