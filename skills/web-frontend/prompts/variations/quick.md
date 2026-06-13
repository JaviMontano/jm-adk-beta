# Quick variation — web-frontend (depth=quick)

Fast path: resolve the topic, run the playbook's essentials, ship a gate-passing result without optional hardening.

## Steps
1. Map the request to ONE `topic`; infer unless two topics truly tie.
2. Read that one `references/<topic>.md`.
3. Execute the core Execute-phase steps only — skip optional hardening the playbook marks as deep-only.
4. Run the minimum verifiers that prove the topic's hard gates (e.g. `size-limit` for build-optimization; Lighthouse + axe for css-architecture/dark-mode; Profiler for react-development).

## Keep even in quick mode
- One playbook only — no cluster loading.
- Build/run clean; no green-as-success.
- One Alfa-core tag per non-obvious claim: `[CÓDIGO]` `[CONFIG]` `[DOC]` `[INFERENCIA]` `[SUPUESTO]`.
- Single brand, no client PII.

## Skip in quick mode
- Exhaustive edge-case sweeps, secondary optimizations, and non-blocking polish — defer to a `deep` run if the user asks.

Use when the user wants a targeted, single-concern result now.
