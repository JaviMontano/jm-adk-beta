<!-- distilled from alfa skills/component-architecture -->
<!-- > -->
# Component Architecture

> "Composition over inheritance." — Gang of Four

## TL;DR

Designs scalable frontend component hierarchies with clear module boundaries, interface contracts, and composition patterns that promote reusability and testability. Use this skill when building component libraries, structuring large frontend applications, or when component coupling is causing maintenance issues. [EXPLICIT]

**In scope:** hierarchy, boundaries, prop/slot contracts, composition strategy, folder layout, naming. **Out of scope (anti-scope):** state-store design (`state-management`), token/theme definition (`design-system`), routing, data-fetching/caching, bundling/perf budgets, a11y audits — name the boundary and hand off rather than absorbing it. [INFERENCIA]

## Procedure

### Step 1: Discover
- Audit existing component structure and identify coupling issues
- Map component categories: layout, navigation, data display, forms, feedback
- Identify shared components vs. feature-specific components
- Review existing design system tokens and patterns
- Capture current pain (e.g. files >300 LOC, props >10, duplicated variants) as a baseline so improvement is measurable, not asserted [INFERENCIA]

### Step 2: Analyze
- Apply smart/dumb (container/presentational) separation
- Identify compound component opportunities (components that work together as a unit)
- Design interface contracts: required props, optional props, render props, slots
- Plan component composition strategy: HOCs, render props, hooks, or slots

**Composition decision (pick ONE primary axis; justify the trade-off):** [INFERENCIA]
| Pattern | Use when | Trade-off accepted |
|---------|----------|--------------------|
| Hooks | Sharing *logic*, no shared markup | No DOM contract; caller owns render |
| Compound (Context) | Parts share implicit state (`Tabs`/`Tab`) | Parts coupled to parent; harder to use à la carte |
| Slots / children-as-prop | Caller owns layout, parent owns behavior | Looser typing of slot content |
| Render props | Caller needs parent's internal state inline | Verbosity, nesting if overused |
| HOC | Cross-cutting wrap, legacy interop | Wrapper hell, prop-name collisions — prefer hooks for new code |

### Step 3: Execute
- Define module boundaries with clear public APIs (barrel exports)
- Create component interface contracts with TypeScript props interfaces
- Implement compound component patterns for complex interactive elements
- Design a folder structure that reflects component hierarchy and ownership
- Document component usage examples with props variations
- Establish naming conventions: PascalCase, prefix conventions, file organization

**Worked example — compound over a 12-prop monolith:** [INFERENCIA]
```tsx
// BEFORE: god API, every variant a boolean prop
<Modal title open onClose hasFooter footerAlign primaryLabel ... />

// AFTER: compound, slots own layout, parent owns open/close + focus trap
<Modal open onOpenChange={set}>
  <Modal.Header>Delete project?</Modal.Header>
  <Modal.Body>This cannot be undone.</Modal.Body>
  <Modal.Footer><Button onClick={set}>Cancel</Button><Button danger>Delete</Button></Modal.Footer>
</Modal>
```
Public API stays one symbol (`Modal`); barrel re-exports only it, never the sub-parts' files. [INFERENCIA]

**Barrel discipline:** export the public surface from `index.ts`; do NOT re-export internals (hooks, helpers, sub-part files) or barrels that import sibling barrels — both create cycles and defeat tree-shaking. [INFERENCIA]

### Step 4: Validate
- Verify components have single responsibility (one reason to change)
- Confirm interface contracts are minimal — no unnecessary props
- Check that smart components don't contain presentational logic
- Validate components are testable in isolation without heavy mocking
- Confirm no barrel import cycle (`madge --circular` or equivalent) and that removing the component from its barrel breaks only intended call sites [INFERENCIA]

## Quality Criteria

- [ ] Components follow single responsibility principle
- [ ] Interface contracts are typed and documented with examples
- [ ] Smart/dumb separation is consistently applied
- [ ] Module boundaries have explicit public APIs via barrel exports
- [ ] Composition axis chosen per component with trade-off recorded
- [ ] No circular barrel imports; internals not re-exported
- [ ] Evidence tags applied to all claims

## Acceptance Criteria (done = all true)

- Each touched component has ≤1 reason to change and a typed props interface with ≥1 usage example. [SUPUESTO]
- Container components contain zero JSX styling/layout; presentational components hold zero data-fetching or store access. [INFERENCIA]
- Public API of each module is a single barrel; `madge --circular src` reports no cycles. [INFERENCIA]
- Baseline pain metrics from Step 1 (LOC, prop count, duplication) are measurably reduced and the deltas are reported. [INFERENCIA]
- Every claim in deliverables carries exactly one tag from a single family. [DOC]

## Anti-Patterns

- God component: one component handling display, state, and business logic
- Prop drilling through 5+ levels instead of using context or state management
- Tightly coupled components that cannot be tested or used independently
- Boolean-prop explosion (`isPrimary`/`isLarge`/`isGhost`...) where a `variant` union or compound parts belong [INFERENCIA]
- Premature abstraction: extracting a shared component before the 2nd real use (rule of three) — duplication is cheaper than the wrong contract [INFERENCIA]
- Barrel re-exporting internals, creating import cycles and breaking tree-shaking [INFERENCIA]

## Failure Modes & Recovery

| Failure mode | Signal | Recovery |
|--------------|--------|----------|
| Over-abstraction | Generic component with config-soup props, one caller | Inline back; re-extract on 3rd use |
| Context overuse | Every value in a provider, re-renders cascade | Split contexts by change cadence; lift only shared state |
| Circular barrels | Build/runtime `undefined` export, HMR loops | Break cycle; import leaf modules directly, not via barrel |
| Compound misuse | Sub-parts used outside parent, silent no-op | Guard with context check that throws a clear dev error |
| Untestable unit | Test needs 5+ mocks | Push side-effects to container; keep leaf pure |

## Related Skills

- `design-system` — design tokens consumed by components
- `state-management` — state boundaries align with component architecture
- `responsive-design` — components adapt to viewport using architecture patterns

## Usage

Example invocations:

- "/component-architecture" — Run the full component architecture workflow
- "component architecture on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Patterns assume a component framework with composition primitives (React/Vue/Svelte/Solid); imperative/template-only stacks need adaptation [SUPUESTO]
- TypeScript examples are illustrative — JS projects apply the same contracts via PropTypes/JSDoc [INFERENCIA]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| No design system exists yet | Proceed with local contracts; flag token gap, hand off to `design-system` [INFERENCIA] |
| Legacy class components / no TS | Apply same boundaries via PropTypes; defer migration as separate scope [INFERENCIA] |
| Micro-frontend / multi-team ownership | Treat each MFE boundary as a hard public API; version the barrel contract [SUPUESTO] |
