<!-- distilled from alfa skills/web-components -->
<!-- > -->
# Web Components

> "The best component is the one that works everywhere without asking permission." — Alex Russell

## TL;DR

Guides framework-agnostic UI components using Web Components standards (Custom Elements v1, Shadow DOM, slots, HTML `<template>`) plus Lit for ergonomic development. Use when you need reusable components that work across any framework or vanilla HTML. [DOC]

**Use this when:** a design system must outlive framework churn, or the same widget ships into React + Vue + server-rendered pages. **Do NOT use when:** the component is app-internal and the team is single-framework — native React/Vue components are lighter and better-typed there. [INFERENCIA]

## Procedure

### Step 1: Discover
- Identify reusable UI patterns that benefit from encapsulation
- Check for existing component libraries or design-system tokens
- Decide Lit vs vanilla Custom Elements (decision table below)
- Review browser-support targets and polyfill needs — Custom Elements v1 + Shadow DOM v1 are baseline in all evergreen browsers; only legacy targets need polyfills [DOC]

### Step 2: Analyze
- Define the component API: attributes vs properties, events, slots, CSS custom properties
- Plan the Shadow DOM boundary — what styles leak in/out, what content is slotted
- Evaluate state needs (internal state, reactive properties, context)
- Design lifecycle: `connectedCallback`, `disconnectedCallback`, `attributeChangedCallback`

### Step 3: Execute
- Create a Custom Element class extending `HTMLElement` or `LitElement`
- Implement Shadow DOM with declarative templates and named slots
- Expose CSS custom properties and `::part()` selectors for theming
- Add `observedAttributes` + property reflection for framework interop
- Publish as an npm package or import-map module

### Step 4: Validate
- Test across React, Vue, Angular, and vanilla HTML
- Verify slot projection and fallback content
- Confirm CSS encapsulation — no leakage in either direction
- Check SSR compatibility and hydration if applicable

## Decision: Lit vs vanilla Custom Elements

| Factor | Vanilla | Lit |
|---|---|---|
| Bundle cost | 0 KB | ~5–6 KB min+gz [SUPUESTO] |
| Reactive rendering | Manual DOM diffing | Declarative, batched |
| Best for | 1–2 leaf components, zero deps | Component libraries, frequent state |
| Trade-off | More boilerplate, easy lifecycle bugs | Adds a dependency to audit/version |

Default to vanilla for a handful of static leaf widgets; choose Lit once you have reactive state or more than a few components — the boilerplate and manual-render bug surface outgrow the bundle cost. [INFERENCIA]

## Worked example (Lit)

```js
import { LitElement, html, css } from 'lit';

export class StatusBadge extends LitElement {
  static properties = { label: {}, tone: { reflect: true } }; // reflect → CSS/framework can target it
  static styles = css`
    :host { display: inline-flex; }
    .badge { padding: var(--badge-pad, 2px 8px); border-radius: 999px; }
    :host([tone="error"]) .badge { background: var(--tone-error, #fdd); }
  `;
  constructor() { super(); this.label = ''; this.tone = 'info'; }
  render() {
    return html`<span class="badge" part="badge"><slot>${this.label}</slot></span>`;
  }
}
customElements.define('status-badge', StatusBadge); // MUST be hyphenated
```

Consume anywhere: `<status-badge tone="error">Down</status-badge>`. Theme via `status-badge::part(badge) { --badge-pad: 4px 12px; }`. [CÓDIGO]

## Quality Criteria

- [ ] Tag name is hyphenated and registered once per page (guard against double-define) [DOC]
- [ ] Shadow DOM encapsulates styles without breaking the host page
- [ ] Public API documented: attributes, properties, events, slots, CSS parts
- [ ] Custom events use `composed: true` so they cross the shadow boundary [DOC]
- [ ] Works without a framework — pure HTML + JS usage validated
- [ ] Evidence tags applied to all non-obvious claims

## Anti-Patterns

- Using Shadow DOM when light-DOM styling is actually needed
- Reflecting every property to attributes — only reflect what CSS/frameworks must target (heavy DOM mutations otherwise)
- Putting business logic in components instead of keeping them presentational
- Firing events without `composed: true` — they die at the shadow boundary and frameworks never see them [INFERENCIA]
- Registering the same tag twice — the second `define` throws and breaks the page [DOC]

## Failure Modes

| Symptom | Likely cause | Fix |
|---|---|---|
| Event never reaches React/Vue handler | `composed`/`bubbles` not set | `new CustomEvent(name, { bubbles: true, composed: true })` |
| `define()` throws `already defined` | Module loaded twice / HMR | Guard: `if (!customElements.get('x')) customElements.define(...)` |
| Styles bleed onto host page | Used light DOM or global `<style>` | Move styles inside `static styles` / shadow root |
| Property set before upgrade is lost | Framework set prop pre-registration | Lit handles this; vanilla needs an upgrade-property shim |
| SSR markup mismatches client | Declarative Shadow DOM not emitted | Render `<template shadowrootmode>` server-side |

## Related Skills

- `dark-mode` — CSS custom properties bridge theme tokens into Shadow DOM
- `accessibility-testing` — Shadow DOM needs careful ARIA, focus, and label management

## Usage

Example invocations:

- "/web-components" — Run the full web components workflow
- "web components on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [SUPUESTO]
- English-language output unless otherwise specified [DOC]
- Does not replace domain-expert judgment for final decisions [DOC]
- Out of scope: full design-system token architecture (see `dark-mode`), and cross-shadow focus trapping beyond per-component ARIA (see `accessibility-testing`) [INFERENCIA]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Form-associated control needed | Use `formAssociated = true` + `ElementInternals`; plain Shadow DOM inputs do not submit with the host form [DOC] |
| Legacy browser target | Add Custom Elements / Shadow DOM polyfills; verify `::part()` support [SUPUESTO] |
