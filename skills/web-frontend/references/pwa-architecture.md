<!-- distilled from alfa skills/pwa-architecture -->
<!-- Progressive Web App design. Service workers, Web App Manifest, offline-first, push notifications via FCM. [EXPLICIT] -->
# pwa-architecture {Architecture} (v1.1)
> **"Architecture is decisions. Document every one."**
## Purpose
Progressive Web App design on Firebase/Google: service workers, Web App Manifest, offline-first, FCM push. [EXPLICIT]
**When to use:** Designing or reviewing PWA architecture for Firebase/Google stack projects.
**Anti-scope:** Native iOS/Android (use mobile-architecture); non-Firebase backends; SEO/SSR strategy (defer to framework skill).
## Core Principles
1. **Law of Firebase-First:** All decisions constrained to Firebase/Google ecosystem (R-002). [EXPLICIT]
2. **Law of Evidence:** Every claim tagged [CODE], [CONFIG], [DOC], [INFERENCE], or [ASSUMPTION]. [EXPLICIT]
3. **Law of Diagrams:** Architecture without diagrams is incomplete. Mermaid for C4, sequence, flow. [EXPLICIT]
4. **Law of Offline-First:** App shell must render and core reads must resolve with zero network. [INFERENCE]
## PWA Building Blocks
- **Service worker** — lifecycle install→activate→fetch; precache app shell on install, clean stale caches on activate, intercept fetch. Register after `load` to avoid blocking first paint. [DOC]
- **Web App Manifest** — required for installability: `name`, `short_name`, `start_url`, `display: standalone`, `theme_color`, icons incl. 192px + 512px maskable. [DOC]
- **FCM push** — `firebase-messaging-sw.js` handles `onBackgroundMessage`; foreground via `onMessage`. Requires Notification permission + VAPID key. [CONFIG]
- **Storage tiers** — Cache API (assets), IndexedDB (structured/offline writes), Firestore offline persistence (synced reads/writes). [DOC]
## Caching Strategy (decide per route)
| Route type | Strategy | Trade-off |
|------------|----------|-----------|
| App shell, fonts, JS/CSS | Cache-first + versioned precache | Fast, but needs cache-bust on deploy [INFERENCE] |
| API/Firestore reads | Stale-while-revalidate | Instant UI, brief staleness [INFERENCE] |
| Auth, payments, mutations | Network-only | Correctness over offline [ASSUMPTION] |
| User uploads (offline) | Background Sync queue → retry | Eventual consistency [DOC] |
## Core Process
### Phase 1: Analyze requirements, offline scope, install targets, push needs.
### Phase 2: Design with Firebase/Google services; map each route to a caching strategy.
### Phase 3: Document with C4 diagrams, ADRs, evidence tags.
## Validation Gate
- [ ] Architecture within Firebase/Google/Hostinger constraints; no AWS/Azure/Docker references
- [ ] C4 or sequence diagrams produced (Mermaid)
- [ ] Manifest installability fields + maskable 192/512 icons specified
- [ ] Service-worker lifecycle, cache-versioning, and update flow documented
- [ ] Each route mapped to a caching strategy; offline-first reads identified
- [ ] FCM foreground + background handling defined
- [ ] Evidence tags on all claims; ADR per significant decision

## Usage
Example invocations:
- "/pwa-architecture" — Run the full PWA architecture workflow
- "pwa architecture on this project" — Apply to current context

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- HTTPS (or localhost) assumed; service workers and install prompts require secure context [DOC]

## Edge Cases & Failure Modes
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Stale service worker after deploy | Version cache names; `skipWaiting` + `clients.claim` with user-prompted reload [DOC] |
| iOS push limitations | Web push needs installed PWA + iOS 16.4+; degrade gracefully [DOC] |
| Notification permission denied | Disable push UI, fall back to in-app messaging [INFERENCE] |
| Offline write conflict | Queue via Background Sync / Firestore; resolve last-write-wins or merge [ASSUMPTION] |
| Non-secure context (HTTP) | SW unavailable; flag as blocking install/push [DOC] |
