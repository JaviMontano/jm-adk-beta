<!-- distilled from alfa skills/angular-development -->
<!-- > -->
# Angular Development

> "Angular is a platform for building mobile and desktop web applications." — Angular Team

## TL;DR

Develops Angular applications using modern patterns including Signals for reactivity, standalone components, SSR with Angular Universal, typed reactive forms, and efficient RxJS operator chains. Use this skill when building Angular applications, migrating to modern Angular patterns, or establishing Angular best practices for a team. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify Angular version and available features (Signals require v16+)
- Review existing project structure: modules vs. standalone, state management approach
- Audit RxJS usage: operator chains, subscription management, memory leaks
- Check build configuration: esbuild, SSR setup, lazy loading routes

### Step 2: Analyze
- Plan component architecture: standalone components with explicit imports
- Design state strategy: Signals for local state, NgRx/SignalStore for complex global state
- Evaluate routing: lazy-loaded routes, guards, resolvers, nested routing
- Plan form strategy: reactive forms with typed FormGroup/FormControl
- Assess SSR needs: Angular Universal or Angular SSR for SEO-critical pages

### Step 3: Execute
- Implement standalone components with focused, explicit dependency declarations
- Use Signals for reactive state: `signal()`, `computed()`, `effect()`
- Build reactive forms with strict typing and custom validators
- Implement smart/dumb component pattern with OnPush change detection
- Set up lazy-loaded route modules with preloading strategies
- Configure SSR with hydration for SEO-critical pages
- Implement HTTP interceptors for auth tokens, error handling, and logging

### Step 4: Validate
- Verify no memory leaks: all subscriptions unsubscribed (takeUntilDestroyed)
- Confirm OnPush change detection works correctly with Signals
- Check lazy-loaded routes load on demand (not bundled in main chunk)
- Test SSR renders correctly and hydration does not cause layout shifts

## Quality Criteria

- [ ] Components are standalone with explicit imports
- [ ] Signals used for reactive state where applicable
- [ ] RxJS subscriptions are properly managed (no memory leaks)
- [ ] Forms use typed reactive forms with validation
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Manual subscription management instead of using async pipe or takeUntilDestroyed
- NgModule-heavy architecture when standalone components are available
- Putting business logic in components instead of services

## Related Skills

- `typescript-patterns` — TypeScript patterns powering Angular applications
- `state-management` — NgRx and SignalStore patterns
- `component-architecture` — component design patterns applicable to Angular

## Usage

Example invocations:

- "/angular-development" — Run the full angular development workflow
- "angular development on this project" — Apply to current context


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
