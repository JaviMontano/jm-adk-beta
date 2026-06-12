<!-- distilled from alfa skills/rbac-patterns -->
<!-- > -->
# Rbac Patterns
> "Method over hacks."
## TL;DR
Design role-based access control: model roles → permissions as a matrix, enforce server-side, distribute claims via Firebase custom claims (or equivalent token claims). Deny by default. [DOC]

## Core model
- **Subject** (user/service) → **Role(s)** → **Permission(s)** → **Resource + Action**. Never bind permissions to users directly; always through roles. [INFERENCIA]
- Permission grain = `resource:action` (e.g. `invoice:read`, `invoice:approve`). Coarser than per-field; finer than per-screen. [SUPUESTO] verify against the app's actual authz checks before locking grain.
- Roles compose, permissions don't: a user holding two roles gets the union of permissions. Model role hierarchy as inheritance (`admin` ⊇ `editor` ⊇ `viewer`), not duplication. [INFERENCIA]

## Permission matrix (worked example)
| Role \ Action | invoice:read | invoice:create | invoice:approve | user:manage |
|---|---|---|---|---|
| viewer | ✓ | | | |
| editor | ✓ | ✓ | | |
| approver | ✓ | ✓ | ✓ | |
| admin | ✓ | ✓ | ✓ | ✓ |
The matrix IS the source of truth — generate enforcement checks from it, don't hand-maintain both. [INFERENCIA]

## Firebase custom claims pattern
- Set roles as claims server-side only (Admin SDK), never from the client: `setCustomUserClaims(uid, { roles: ['editor'] })`. [DOC]
- Keep claims small: store **role names**, not the expanded permission set — claims cap at 1000 bytes and changes require token refresh. [DOC]
- Resolve role→permission **server-side per request**; the token carries identity + roles, the backend owns the matrix. [INFERENCIA]
- Propagation lag: claims update only on next ID-token refresh (≈1h, or force `getIdToken(true)`). Treat a freshly-revoked role as still-active until refresh — for instant revocation, check a server-side denylist, not just the claim. [SUPUESTO] confirm token TTL in project auth config.

## Procedure
### Step 1: Discover
- Enumerate resources, actions, and the distinct user personas. List who must be denied, not just who's allowed.
### Step 2: Analyze
- Build the permission matrix; collapse personas into the fewest roles that preserve required separations (esp. separation-of-duties, e.g. creator ≠ approver). Evaluate per Constitution XIII/XIV.
### Step 3: Execute
- Implement deny-by-default enforcement at the server boundary; emit the matrix + claim-shape with evidence tags.
### Step 4: Validate
- Verify each matrix cell with a positive AND negative test; confirm no client-trusted authz.

## Quality Criteria
- [ ] Deny-by-default: unmapped `resource:action` is rejected, not allowed [DOC]
- [ ] Enforcement is server-side; client checks are UX-only, never authoritative
- [ ] Roles, not users, hold permissions; separation-of-duties preserved
- [ ] Evidence tags applied (Alfa set) and Constitution-compliant
- [ ] Each matrix cell covered by a negative test

## Usage
Example invocations:
- "/rbac-patterns" — Run the full rbac patterns workflow
- "rbac patterns on this project" — Apply to current context

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs) [SUPUESTO]
- English-language output unless otherwise specified [SUPUESTO]
- RBAC only — does not cover ABAC/relationship-based (ReBAC) authz; if rules depend on resource attributes or ownership, RBAC alone is insufficient [INFERENCIA]
- Does not replace domain expert judgment for final approval-flow decisions [SUPUESTO]
- Anti-scope: no secret/key management, no network-layer authz, no audit-log design

## Edge Cases & Failure Modes
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope (ABAC/ReBAC) request | Redirect to appropriate skill or escalate |
| User holds conflicting roles | Union of permissions applies; flag if it breaks separation-of-duties |
| Role revoked but token still valid | Stale until refresh — enforce server-side denylist for instant revocation |
| Permission added but no role grants it | Orphan permission — unreachable; flag in matrix review |
| Client sends role in request body | Ignore entirely; trust only server-verified token claims |
| New resource with no matrix row | Deny-by-default until matrix updated |
