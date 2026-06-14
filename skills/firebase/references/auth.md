<!-- distilled from alfa skills/firebase-auth -->
<!-- > -->
# Firebase Authentication

> "Authentication is the front door — make it easy to enter but impossible to pick." — Unknown

## TL;DR

Guides Firebase Authentication implementation — configuring sign-in providers (email/password, Google, GitHub, phone, anonymous), managing auth state across the application, setting custom claims for role-based access, and handling auth edge cases. Use when adding user authentication to a Firebase-powered application. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify required sign-in methods (email, social, phone, anonymous)
- Check if user profile data needs to extend beyond Firebase Auth (Firestore user doc keyed by `uid`) [INFERENCIA]
- Review existing auth state management and protected route patterns
- Determine custom claims requirements for roles/permissions; claims are capped at 1000 bytes total per user [DOC]

### Step 2: Analyze
- Plan auth flow: sign up → email verification → profile completion → app access
- Design auth state management (context provider, global store, auth observer)
- Evaluate linking multiple providers to a single account (`linkWithCredential`) vs separate accounts [DOC]
- Plan session persistence and pick one explicitly (see decision table) [INFERENCIA]

### Step 3: Execute
- Enable sign-in providers in Firebase Console and configure OAuth credentials (client ID/secret, authorized domains) [CONFIG]
- Implement `onAuthStateChanged` observer as the single source of auth truth
- Build sign-in/sign-up forms with error handling keyed on `error.code` (not message strings, which are unstable) [INFERENCIA]
- Add Google/GitHub OAuth via `signInWithPopup` or `signInWithRedirect` (see decision table)
- Set custom claims via Admin SDK in Cloud Functions (never client-side) [DOC]
- Create protected route wrapper that redirects unauthenticated users
- Handle edge cases: email already in use, account linking, password reset

### Step 4: Validate
- Test all sign-in providers end-to-end (including error cases)
- Verify auth state persists across page refreshes and browser tabs
- Confirm custom claims propagate only after token refresh — force with `getIdToken(true)` or re-login; ID tokens cache claims ~1h [DOC]
- Test with Firebase Auth emulator for deterministic automated testing [DOC]

## Decisions & Trade-offs

| Decision | Choose | Because | Trade-off |
|----------|--------|---------|-----------|
| OAuth flow | `signInWithPopup` | Keeps SPA state, simpler | Blocked by popup blockers; fails on most mobile webviews — fall back to redirect [INFERENCIA] |
| OAuth flow | `signInWithRedirect` | Works in webviews/mobile | Loses in-memory state across redirect; needs `getRedirectResult` on return [DOC] |
| Persistence | `browserLocal` (default) | Survives tab close/reopen | Token lives on shared/kiosk machines — wrong for public terminals [INFERENCIA] |
| Persistence | `browserSession` | Cleared on tab close | Lost on refresh-to-new-tab; re-auth friction [INFERENCIA] |
| Persistence | `none` (in-memory) | Highest security | Re-auth every page load — only for high-sensitivity flows [SUPUESTO] |
| Roles | Custom claims | Enforced in Security Rules + token, no extra read | 1000-byte cap; ~1h propagation lag [DOC] |
| Roles | Firestore role doc | Instant update, unbounded | Extra read per check; rules must `get()` the doc [INFERENCIA] |

## Quality Criteria

- [ ] Auth state managed via `onAuthStateChanged` observer (not manual checks)
- [ ] All sign-in error codes handled with user-friendly messages, keyed on `error.code`
- [ ] Custom claims set server-side only (via Admin SDK in Cloud Functions)
- [ ] Email verification enforced before full account access
- [ ] Session persistence chosen explicitly, not left to default
- [ ] `getRedirectResult` handled when `signInWithRedirect` is used
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Storing auth tokens in localStorage manually (Firebase SDK handles persistence) [DOC]
- Setting custom claims from the client (security vulnerability — claims are trusted by rules) [DOC]
- Checking `currentUser` synchronously on page load (it's null before auth resolves; gate UI on the observer) [DOC]
- Branching on `error.message` text instead of `error.code` (messages change across SDK versions) [INFERENCIA]
- Trusting `emailVerified` from the client without re-checking server-side for sensitive actions [SUPUESTO]
- Forgetting `getRedirectResult` after `signInWithRedirect` — sign-in silently appears to fail [INFERENCIA]

## Failure Modes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `auth/unauthorized-domain` | App domain not in Console allowlist | Add domain under Auth → Settings → Authorized domains [CONFIG] |
| New claims not visible to client | ID token still cached | `getIdToken(true)` or sign out/in to force refresh [DOC] |
| `auth/account-exists-with-different-credential` | Email already linked to another provider | Fetch sign-in methods, prompt to link via `linkWithCredential` [DOC] |
| Popup sign-in does nothing | Popup blocked / mobile webview | Fall back to `signInWithRedirect` [INFERENCIA] |
| User briefly sees logged-out UI then logs in | UI rendered before observer resolved | Render loading state until first `onAuthStateChanged` fires [INFERENCIA] |
| Rules deny despite valid role | Claim not in token yet or rules read wrong field | Confirm token refresh + rule path against claim key [INFERENCIA] |

## Worked Example: role-based gate

```js
// Server (Cloud Function, Admin SDK) — sets the claim
await admin.auth().setCustomUserClaims(uid, { role: "admin" });

// Client — force-refresh so the new claim lands in the token
await auth.currentUser.getIdToken(true);
const { claims } = await auth.currentUser.getIdTokenResult();
const isAdmin = claims.role === "admin";
```

```javascript
// Security Rule consuming the claim
allow write: if request.auth.token.role == "admin";
```

## Related Skills

- `firestore-security-rules` — rules rely on auth identity and custom claims
- `cloud-functions` — custom claims must be set via Admin SDK in functions

## Usage

Example invocations:

- "/firebase-auth" — Run the full firebase auth workflow
- "firebase auth on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Anti-scope: does NOT cover Firebase App Check, multi-tenancy (Identity Platform), or SAML/OIDC enterprise SSO — those need Identity Platform tiering [SUPUESTO]
- Phone auth assumes a billing-enabled project (SMS quota) and reCAPTCHA configured [DOC]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Anonymous → permanent account | Upgrade in place via `linkWithCredential` to preserve `uid` and data [DOC] |
| Same email, multiple providers | Resolve `account-exists-with-different-credential` by linking, not duplicating [DOC] |
| Password reset for OAuth-only user | No password exists; direct user back to their original provider [INFERENCIA] |
