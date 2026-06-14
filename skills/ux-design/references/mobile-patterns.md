<!-- distilled from alfa skills/mobile-patterns -->
<!-- > -->
# Mobile Patterns
> "Method over hacks."
## TL;DR
Selection guide for the core touch patterns: bottom sheets, pull-to-refresh, swipe actions, FAB, gesture navigation. Pick by intent + reachability, not novelty. [EXPLICIT]

## Pattern Selection
| Pattern | Use when | Avoid when | Hard constraints |
|---------|----------|-----------|------------------|
| Bottom sheet | Contextual actions/filters without leaving screen | Content needs full focus or deep nav | Min touch target 44x44pt (iOS) / 48x48dp (Android); drag handle + tap-scrim dismiss; respect safe-area inset [EXPLICIT] |
| Pull-to-refresh | Manually refreshing a top-anchored feed | Paginated/infinite lists where scroll-up is frequent; non-list screens | Pair with visible spinner; debounce to avoid double-fetch; never sole refresh path (offer manual control) [EXPLICIT] |
| Swipe actions | Fast row-level verbs (archive, delete) on lists | Destructive action without undo; >2 actions per side | Each swipe action needs an equivalent tap path (a11y); confirm or offer undo for destructive [INFERENCIA] |
| FAB | One dominant, screen-wide create action | Multiple co-equal actions; scroll-heavy screens that occlude it | Exactly one primary FAB per screen; keep in thumb zone; don't cover list content/last row [EXPLICIT] |
| Gesture navigation | Back/dismiss as ambient affordance | Sole discovery path for a feature; conflicts with system edge-swipe | Always pair gesture with a visible control; reserve OS edge gestures [EXPLICIT] |

## Decision Order
1. Discover: capture intent, target platform (iOS/Android), one-handed reachability needs. [EXPLICIT]
2. Analyze: map intent to the table above per Constitution XIII/XIV; reject patterns failing a hard constraint. [EXPLICIT]
3. Execute: implement with evidence tags; wire the a11y fallback path before the gesture. [EXPLICIT]
4. Validate: run Quality Criteria + Acceptance Criteria below. [EXPLICIT]

## Acceptance Criteria
- [ ] Every gesture/swipe has a discoverable tap equivalent (a11y) [EXPLICIT]
- [ ] All interactive targets >= 44pt/48dp; FAB and sheets honor safe-area insets [EXPLICIT]
- [ ] Destructive swipe/action is reversible (undo) or confirmed [INFERENCIA]
- [ ] Exactly one primary FAB per screen; no occluded content [EXPLICIT]
- [ ] Platform conventions respected (no Android-style pull on iOS modal sheets) [INFERENCIA]

## Quality Criteria
- [ ] Evidence tags applied
- [ ] Constitution-compliant
- [ ] Actionable output

## Failure Modes
- Gesture-only navigation: feature undiscoverable -> always pair with visible control. [EXPLICIT]
- Pull-to-refresh on infinite list: accidental refresh + duplicate fetch -> debounce, prefer auto-load. [EXPLICIT]
- Swipe-to-delete without undo: irreversible data loss -> add undo snackbar. [INFERENCIA]
- FAB over list tail: last item untappable -> inset list or hide FAB on scroll. [EXPLICIT]
- Edge-gesture clash with OS back: dead zone -> keep app gestures off the screen edge. [EXPLICIT]

## Usage

Example invocations:

- "/mobile-patterns" — Run the full mobile patterns workflow
- "mobile patterns on this project" — Apply to current context

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Targets phone form factor; tablet/foldable split-view out of scope here [SUPUESTO]
- Touch-target/safe-area figures are iOS/Android baselines; verify vs. current platform HIG/Material on use [INFERENCIA]
- English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Pattern fails a hard constraint | Reject pattern, propose compliant alternative from table |
| Two patterns compete (FAB vs bottom sheet) | Prefer single primary action; demote the other to a menu |
