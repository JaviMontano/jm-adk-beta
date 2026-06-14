<!-- distilled from alfa skills/auth-architecture -->
<!-- Firebase Auth setup. Custom claims for RBAC. Session management. MFA configuration. Provider selection. [EXPLICIT] -->
# auth-architecture {Architecture} (v1.1)
> **"Auth is not a feature. It's the foundation."**
## Purpose
Designs authentication and authorization architecture using Firebase Auth: provider selection, custom claims for RBAC, session management, and MFA. [EXPLICIT]
**When to use:** Setting up or hardening auth for any Firebase project.
**Anti-scope:** Not for non-Firebase IdPs (raw OIDC/SAML, Auth0, Cognito), payment authz, or app-layer business rules beyond `request.auth`. Redirect those. [SUPUESTO]
## Core Principles
1. **Law of Claims:** Custom claims carry roles (admin, editor, viewer). Set via Admin SDK only — never client-writable. Cap total claims at 1000 bytes; store coarse roles, not per-resource grants. [EXPLICIT]
2. **Law of Rules:** Firestore Security Rules authorize off `request.auth.token` claims, never off client-sent fields. Rules are the enforcement boundary; client checks are UX only. [EXPLICIT]
3. **Law of Providers:** Start with email/password + Google; add others on real demand. Each provider is attack surface + account-linking complexity. [INFERENCIA]
4. **Law of Propagation:** Claim changes reach the client only on token refresh (~1h, or forced refresh). Treat RBAC changes as eventually-consistent. [INFERENCIA]
## Core Process
### Phase 1: Select auth providers based on user requirements.
Decide email/password vs federated vs anonymous→permanent upgrade. Define account-linking policy when one email arrives via multiple providers. [INFERENCIA]
### Phase 2: Design role hierarchy and custom claims structure.
Flat role enum over nested objects (Rules read it cheaply; stays under the byte cap). Document who calls `setCustomUserClaims` and the revocation path. [INFERENCIA]
### Phase 3: Design Security Rules that enforce claims. Configure MFA if required.
Default-deny; grant by claim. Gate sensitive ops behind MFA (`firebase.sign_in_second_factor`). Plan token-refresh latency into authz UX. [EXPLICIT]
## Worked Example — claims + Rule
```js
// Admin SDK (trusted backend)
await admin.auth().setCustomUserClaims(uid, { role: "editor" });
```
```
// Firestore Rules
allow write: if request.auth.token.role in ["admin", "editor"];
```
## Decisions & Trade-offs
| Decision | Choice | Trade-off |
|----------|--------|-----------|
| Roles store | Custom claims, not Firestore doc | Fast Rules eval; but stale until token refresh [INFERENCIA] |
| Session length | Default 1h ID token + refresh token | Lower re-auth friction vs slower revocation [SUPUESTO] |
| MFA scope | Sensitive ops only, not whole-session | Usability vs uniform assurance [INFERENCIA] |
## Failure Modes
- **Claim bloat** (>1000B) → `setCustomUserClaims` rejects. Keep roles coarse. [EXPLICIT]
- **Stale authz** after role change → user keeps old access ~1h. Force refresh or short-TTL on critical paths. [INFERENCIA]
- **Rules trust client data** → privilege escalation. Authorize only off `request.auth.token`. [EXPLICIT]
- **Revocation gap** → revoke refresh tokens (`revokeRefreshTokens`) for true logout-everywhere. [DOC]
- **Account-linking collision** → same email, two providers, split accounts. Set linking policy in Phase 1. [INFERENCIA]
## Validation Gate
- [ ] Auth providers selected, documented, account-linking policy set
- [ ] Custom claims structure defined, under byte cap, Admin-SDK-only writes
- [ ] Security Rules default-deny and enforce claims (not client fields)
- [ ] Session + revocation strategy documented (refresh-token revocation path)
- [ ] MFA configured for sensitive operations if required
## Usage
Example invocations:
- "/auth-architecture" — Run the full auth architecture workflow
- "auth architecture on this project" — Apply to current context
## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Firebase Auth + Firestore is the target stack; other IdPs out of scope [SUPUESTO]
- English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
## Edge Cases
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request (non-Firebase IdP) | Redirect to appropriate skill or escalate |
| Role change must take effect now | Force token refresh; do not rely on 1h expiry |
