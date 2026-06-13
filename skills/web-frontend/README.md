# web-frontend

Frontend implementation **router**. One invocation resolves a single `topic`, loads exactly one playbook from `routes:`, and executes it under the Discover → Analyze → Execute → Validate spine. It does not bundle multiple playbooks — pick the dominant topic and finish; re-invoke for a genuinely separate second need.

## What it does
Routes any frontend build/architecture task to the correct distilled playbook and runs it to a verifiable gate. The 15 topics span three families:

- **Framework code:** `react-development`, `angular-development`, `web-components`.
- **Cross-cutting concerns:** `component-architecture`, `css-architecture`, `build-optimization`, `pwa-architecture`, `dark-mode`, `form-engineering`, `internationalization`, `localization-guide`.
- **Site archetypes:** `ecommerce-frontend`, `blog-cms`, `portfolio-sites`, `admin-dashboards`.

## When to use
- A request maps to one frontend topic: framework code, component/CSS structure, bundler tuning, PWA/offline, dark-mode, i18n/l10n, forms, or a site archetype.
- You want a measured, gate-passing result (build runs clean, Lighthouse/axe thresholds met, evidence tags on every non-obvious claim).

**Not for:** backend, infra, or design-only work. Hand off to the named boundary skill instead.

## How it routes / executes
1. **Resolve `topic`** — map the request to ONE enum value. Disambiguation rules live in `SKILL.md` (e.g. styling system → `css-architecture`; component boundaries/state → `component-architecture`; runtime i18n wiring → `internationalization` vs content/locale process → `localization-guide`). Ask one crisp question only on a true tie.
2. **Load one playbook** — Read the single mapped file under `references/`. Never load a second.
3. **Pick `depth`** — `quick` (essentials, default) or `deep` (exhaustive, verify each step).
4. **Execute + validate** — run the playbook's protocol, then its Validation Gate. Code must build/run clean; thresholds (bundle size, Lighthouse, WCAG 2.1 AA) must pass with evidence, never green-as-success.

## References (the 15 playbooks)
- `references/react-development.md` — Hooks, RSC/`use client` boundaries, Suspense, render-perf.
- `references/angular-development.md` — Angular app structure and patterns.
- `references/web-components.md` — custom elements, Shadow DOM, framework-agnostic UI.
- `references/component-architecture.md` — component boundaries, composition, state placement.
- `references/css-architecture.md` — BEM/utility-first, `@layer`, custom properties, container queries.
- `references/build-optimization.md` — Vite/Webpack chunking, tree shaking, Brotli/gzip, source maps.
- `references/pwa-architecture.md` — service workers, manifest, offline-first, push via FCM.
- `references/dark-mode.md` — `prefers-color-scheme` + `[data-theme]` override, no FOUC.
- `references/form-engineering.md` — validation, accessibility, controlled/uncontrolled inputs.
- `references/internationalization.md` — framework/runtime i18n wiring.
- `references/localization-guide.md` — content/locale process and pipeline.
- `references/ecommerce-frontend.md` — cart, checkout, product UI archetype.
- `references/blog-cms.md` — content site / CMS-backed frontend archetype.
- `references/portfolio-sites.md` — portfolio/marketing-site archetype.
- `references/admin-dashboards.md` — data-dense admin UI archetype.

## Companion bundle
- `assets/` — the DoD asset bundle (routing rubric + topic checklist). See `assets/README.md`.
- `agents/` — lead / specialist / support / guardian role contracts for this router.
- `knowledge/` — frontend body-of-knowledge and concept graph.
- `prompts/`, `templates/`, `evals/`, `examples/` — invocation prompts, the output scaffold, eval cases, and a worked example.

## Evidence convention
Every non-obvious claim carries exactly one Alfa-core tag: `[CÓDIGO]` `[CONFIG]` `[DOC]` `[INFERENCIA]` `[SUPUESTO]`. One taxonomy, one spelling, never mixed with the Jarvis family. Constitution v6.0.0 gates apply; prefer a script over ad-hoc steps.
