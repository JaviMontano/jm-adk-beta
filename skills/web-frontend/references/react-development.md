<!-- distilled from alfa skills/react-development -->
<!-- > -->
# React Development

> "React makes it painless to create interactive UIs." — React Team

## TL;DR

Builds React apps on modern primitives — Hooks, Server Components (RSC), Suspense, the Context API — minimizing client JS while keeping interactivity responsive. Use when building React apps, migrating to React 19, or fixing re-render/hydration/data-fetch pathologies. [EXPLICIT]

**In scope:** component boundaries (Server vs Client), hook design, Suspense/error-boundary placement, render-perf, data-fetch strategy selection. **Out of scope (anti-scope):** state-store internals (`state-management`), token/theme (`design-system`), bundling budgets (`build-optimization`), TS types (`typescript-patterns`) — name the boundary and hand off. [INFERENCIA]

## Procedure

### Step 1: Discover
- Identify React version + framework (Next.js App Router, Remix, Vite). RSC/`use client` only exist in App-Router-class setups; a Vite SPA has no Server Components — do not prescribe them. [INFERENCIA]
- Review patterns: class vs functional, state library, current Server/Client split.
- Audit hooks: custom hooks, dependency arrays, effect cleanup, stale closures.

### Step 2: Analyze
- Design hierarchy with intentional Server/Client boundaries; push `use client` to leaves, keep trees server-rendered by default. [INFERENCIA]
- Pick state per scope: `useState`/`useReducer` local, Context for low-frequency shared (theme/auth/locale), external store for high-frequency/complex. Context re-renders all consumers on value change — wrong tool for fast-changing state. [INFERENCIA]
- Data fetch: Server Components for initial/static, React Query/SWR for client mutation + cache. Never `useEffect`-fetch what a Server Component can fetch. [INFERENCIA]
- Place Suspense at meaningful granularity (per slow region, not one page-wide spinner) and an error boundary per feature section.

### Step 3: Execute
- Server Components for data fetch + static render; add `use client` only where interactivity (state, effects, browser APIs, event handlers) is required.
- Build custom hooks for reusable stateful logic (`useDebounce`, `useMediaQuery`); return stable references and clean up subscriptions.
- Suspense boundaries with skeleton fallbacks; stream SSR via App Router for progressive paint.
- Apply `React.memo`/`useMemo`/`useCallback` only on measured hot paths — see Decisions. [INFERENCIA]
- Error boundaries with fallback UI + recovery (reset key / retry) per feature.

### Step 4: Validate
- Server Components import no client-only libs (no `window`, no hook calls). [INFERENCIA]
- No avoidable re-renders — confirm with React DevTools Profiler, not by guessing.
- Suspense fallbacks are meaningful (skeleton matching layout, not bare text).
- Error boundaries catch + recover; effects with subscriptions clean up on unmount.

## Decisions & Trade-offs

| Decision | Choose when | Trade-off | Tag |
|---|---|---|---|
| Server vs Client Component | Static/data-heavy → Server; interactive → Client | Server cuts client JS but loses state/effects/browser APIs | [INFERENCIA] |
| Context vs external store | Context for low-frequency shared; store for hot/complex | Context re-renders all consumers; store adds a dependency + boilerplate | [INFERENCIA] |
| RSC fetch vs React Query | RSC for initial load; RQ for client mutation/refetch | RSC has no client cache/optimistic updates; RQ ships client JS | [INFERENCIA] |
| `memo`/`useMemo` now vs later | Only after Profiler shows a real cost | Premature memo adds complexity + can slow cold renders | [INFERENCIA] |

## Quality Criteria

- [ ] Server/Client boundary is intentional and minimizes client JS
- [ ] Custom hooks encapsulate reusable logic with proper cleanup + stable refs
- [ ] Suspense boundaries exist at meaningful loading granularity
- [ ] Performance optimizations are measured (Profiler), not premature
- [ ] No Server Component imports client-only code; no `useEffect` data-fetch that RSC could own
- [ ] Evidence tags applied to all non-obvious claims

## Acceptance Criteria

- Adding `use client` to a file does not move it up the tree — boundary stays at the leaf that needs it. [INFERENCIA]
- Every Suspense boundary has a fallback that matches the eventual layout footprint (no layout shift). [INFERENCIA]
- Every effect that subscribes/opens/timers has a cleanup return. [INFERENCIA]
- Profiler shows zero re-renders triggered by unrelated state on the target path. [INFERENCIA]

## Anti-Patterns

- `use client` at the top of every file, negating Server Component benefits.
- `useEffect` data-fetching that belongs in a Server Component or React Query.
- Missing dependency-array items causing stale closures; or over-broad deps causing effect thrash.
- One page-wide Suspense spinner instead of region-level boundaries (blocks fast content on slow). [INFERENCIA]
- `useMemo`/`useCallback` everywhere "for safety" — unmeasured, adds cost. [INFERENCIA]
- Putting fast-changing values in Context, re-rendering every consumer each tick. [INFERENCIA]

## Worked Example

Dashboard page: shell + nav are Server Components (no client JS). The filter bar is a `use client` leaf holding filter state. The data table is a Server Component fetching with the current filters, wrapped in `<Suspense fallback={<TableSkeleton/>}>` so the shell paints immediately and streams the table when ready. A per-table error boundary shows "retry" on fetch failure. Result: interactive filters, minimal client bundle, progressive paint. [INFERENCIA]

## Failure Modes

| Symptom | Likely cause | Fix |
|---|---|---|
| Hydration mismatch warning | Server/client render diverge (Date.now, random, `window`) | Gate non-deterministic code to client effect or `useId` |
| Stale data after mutation | RSC cache not invalidated | `revalidatePath`/`revalidateTag` or RQ `invalidateQueries` |
| Infinite effect loop | Object/array dep recreated each render | Memoize dep or move it into the effect |
| Whole page spinner on one slow query | Suspense boundary too high | Lower the boundary to the slow region |
| Sluggish typing in large list | Context/value changing re-renders all | Split context or move to external store |

## Related Skills

- `typescript-patterns` — type-safe React with TypeScript
- `state-management` — React state management strategies
- `component-architecture` — component patterns applicable to React

## Usage

Example invocations:

- "/react-development" — Run the full react development workflow
- "react development on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs). [EXPLICIT]
- Requires English-language output unless otherwise specified. [EXPLICIT]
- RSC/`use client`/streaming SSR guidance assumes an App-Router-class framework; degrade to client-only patterns for plain SPAs (Vite/CRA). [SUPUESTO]
- Does not replace domain expert judgment for final decisions. [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| No RSC support (Vite/CRA SPA) | Drop Server Component steps; use client fetch + React Query |
| Legacy class components | Keep working code; migrate incrementally, not big-bang |
