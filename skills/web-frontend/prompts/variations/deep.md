# Deep variation — web-frontend (depth=deep)

Exhaustive path: apply the routed playbook fully, verify every step, and clear the topic gate plus all cross-cutting gates with captured evidence.

## Steps
1. Resolve ONE `topic` (ask one question only on a true tie); read its single playbook.
2. Run the full Discover → Analyze → Execute → Validate spine, including the playbook's optional hardening, edge cases, and failure-mode mitigations.
3. Resolve every entry in the playbook's Decisions & Trade-offs table and justify each with a tag.
4. Run the complete verifier set for the topic and attach raw output:
   - `build-optimization`: `npx size-limit`, `npx vite-bundle-visualizer`, `find dist -name '*.br'`, assert no `.map` fetchable.
   - `css-architecture` / `dark-mode`: Lighthouse (all 4 categories > 90), axe-core (zero serious/critical), forced dark mode + 200% zoom, FOUC check.
   - `react-development` / `component-architecture`: Profiler re-render trace, RSC import audit, effect-cleanup audit.
   - `pwa-architecture`: Lighthouse PWA audit, offline-reload check.
5. Produce a full gate report: every criterion → evidence → pass/fail.

## Discipline (deep does not relax)
- Still ONE playbook only — depth means thorough, not multi-topic.
- One Alfa-core tag per non-obvious claim: `[CÓDIGO]` `[CONFIG]` `[DOC]` `[INFERENCIA]` `[SUPUESTO]`.
- Constitution v6.0.0, script-first, single brand, no client PII, never green-as-success.

Use when correctness and completeness outweigh speed.
