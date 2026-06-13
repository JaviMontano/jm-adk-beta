# web-frontend — Body of Knowledge

Domain knowledge for routing and executing frontend implementation tasks. This is router knowledge: enough to choose the right playbook and to know what "good" means once inside it. Deep mechanics live in each `references/<topic>.md`.

## 1. The router model
`web-frontend` is a one-shot dispatcher over 15 playbooks. The governing rule: **resolve one `topic`, load one playbook, finish.** Loading multiple playbooks defeats the router — it costs context and dilutes focus. The spine for every topic is **Discover → Analyze → Execute → Validate**. [DOC]

### Topic families
| Family | Topics | What it decides |
|---|---|---|
| Framework code | react-development, angular-development, web-components | Component model, reactivity, lifecycle |
| Styling & structure | css-architecture, component-architecture | Styling methodology, component boundaries, state placement |
| Build & delivery | build-optimization, pwa-architecture | Bundle shape, caching, offline |
| Concerns | dark-mode, form-engineering, internationalization, localization-guide | Theming, input UX, locales |
| Archetypes | ecommerce-frontend, blog-cms, portfolio-sites, admin-dashboards | Whole-site composition |

## 2. Disambiguation rules (decision logic)
- **css-architecture vs component-architecture:** a question about the *styling system* (tokens, layers, methodology) → css-architecture; a question about *component boundaries, composition, or where state lives* → component-architecture. [INFERENCIA]
- **internationalization vs localization-guide:** *framework/runtime wiring* (message format, locale switching, bundle splitting per locale) → internationalization; *content and locale process* (translation pipeline, copy management) → localization-guide. [INFERENCIA]
- **dark-mode is standalone:** treat it as its own playbook, not a sub-task of css-architecture. [SUPUESTO]
- **Archetype vs concern:** if the request names a whole site type, route to the archetype and let it pull concerns; if it names a single concern, route to that concern. [INFERENCIA]

## 3. Key platform concepts
- **Server vs Client Components (RSC):** Server Components cut client JS but lose state/effects/browser APIs; `use client` belongs at the leaf that needs interactivity, never hoisted up the tree. RSC exists only in App-Router-class frameworks — a Vite/CRA SPA has none. [INFERENCIA]
- **State placement:** `useState`/`useReducer` for local; Context for low-frequency shared (theme/auth/locale); external store for high-frequency/complex. Context re-renders *all* consumers on value change — wrong for fast-changing state. [INFERENCIA]
- **CSS layering:** `@layer reset, tokens, base, components, utilities` ends specificity wars; `!important` in the component layer is a smell — reorder layers instead. [EXPLICIT]
- **Container vs media queries:** container queries make components context-agnostic; media queries handle page-level/viewport concerns. [INFERENCIA]
- **Build physics:** minimal payload (tree-shake, lazy-load), parallel loading (route-based splitting), compression (Brotli preferred, gzip fallback). An uncompressed production deploy is a bug. [EXPLICIT]
- **Theme without FOUC:** set `[data-theme]` in a blocking inline `<head>` script before first paint; respect `prefers-color-scheme` but allow a stored override. [INFERENCIA]
- **PWA core:** service worker (caching strategy) + Web App Manifest + offline-first; push via FCM. Offline reload must not white-screen. [EXPLICIT]

## 4. Standards & thresholds (the bar for "good")
- **Accessibility:** WCAG 2.1 AA minimum — contrast ≥ 4.5:1 for text, visible focus, keyboard-reachable, axe-core zero serious/critical. [EXPLICIT]
- **Performance:** Lighthouse > 90 across Perf/A11y/Best-Practices/SEO; no avoidable CLS (reserve layout space for async states). [EXPLICIT]
- **Bundle budgets:** initial < 250KB gzipped, no single chunk > 100KB gzipped, measured with `size-limit`; budgets are thresholds, not targets — investigate >10% growth in one PR. [EXPLICIT]
- **Verification before done:** every threshold is proven by its verifier (Profiler, size-limit, Lighthouse, axe, `.br` presence), never asserted. [DOC]

## 5. Decision rules
1. If two topics tie, ask one crisp question; otherwise infer and proceed. [SUPUESTO]
2. `depth=deep` → apply the playbook exhaustively and verify each step; `quick` → essentials, skip optional hardening. [CONFIG]
3. Confirm stack facts (framework version, bundler, browser targets) before prescribing capability-specific patterns; degrade gracefully when a capability is absent. [INFERENCIA]
4. Optimize only after a measured baseline exists — never on a hunch. [INFERENCIA]
5. Name the boundary and hand off anything backend/infra/design-only — do not absorb it. [INFERENCIA]

## 6. Evidence taxonomy (Alfa-core)
One tag per non-obvious claim, one spelling, never mixed with the Jarvis family:
`[CÓDIGO]` verifiable in code · `[CONFIG]` from configuration/tooling · `[DOC]` from documentation/spec · `[INFERENCIA]` reasoned inference · `[SUPUESTO]` assumption to confirm. Constitution v6.0.0 gates apply; prefer a script over ad-hoc steps.

## 7. Anti-patterns (router-level)
- Loading multiple playbooks "to be safe". [INFERENCIA]
- Guessing `topic` on a truly ambiguous request instead of asking one question. [SUPUESTO]
- Answering from memory instead of the playbook — frontend ecosystems drift fast. [INFERENCIA]
- Emitting code with zero tags, or declaring green without a real build/run/audit. [DOC]
