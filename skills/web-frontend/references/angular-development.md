<!-- distilled from alfa skills/angular-development -->
<!-- > -->
# Angular Development

> "Angular is a platform for building mobile and desktop web applications." — Angular Team

## TL;DR

Builds Angular apps on modern patterns: Signals reactivity, standalone components, SSR + hydration, typed reactive forms, disciplined RxJS. Use when building, migrating to modern Angular, or setting team conventions. [EXPLICIT]

**In scope:** architecture, state, forms, routing, SSR, RxJS hygiene, change-detection. **Anti-scope:** backend/API design, CSS/design-systems (defer to `component-architecture`), e2e infra, CI/CD, non-Angular SPAs. [EXPLICIT]

## Procedure

### Step 1: Discover
- Pin Angular version — gates available patterns. Signals GA v17+ (preview v16); `@if`/`@for` control flow v17+; `input()`/`output()`/`model()` signal APIs v17.1+; zoneless dev preview v18+. Below v16 → no Signals, plan RxJS-only or upgrade first. [DOC]
- Map structure: NgModule vs standalone; state approach (services, NgRx, SignalStore); routing shape.
- Audit RxJS: operator chains, subscription teardown, leak sites (manual `.subscribe` without teardown).
- Inspect build: esbuild/`application` builder, SSR config, lazy boundaries, bundle budgets.

### Step 2: Analyze
- Components: standalone with explicit `imports`; OnPush by default.
- State decision (record trade-off): local/UI → Signals (zero boilerplate, fine-grained, no async-pipe); cross-cutting server cache → SignalStore or NgRx; large app with time-travel/devtools/effects-heavy flows → NgRx (more boilerplate, buys traceability). Default to the lightest tier that fits. [INFERENCIA]
- Routing: lazy `loadComponent`/`loadChildren`, `canMatch`/`canActivate` guards, resolvers, `withPreloading`.
- Forms: typed reactive (`FormGroup<T>`) for non-trivial/validated forms; template-driven only for trivial single-field cases. [INFERENCIA]
- SSR: enable only for SEO-critical or slow-FCP routes — it adds server runtime + hydration-mismatch surface; pure authed dashboards rarely need it. [INFERENCIA]

### Step 3: Execute
- Standalone components, focused explicit deps, `changeDetection: OnPush`.
- Signals for state: `signal()`, `computed()`, `effect()`. Convert streams at the edge with `toSignal()`; never call `.set()` inside a `computed`.
- Typed reactive forms + custom/async validators; prefer `nonNullable`.
- Smart/dumb split: containers hold state + side effects, presentationals are pure `input()`/`output()`.
- Lazy routes + preloading strategy; keep eager bundle within budget.
- SSR with client hydration (`provideClientHydration`) for SEO routes.
- HTTP interceptors (functional, `withInterceptors`) for auth, error mapping, logging.
- Teardown every long-lived subscription with `takeUntilDestroyed()` or `async` pipe.

### Step 4: Validate
- No leaks: every manual subscription has teardown; prefer `async`/`toSignal`. Verify via repeated route-enter/leave with no listener growth in devtools. [INFERENCIA]
- OnPush + Signals: view updates on signal change without manual `markForCheck`.
- Lazy routes load on demand — confirm separate chunk in build output, absent from main.
- SSR: rendered HTML matches client; no hydration NG0500-class warnings; no layout shift.

## Worked examples

```ts
// Signal state + derived + edge-converted stream
const count = signal(0);
const doubled = computed(() => count() * 2);
const user = toSignal(this.http.get<User>('/me'), { initialValue: null });
count.update(n => n + 1);              // not count.set(count()+1)

// Typed reactive form
form = new FormGroup({
  email: new FormControl('', { nonNullable: true,
    validators: [Validators.required, Validators.email] }),
});

// Leak-safe stream in a component
ngOnInit() {
  this.ticks$.pipe(takeUntilDestroyed(this.destroyRef))
    .subscribe(v => this.handle(v));   // auto-torn-down on destroy
}

// Functional auth interceptor
const auth: HttpInterceptorFn = (req, next) =>
  next(req.clone({ setHeaders: { Authorization: `Bearer ${token()}` } }));
```

## Quality Criteria

- [ ] Components standalone, OnPush, explicit `imports`
- [ ] Signals for reactive/local state where version allows
- [ ] Every subscription torn down (async pipe / `takeUntilDestroyed` / `toSignal`)
- [ ] Forms typed + validated; `nonNullable` where applicable
- [ ] Lazy routes produce distinct chunks; eager bundle within budget
- [ ] SSR routes hydrate with zero mismatch warnings (if SSR enabled)
- [ ] One evidence tag per non-obvious claim, single family

## Anti-Patterns

- Manual `.subscribe` with no teardown → memory leak. [INFERENCIA]
- NgModule-heavy architecture when standalone is available.
- Business logic in components instead of services.
- `.set()`/side effects inside `computed()` (use `effect()` or an explicit write). [DOC]
- Nested subscribes instead of `switchMap`/`mergeMap`/`concatMap`.
- Reaching for NgRx on a small app where Signals/SignalStore suffice (boilerplate tax with no payoff). [INFERENCIA]
- Mutating signal state in place — replace the value so change detection fires. [INFERENCIA]

## Failure Modes

| Symptom | Likely cause | Fix |
|---|---|---|
| View not updating | OnPush + mutated object, or signal not replaced | Emit new reference / `signal.update` |
| Memory grows per navigation | subscription without teardown | `async` pipe / `takeUntilDestroyed` |
| Hydration NG0500 mismatch | non-deterministic SSR (Date/random/`window`) | guard with `isPlatformBrowser`, stabilize render |
| `ExpressionChangedAfterChecked` | state written during CD | move to lifecycle hook / `effect()` |
| Lazy route in main bundle | static import of the component | use `loadComponent`/`loadChildren` |
| `effect()` runs unexpectedly | reads a signal you didn't intend to track | narrow reads / `untracked()` |

## Related Skills

- `typescript-patterns` — TypeScript patterns powering Angular applications
- `state-management` — NgRx and SignalStore patterns
- `component-architecture` — component design patterns applicable to Angular

## Usage

Example invocations:

- "/angular-development" — Run the full angular development workflow
- "angular development on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs). [EXPLICIT]
- Version-specific guidance assumes Angular v16+; for older versions, upgrade-first or RxJS-only path. [SUPUESTO]
- English-language output unless otherwise specified. [EXPLICIT]
- Does not replace domain expert judgment for final architectural decisions. [EXPLICIT]
- Does not cover styling/design tokens, backend contracts, or deployment infra (see Anti-scope). [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Angular < v16 | Flag Signals unavailable; propose upgrade or RxJS-only design |
| Mixed NgModule + standalone | Allow incremental migration; do not force big-bang refactor |
| SSR requested for authed-only app | Question need; SSR cost may exceed SEO benefit |
