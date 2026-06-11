---
name: web-frontend
description: "Frontend implementation: frameworks, component/CSS architecture, builds, PWA, i18n, and site types (ecommerce, blog, portfolio, admin). Topics: admin-dashboards, angular-development, blog-cms, build-optimization, component-architecture, css-architecture, dark-mode, ecommerce-frontend, form-engineering, internationalization, localization-guide, portfolio-sites, pwa-architecture, react-development, web-components."
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

Router skill. Resolve `topic` from the request, then Read EXACTLY ONE playbook
from `routes:`. Never load the whole cluster. `depth=deep` → apply the playbook
exhaustively with verification at each step; `quick` → essentials only.

Spine: Discover → Analyze → Execute → Validate.
Quality gates: constitution v6.0.0 (enforcement), evidence tags, script-first rule.
