<!-- distilled from alfa skills/component-designer -->
<!-- UI component architecture. Atomic design (atoms/molecules/organisms). Props contracts. Composition patterns. Accessibility built-in. [EXPLICIT] -->
# component-designer {Architecture} (v1.1)
> **"A component is a contract: props in, UI out, accessible always."**
## Purpose
Designs UI component architecture using atomic design (atoms → molecules → organisms → templates → pages). Defines props contracts, composition patterns, and accessibility requirements. [EXPLICIT]
**When to use:** Designing component libraries or page layouts for React/Angular.
**Anti-scope:** Not visual/token design (colors, spacing scales → design-system), not state management or data fetching, not backend contracts, not pixel-level styling. Outputs an architecture, not shipped code. [INFERENCE]
## Core Principles
1. **Law of Atoms:** Start small. Buttons, inputs, labels are atoms. Compose up; never let an organism reach down past one level. [EXPLICIT]
2. **Law of Props:** Every component has a typed props interface. No implicit props, no `any`, no prop that silently changes behavior of another. [EXPLICIT]
3. **Law of A11y:** Every interactive component has ARIA attributes, keyboard handling, focus management. A11y is a gate, not a backlog item. [EXPLICIT]
## Core Process
### Phase 1: Identify UI patterns from spec/designs.
Inventory repeated visual units; name recurring patterns once. [EXPLICIT]
### Phase 2: Classify into atomic levels. Define props interfaces.
Atom = no app logic, no composition. Molecule = small group of atoms with one job. Organism = section-level, may hold local UI state. Template = layout slots, no data. Page = template + real data. Tie-breaker: if it could exist in another product unchanged, push it down a level. [INFERENCE]
### Phase 3: Document composition rules and accessibility requirements.
Prefer composition (children/slots) over config booleans; collapse 3+ boolean variants into a `variant` union. Specify ARIA role, keyboard map, and focus order per interactive component. [EXPLICIT]
## Worked Example (excerpt)
`SearchField` (molecule) = `Input` (atom) + `IconButton` (atom) + `Label` (atom). Props: `{ value: string; onChange: (v: string) => void; onSubmit: () => void; label: string; disabled?: boolean }`. A11y: `role="search"` on wrapper, `Enter` submits, `Escape` clears, label bound via `htmlFor`, focus stays on input after submit. [EXPLICIT]
## Decisions & Trade-offs
- **Composition over config:** flexible, fewer prop explosions; costs more files and a steeper first read. Chosen — config-heavy components rot fastest. [INFERENCE]
- **Strict atomic levels:** clear reuse boundaries; can feel over-engineered for a 5-screen app. For small scopes, collapse template/page into one. [ASSUMPTION] verify against project size before applying.
- **A11y as a gate:** slower to "done", but retrofitting ARIA/focus is far costlier. [INFERENCE]
## Validation Gate
- [ ] Components classified by atomic level (no level-skipping in composition)
- [ ] Props interfaces defined (TypeScript), no `any`, optional vs required explicit
- [ ] Accessibility per interactive component: role, keyboard map, focus order
- [ ] Composition patterns documented; boolean-prop explosions collapsed to unions
- [ ] Each pattern named once; no duplicate components for the same job

## Usage

Example invocations:

- "/component-designer" — Run the full component designer workflow
- "component designer on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Assumes React or Angular with TypeScript; props-contract output is typed for these [ASSUMPTION] confirm framework before emitting interfaces.
- Requires English-language output unless otherwise specified [EXPLICIT]
- Produces architecture and contracts, not runnable components or styles [INFERENCE]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| No design system / token source | Note dependency; design contracts now, defer visual tokens [INFERENCE] |
| Same pattern, two slightly different uses | One component + `variant` union, not two components [INFERENCE] |
| Non-TS or vanilla-JS project | Emit prop contracts as JSDoc/PropTypes; flag loss of compile-time safety [ASSUMPTION] |
| Deeply nested / "god" organism | Split at the first reusable seam; cap nesting before it blocks reuse [INFERENCE] |
