<!-- distilled from alfa skills/notification-ux -->
<!-- > -->
# Notification Ux
> "Method over hacks."
## TL;DR
Decide the right channel (toast / badge / inbox / interrupt) per message by urgency × interruptibility, then design dismissal, persistence, and grouping so signal survives and noise dies. [EXPLICIT]

## Scope
In: in-app surfaces — transient toasts, badge counts, notification center/inbox, banners, in-context inline alerts, and priority ranking across them. [EXPLICIT]
Out: OS push delivery, email/SMS transport, consent/opt-in legal flows, copy/tone (see `ux-writing`). Reference those skills; do not duplicate. [SUPUESTO]

## Channel decision
Pick by urgency (does it need action now?) and interruptibility (is blocking the user justified?). [INFERENCIA]

| Pattern | Use when | Persistence | Dismissal |
|---|---|---|---|
| Toast | Confirm an action just taken | Auto-dismiss 4–6s | Auto + manual close |
| Inline alert | Error/state tied to a field or region | Until resolved | Resolves on fix |
| Badge | Count of unseen items, no urgency | Until viewed | Clears on view |
| Inbox/center | History + low-priority digestable items | Persistent | Read/archive |
| Banner | System-wide state (outage, maintenance) | Until condition clears | Manual, sticky |
| Modal/interrupt | Irreversible/destructive needing a decision | Blocks until answered | Explicit choice |

Default to the *least* interruptive pattern that still gets the job done; escalate only with evidence the user missed it. [INFERENCIA]

## Procedure
1. **Discover** — inventory every notify-worthy event; tag each with urgency, interruptibility, and whether it needs history. [EXPLICIT]
2. **Map** — assign each event to a pattern via the table; flag any event mapping to modal/interrupt for review (interrupts are expensive). [EXPLICIT]
3. **Design** — specify timing, grouping/coalescing rules, dismissal, persistence, and empty/zero states per surface. [EXPLICIT]
4. **Validate** — against Quality Criteria + Edge Cases; tag every design claim. [EXPLICIT]

## Decisions & trade-offs
- **Auto-dismiss 4–6s for toasts**: long enough to read one line, short enough not to stack; never auto-dismiss anything carrying an action the user must take — that belongs in inbox/inline. [SUPUESTO]
- **Coalesce bursts** ("12 new messages", not 12 toasts) to protect signal; trade-off is loss of per-item immediacy — acceptable for non-urgent classes. [INFERENCIA]
- **Badges count, toasts announce, inbox remembers** — never use one to do another's job (e.g. a toast as the only record of an error is data loss). [INFERENCIA]
- **Accessibility is not optional**: route via ARIA live regions — `polite` for toasts, `assertive` for errors; never color-only signals. [SUPUESTO] → verify with screen-reader pass.

## Quality Criteria
- [ ] Every event mapped to exactly one primary pattern, justified by urgency × interruptibility [EXPLICIT]
- [ ] Dismissal, persistence, and grouping defined per surface [EXPLICIT]
- [ ] Action-bearing notifications are recoverable (not toast-only) [EXPLICIT]
- [ ] Live-region role + reduced-motion + focus order specified [EXPLICIT]
- [ ] Empty/zero state defined for badges and inbox [EXPLICIT]
- [ ] Evidence tags applied; Constitution XIII/XIV honored [EXPLICIT]

## Usage
- "/notification-ux" — Run the full notification ux workflow
- "notification ux on this project" — Apply to current context

## Assumptions & Limits
- Assumes access to the event inventory and target surfaces (web/mobile/desktop) [EXPLICIT]
- English-language output unless otherwise specified [EXPLICIT]
- Covers design/spec only — not delivery infra, throttling backend, or push consent [EXPLICIT]
- Does not replace domain/legal judgment on opt-in or regulated alerts [EXPLICIT]

## Edge Cases & Failure Modes
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Notification storm / burst | Coalesce + rate-limit per class; collapse to one summary toast |
| Stacked toasts overflow | Cap visible (e.g. 3), queue rest, oldest auto-dismisses first |
| Stale notification (event resolved) | Auto-retract or mark resolved; never leave dead state |
| Offline → reconnect flood | Batch on reconnect; show one "synced" summary, not the backlog |
| Critical alert dismissed unseen | Escalate persistence (inbox + badge), do not silently drop |
| Duplicate events | Dedupe by event key before surfacing |
