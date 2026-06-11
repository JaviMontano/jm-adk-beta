<!-- distilled from alfa skills/web-components -->
<!-- > -->
# Web Components

> "The best component is the one that works everywhere without asking permission." — Alex Russell

## TL;DR

Guides the creation of framework-agnostic UI components using Web Components standards (Custom Elements v1, Shadow DOM, slots, HTML templates) and the Lit library for ergonomic development. Use when you need reusable components that work across any framework or vanilla HTML. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify reusable UI patterns in the project that benefit from encapsulation
- Check for existing component libraries or design system tokens
- Determine if Lit or vanilla Custom Elements best fit the project
- Review browser support requirements and polyfill needs

### Step 2: Analyze
- Define component API: attributes vs properties, events, slots, CSS custom properties
- Plan Shadow DOM boundary — what styles leak in/out, what content is slotted
- Evaluate state management needs (internal state, reactive properties, context)
- Design the component lifecycle (connectedCallback, disconnectedCallback, attributeChangedCallback)

### Step 3: Execute
- Create Custom Element class extending HTMLElement or LitElement
- Implement Shadow DOM with declarative templates and named slots
- Expose CSS custom properties and `::part()` selectors for theming
- Add `observedAttributes` and property reflection for framework interop
- Publish as npm package or import map module

### Step 4: Validate
- Test in multiple frameworks (React, Vue, Angular, vanilla HTML)
- Verify slot content projection and fallback content
- Confirm CSS encapsulation — no style leakage in either direction
- Check SSR compatibility and hydration if applicable

## Quality Criteria

- [ ] Component registers with a hyphenated tag name per spec
- [ ] Shadow DOM encapsulates styles without breaking host page
- [ ] All public API documented (attributes, properties, events, slots, CSS parts)
- [ ] Works without a framework — pure HTML + JS usage validated
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Using Shadow DOM when light DOM styling is actually needed
- Reflecting every property to attributes (heavy DOM mutations)
- Putting business logic inside components instead of keeping them presentational

## Related Skills

- `dark-mode` — CSS custom properties bridge theme tokens into Shadow DOM
- `accessibility-testing` — Shadow DOM requires careful ARIA and focus management

## Usage

Example invocations:

- "/web-components" — Run the full web components workflow
- "web components on this project" — Apply to current context


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
