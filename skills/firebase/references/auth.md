<!-- distilled from alfa skills/firebase-auth -->
<!-- > -->
# Firebase Authentication

> "Authentication is the front door — make it easy to enter but impossible to pick." — Unknown

## TL;DR

Guides Firebase Authentication implementation — configuring sign-in providers (email/password, Google, GitHub, phone, anonymous), managing auth state across the application, setting custom claims for role-based access, and handling auth edge cases. Use when adding user authentication to a Firebase-powered application. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify required sign-in methods (email, social, phone, anonymous)
- Check if user profile data needs to extend beyond Firebase Auth (Firestore user doc)
- Review existing auth state management and protected route patterns
- Determine custom claims requirements for roles/permissions

### Step 2: Analyze
- Plan auth flow: sign up → email verification → profile completion → app access
- Design auth state management (context provider, global store, auth observer)
- Evaluate linking multiple providers to a single account
- Plan session management (persistence: local, session, none)

### Step 3: Execute
- Enable sign-in providers in Firebase Console and configure OAuth credentials
- Implement `onAuthStateChanged` observer as the single source of auth truth
- Build sign-in/sign-up forms with proper error handling and messaging
- Add Google/GitHub OAuth sign-in with `signInWithPopup` or `signInWithRedirect`
- Set custom claims via Admin SDK in Cloud Functions (never client-side)
- Create protected route wrapper that redirects unauthenticated users
- Handle edge cases: email already in use, account linking, password reset

### Step 4: Validate
- Test all sign-in providers end-to-end (including error cases)
- Verify auth state persists across page refreshes and browser tabs
- Confirm custom claims propagate after token refresh (`getIdToken(true)`)
- Test with Firebase Auth emulator for automated testing

## Quality Criteria

- [ ] Auth state managed via `onAuthStateChanged` observer (not manual checks)
- [ ] All sign-in error codes handled with user-friendly messages
- [ ] Custom claims set server-side only (via Admin SDK in Cloud Functions)
- [ ] Email verification enforced before full account access
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Storing auth tokens in localStorage manually (Firebase SDK handles persistence)
- Setting custom claims from the client (security vulnerability)
- Checking `currentUser` synchronously on page load (it's null before auth resolves)

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

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
