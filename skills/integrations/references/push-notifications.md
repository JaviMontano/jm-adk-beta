<!-- distilled from alfa skills/push-notifications -->
<!-- > -->
# Push Notifications

> "A notification should feel like a helpful tap on the shoulder, not a slap in the face." — Unknown

## TL;DR

Guides push notification implementation using Firebase Cloud Messaging (FCM) and the Web Push API — from permission requests to topic-based messaging, notification strategies, and user preference management. Use when your app needs to re-engage users with timely, relevant notifications. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify notification use cases (new messages, order updates, reminders, marketing)
- Check browser/platform support requirements (web, Android, iOS)
- Review existing notification infrastructure and FCM setup
- Determine notification frequency and user control requirements

### Step 2: Analyze
- Design notification strategy: which events trigger notifications, and how often
- Plan permission request timing (contextual, not on first page load)
- Choose targeting: individual tokens, topics, user segments
- Evaluate notification payload: data-only vs notification + data

### Step 3: Execute
- Set up FCM in Firebase project and generate VAPID key for web push
- Implement service worker for background notification handling
- Request notification permission at a contextual moment (not page load)
- Store FCM tokens in Firestore linked to user documents
- Send notifications from Cloud Functions via Admin SDK
- Implement topic subscriptions for category-based notifications
- Build notification preferences UI for user control
- Handle token refresh and cleanup of stale tokens

### Step 4: Validate
- Test notifications in foreground and background states
- Verify token refresh updates Firestore correctly
- Confirm notification preferences are respected (no sends to opted-out users)
- Test on multiple browsers and devices

## Quality Criteria

- [ ] Permission requested at contextual moment with clear value proposition
- [ ] FCM tokens stored and refreshed in Firestore per user
- [ ] User notification preferences respected for all sends
- [ ] Stale tokens cleaned up to prevent send errors
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Requesting notification permission on first page load (high denial rate)
- Not cleaning up stale tokens (causes FCM send errors and wasted quota)
- Sending too many notifications without user control (leads to unsubscribe/block)

## Related Skills

- `cloud-functions` — notifications sent from server-side Cloud Functions
- `firebase-auth` — FCM tokens linked to authenticated users

## Usage

Example invocations:

- "/push-notifications" — Run the full push notifications workflow
- "push notifications on this project" — Apply to current context


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
