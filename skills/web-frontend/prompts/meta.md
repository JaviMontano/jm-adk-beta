# Meta prompt — web-frontend (reasoning & self-check)

Use this to steer the router's own reasoning before and during execution.

## Pre-flight reasoning
- **Which family?** Place the request in one of: framework code / styling & structure / build & delivery / concerns / archetypes. This narrows 15 topics to a handful.
- **Is it a tie?** Only ask the user a question when two topics genuinely compete. If one topic is dominant, infer and proceed — do not stall.
- **Is it in scope?** Backend, infra, or design-only → name the boundary skill and hand off; do not absorb it.
- **What stack is real?** Never prescribe RSC/`use client` for a plain SPA, container queries for unsupported targets, or budgets sized for the wrong app shape. Confirm first.

## During execution
- Read ONE playbook. If you feel the urge to open a second, you mis-routed — re-resolve `topic` instead of loading both.
- Optimize only after a measured baseline. No guess-driven `memo`, chunking, or compression claims.
- For every threshold the playbook names, line up its verifier *before* claiming pass.

## Self-check before "done"
1. Exactly one playbook loaded and followed? 
2. Code builds/runs clean; config matches target bundler/framework?
3. Each topic-gate threshold proven by captured evidence (not asserted)?
4. Every non-obvious claim has exactly one Alfa-core tag, one spelling, no Jarvis mixing?
5. Single brand, no client PII, script-first respected?

If any answer is "no", the verdict is **fail/blocked** — fix or report the gap, never wave it through.

## Tag discipline
`[CÓDIGO]` `[CONFIG]` `[DOC]` `[INFERENCIA]` `[SUPUESTO]` — one per claim.
