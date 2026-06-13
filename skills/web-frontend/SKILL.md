---
name: web-frontend
version: 1.0.0
description: "Frontend implementation router: pick ONE topic (react/angular/web-components, component/css architecture, build-optimization, pwa, dark-mode, i18n/localization, form-engineering, or a site type — ecommerce/blog-cms/portfolio/admin) and load only that playbook. Topics: admin-dashboards, angular-development, blog-cms, build-optimization, component-architecture, css-architecture, dark-mode, ecommerce-frontend, form-engineering, internationalization, localization-guide, portfolio-sites, pwa-architecture, react-development, web-components."
params:
  topic:
    enum: [admin-dashboards, angular-development, blog-cms, build-optimization, component-architecture, css-architecture, dark-mode, ecommerce-frontend, form-engineering, internationalization, localization-guide, portfolio-sites, pwa-architecture, react-development, web-components]
    required: true
    infer: from user request; ask only if ambiguous
  depth:
    enum: [quick, deep]
    default: quick
routes:
  admin-dashboards: references/admin-dashboards.md
  angular-development: references/angular-development.md
  blog-cms: references/blog-cms.md
  build-optimization: references/build-optimization.md
  component-architecture: references/component-architecture.md
  css-architecture: references/css-architecture.md
  dark-mode: references/dark-mode.md
  ecommerce-frontend: references/ecommerce-frontend.md
  form-engineering: references/form-engineering.md
  internationalization: references/internationalization.md
  localization-guide: references/localization-guide.md
  portfolio-sites: references/portfolio-sites.md
  pwa-architecture: references/pwa-architecture.md
  react-development: references/react-development.md
  web-components: references/web-components.md
---

# web-frontend

Router skill. Resolve `topic`, Read EXACTLY ONE playbook from `routes:`, execute it.

## When to use
Any frontend build/architecture task: framework code (React/Angular/web-components),
component or CSS structure, bundler tuning, PWA/offline, dark-mode, i18n/l10n, forms,
or a site archetype (ecommerce/blog/portfolio/admin). Not for backend, infra, or design-only. [INFERENCIA]

## Inputs / Outputs
- **In:** `topic` (required; infer from request, ask only if two topics tie), `depth` (quick|deep). [CONFIG]
- **Out:** the work the chosen playbook prescribes — code, config, or architecture decision with evidence tags.

## Routing
1. Map the request to ONE `topic` enum. Ambiguous pairs: css vs component → styling
   system = css-architecture, component boundaries/state = component-architecture;
   i18n (framework/runtime wiring) vs localization-guide (content/locale process);
   dark-mode is its own playbook, not a sub-task of css-architecture. [INFERENCIA]
2. Read the single mapped `routes:` file. NEVER load the cluster or a second playbook —
   pick the dominant topic and finish; re-invoke for a genuinely separate second need. [SUPUESTO]
3. `depth=deep` → apply the playbook exhaustively, verifying each step;
   `quick` → essentials only, skip optional hardening.

## Spine
Discover → Analyze → Execute → Validate. [DOC]

## Validation gate (done = all true)
- Exactly one playbook was loaded and its steps were followed. [DOC]
- Output runs/builds clean if it is code; config matches the target bundler/framework. [CONFIG]
- Every non-obvious claim carries one Alfa-core tag ([CÓDIGO]/[CONFIG]/[DOC]/[INFERENCIA]/[SUPUESTO]),
  one spelling, no mixing with the Jarvis family. See `references/verification-tags.md`. [DOC]
- Constitution v6.0.0 gates honored; script-first rule respected (prefer a script over ad-hoc steps). [DOC]
- Score the result against `assets/quality-rubric.json` (blocking router gates + the routed topic's gates); see `assets/README.md`. [DOC]

## Anti-patterns
- Loading multiple playbooks "to be safe" — defeats the router; costs context, dilutes focus. [INFERENCIA]
- Guessing `topic` when the request is truly ambiguous instead of asking one crisp question. [SUPUESTO]
- Answering from memory instead of the playbook (frontend ecosystems drift fast). [INFERENCIA]
- Emitting code with zero tags, or green-as-success without a real build/run check. [DOC]
