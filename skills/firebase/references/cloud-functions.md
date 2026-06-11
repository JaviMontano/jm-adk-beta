<!-- distilled from alfa skills/cloud-functions -->
<!-- > -->
# Cloud Functions

> "Serverless means someone else worries about the server — but you still worry about the code." — Unknown

## TL;DR

Guides Cloud Functions for Firebase development — HTTP endpoints, Firestore document triggers, Auth event handlers, Storage upload triggers, and PubSub messaging. Covers TypeScript patterns, error handling, cold start optimization, and deployment strategies. Use when you need server-side logic in a Firebase project. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify server-side logic needs (data validation, aggregation, notifications, integrations)
- Check existing functions and their trigger types
- Review runtime configuration and environment variables
- Determine region requirements for latency optimization

### Step 2: Analyze
- Categorize functions by trigger: HTTP (callable/request), Firestore (onCreate/onUpdate/onDelete), Auth (onCreate), Scheduled, PubSub
- Plan function organization (one file per domain vs feature folders)
- Evaluate cold start impact and optimization strategies
- Design error handling and retry behavior per trigger type

### Step 3: Execute
- Set up Functions with TypeScript and `firebase-functions/v2` API
- Implement HTTP callable functions with `onCall` for authenticated endpoints
- Create Firestore triggers for data denormalization and aggregation
- Add Auth triggers for user profile initialization on sign-up
- Configure scheduled functions with `onSchedule` for periodic tasks
- Set up proper error handling: `HttpsError` for callables, retry logic for background
- Use `defineSecret` for sensitive configuration (API keys, credentials)
- Deploy to specific regions for latency optimization

### Step 4: Validate
- Test all functions locally with Firebase Emulator Suite
- Verify Firestore triggers handle idempotency (same event processed twice)
- Check function logs in Cloud Console for errors and performance
- Confirm deployment succeeds and functions respond correctly in staging

## Quality Criteria

- [ ] All functions use TypeScript with strict typing
- [ ] HTTP callable functions validate input parameters and handle errors with `HttpsError`
- [ ] Background triggers are idempotent (safe to re-execute)
- [ ] Secrets stored via `defineSecret`, never hardcoded
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Using `functions.https.onRequest` for authenticated endpoints instead of `onCall`
- Not handling cold starts (global scope initialization, lazy imports)
- Deploying all functions when only one changed (`firebase deploy --only functions:specificFn`)

## Related Skills

- `firebase-setup` — Functions are initialized as part of Firebase project setup
- `serverless-patterns` — general serverless patterns apply to Cloud Functions

## Usage

Example invocations:

- "/cloud-functions" — Run the full cloud functions workflow
- "cloud functions on this project" — Apply to current context


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
