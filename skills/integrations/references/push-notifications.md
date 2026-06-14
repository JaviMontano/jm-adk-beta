<!-- distilled from alfa skills/push-notifications -->
<!-- > -->
# Push Notifications

> "A notification should feel like a helpful tap on the shoulder, not a slap in the face." — Unknown

## TL;DR

Guides push notification implementation using Firebase Cloud Messaging (FCM) and the Web Push API — from permission requests to topic-based messaging, delivery strategy, and user preference management. Use when an app needs to re-engage users with timely, relevant notifications. [EXPLICIT]

## Scope & Anti-Scope

- **In scope:** web (FCM JS SDK + Web Push/VAPID), Android/iOS via FCM, topic + token + segment targeting, preference management, token lifecycle. [EXPLICIT]
- **Out of scope:** APNs-direct (non-FCM) iOS, in-app messaging (Firebase IAM is a separate product), SMS/email channels, marketing-campaign orchestration tooling. [SUPUESTO] → verify channel mix with stakeholder before scoping.
- **Decision — FCM over raw Web Push:** FCM abstracts VAPID/APNs/endpoint differences across platforms; trade-off is a Google dependency and Firebase project coupling. Choose raw Web Push only if avoiding Firebase is a hard requirement. [INFERENCIA]

## Procedure

### Step 1: Discover
- Identify notification use cases (new messages, order updates, reminders, marketing) and tag each as transactional vs promotional — they carry different consent and frequency rules. [INFERENCIA]
- Check browser/platform support: iOS Safari web push requires iOS 16.4+ and an installed (Add to Home Screen) PWA; desktop Safari, Chrome, Firefox, Edge support it directly. [SUPUESTO] → confirm against current caniuse before committing.
- Review existing FCM setup, service worker registration, and any prior token store.
- Determine frequency caps and per-category user-control requirements.

### Step 2: Analyze
- Design the strategy: which events trigger sends, expected volume, and quiet-hours/frequency caps.
- Plan permission timing — request contextually (after a user action that implies intent), never on first page load. [EXPLICIT]
- Choose targeting: individual tokens (1:1), topics (broadcast to subscribers), or server-resolved segments.
- **Decision — payload shape:** `notification`-key payloads auto-display when backgrounded but skip your handler; `data`-only payloads always invoke your handler (full control, but you must display manually and they can be throttled when the app is closed). Use `data`-only when you need custom rendering/click routing; use `notification`+`data` for simple alerts. [INFERENCIA]

### Step 3: Execute
- Set up FCM in the Firebase project and generate a VAPID key for web push. [CONFIG]
- Register a service worker (`firebase-messaging-sw.js`) for background handling. [CÓDIGO]
- Request permission at a contextual moment; handle `granted`, `denied`, and `default` (dismissed) distinctly. [EXPLICIT]
- Store FCM tokens in Firestore keyed by token (not only by user) so one user with multiple devices keeps multiple live tokens. [INFERENCIA]
- Send from Cloud Functions via the Admin SDK; never expose the server key client-side. [CONFIG]
- Implement topic subscriptions for category-based fan-out.
- Build a notification-preferences UI for per-category opt-in/out.
- Handle token refresh (`onTokenRefresh`/new token on `getToken`) and prune stale tokens on `messaging/registration-token-not-registered` errors. [CÓDIGO]

### Step 4: Validate
- Test in foreground, background, and fully-closed app states. [EXPLICIT]
- Verify token refresh updates Firestore and the old token is removed.
- Confirm preferences are honored — no sends to opted-out users or muted categories.
- Test across browsers/devices, including iOS PWA-installed Safari.
- Confirm stale-token cleanup fires on the documented error code, not a generic catch.

## Worked Example: token store + targeted send

```js
// Client: register token, dedupe by token id
const token = await getToken(messaging, { vapidKey: VAPID_KEY });
await setDoc(doc(db, 'fcmTokens', token), {
  uid, platform: 'web', updatedAt: serverTimestamp(),
  prefs: { orders: true, marketing: false },
}, { merge: true }); // [CÓDIGO]

// Cloud Function: send, then prune dead tokens
const res = await getMessaging().sendEachForMulticast({ tokens, notification, data });
res.responses.forEach((r, i) => {
  if (r.error?.code === 'messaging/registration-token-not-registered') {
    deleteDoc(doc(db, 'fcmTokens', tokens[i])); // prune stale [CÓDIGO]
  }
});
```

## Quality Criteria

- [ ] Permission requested at a contextual moment with a clear value proposition. [EXPLICIT]
- [ ] FCM tokens stored per device and refreshed in Firestore. [EXPLICIT]
- [ ] User notification preferences respected for every send, transactional and promotional. [EXPLICIT]
- [ ] Stale tokens pruned on `registration-token-not-registered` to prevent errors and wasted quota. [EXPLICIT]
- [ ] Server credentials (Admin SDK key, server key) never shipped to the client. [INFERENCIA]
- [ ] Foreground, background, and closed-app delivery all verified. [EXPLICIT]
- [ ] Evidence tags applied to all non-obvious claims. [EXPLICIT]

## Anti-Patterns

| Anti-pattern | Consequence | Correct move |
|---|---|---|
| Permission prompt on first page load | High denial; denial is sticky and hard to reverse | Prompt after an intent signal [EXPLICIT] |
| Never pruning stale tokens | FCM send errors, wasted quota, skewed delivery metrics | Prune on the not-registered error code [EXPLICIT] |
| No frequency cap / user control | Unsubscribes, OS-level block, brand damage | Per-category prefs + quiet hours [EXPLICIT] |
| Storing token keyed by uid only | Multi-device users lose notifications on one device | Key by token; keep a token set per uid [INFERENCIA] |
| Treating dismissed (`default`) as denied | Lost chance to re-ask later | Track the three states separately [INFERENCIA] |
| `notification`-key payload when custom click-routing is needed | Handler skipped when backgrounded; routing breaks | Use `data`-only payloads [INFERENCIA] |

## Related Skills

- `cloud-functions` — notifications sent from server-side Cloud Functions
- `firebase-auth` — FCM tokens linked to authenticated users

## Usage

Example invocations:

- "/push-notifications" — Run the full push notifications workflow
- "push notifications on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs). [EXPLICIT]
- Assumes a Firebase project with FCM enabled and a deployable Cloud Functions backend; without it, server-side sends are out of reach. [SUPUESTO] → confirm Firebase project + billing tier early.
- iOS web push depends on the user installing the PWA; a browser-tab-only iOS user cannot receive web push regardless of code. [SUPUESTO]
- Requires English-language output unless otherwise specified. [EXPLICIT]
- Does not replace domain expert judgment for final decisions. [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Permission previously denied | Do not re-prompt programmatically; guide user to browser/OS settings [INFERENCIA] |
| Same user, multiple devices | Maintain a token set per uid; send to all, prune individually [INFERENCIA] |
| Token expires while app closed | Refresh on next open; treat closed-app non-delivery as expected, not a bug [SUPUESTO] |
| iOS Safari, non-installed PWA | Web push unavailable; degrade gracefully or prompt to install [SUPUESTO] |
