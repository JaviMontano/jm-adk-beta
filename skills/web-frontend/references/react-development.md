<!-- distilled from alfa skills/react-development -->
<!-- > -->
# React Development

> "React makes it painless to create interactive UIs." — React Team

## TL;DR

Develops React applications using modern patterns including Hooks, React Server Components (RSC), Suspense for data loading, and the Context API for dependency injection and theming. Use this skill when building React applications, migrating to React 19 patterns, or establishing React best practices. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify React version and framework (Next.js App Router, Remix, Vite)
- Review existing patterns: class vs. functional components, state management library
- Audit hook usage: custom hooks, dependency arrays, effect cleanup
- Check Server Component vs. Client Component boundaries

### Step 2: Analyze
- Design component hierarchy with clear Server/Client Component boundaries
- Plan state management: useState/useReducer for local, Context for shared, external store for complex
- Evaluate data fetching: Server Components for initial data, React Query/SWR for client mutations
- Design Suspense boundaries for loading states at appropriate granularity
- Plan error boundaries for graceful error handling per feature

### Step 3: Execute
- Implement Server Components for data fetching and static rendering
- Add 'use client' directive only where interactivity is needed
- Build custom hooks for reusable stateful logic (useDebounce, useMediaQuery)
- Implement Suspense boundaries with skeleton loading states
- Use React.memo, useMemo, useCallback for performance-critical paths
- Set up error boundaries with fallback UI per feature section
- Implement streaming SSR with Next.js App Router for progressive loading

### Step 4: Validate
- Verify Server Components do not import client-only libraries
- Confirm no unnecessary re-renders using React DevTools Profiler
- Check that Suspense boundaries provide meaningful loading states
- Test error boundaries handle and recover from errors gracefully

## Quality Criteria

- [ ] Server/Client Component boundary is intentional and minimizes client JS
- [ ] Custom hooks encapsulate reusable logic with proper cleanup
- [ ] Suspense boundaries exist at meaningful loading granularity
- [ ] Performance optimizations (memo, useMemo) are measured, not premature
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- 'use client' at the top of every file, negating Server Components benefits
- useEffect for data fetching that should be done in Server Components
- Missing dependency array items in useEffect causing stale closures

## Related Skills

- `typescript-patterns` — type-safe React with TypeScript
- `state-management` — React state management strategies
- `component-architecture` — component patterns applicable to React

## Usage

Example invocations:

- "/react-development" — Run the full react development workflow
- "react development on this project" — Apply to current context


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
