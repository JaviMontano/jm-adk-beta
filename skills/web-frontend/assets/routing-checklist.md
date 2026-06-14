# web-frontend routing checklist

Run top to bottom before declaring a `web-frontend` task done.

## Route
- [ ] Mapped the request to exactly ONE `topic` from the 15-value enum.
- [ ] Applied disambiguation where it mattered:
  - [ ] styling system → `css-architecture`; component boundaries/state → `component-architecture`.
  - [ ] runtime i18n wiring → `internationalization`; content/locale process → `localization-guide`.
  - [ ] `dark-mode` treated as standalone, not a css-architecture sub-task.
- [ ] Asked one crisp question ONLY on a true tie; otherwise inferred and proceeded.
- [ ] Out-of-scope (backend/infra/design-only) named and handed off, not absorbed.

## Load & confirm
- [ ] Read exactly ONE `references/<topic>.md`. No second playbook.
- [ ] Confirmed stack facts (framework + version, bundler, browser targets) before capability-specific prescriptions.
- [ ] Did NOT prescribe RSC/`use client` on a plain SPA, or unsupported CSS features without a fallback.

## Execute
- [ ] Followed Discover → Analyze → Execute → Validate for the routed topic.
- [ ] Resolved each Decisions & Trade-offs entry and justified it with a tag.
- [ ] Optimized only after a measured baseline (no guess-driven memo/chunking/compression).

## Validate (gate)
- [ ] Build/run clean; config matches target bundler/framework.
- [ ] Topic gate thresholds proven by their verifier (size-limit / Lighthouse / axe / Profiler / `.br` presence).
- [ ] Every non-obvious claim has exactly one Alfa-core tag: `[CÓDIGO]` `[CONFIG]` `[DOC]` `[INFERENCIA]` `[SUPUESTO]`.
- [ ] Single brand, no client PII, script-first (Constitution v6.0.0).
- [ ] Verdict is pass/fail/blocked with evidence — never green-as-success.
