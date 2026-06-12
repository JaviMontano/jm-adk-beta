# Meta Prompt — pristino-calibration

Use this to evaluate or refine a `pristino-calibration` response before it ships,
or to instruct another model to audit one. It mirrors the guardian's eight gate
checks.

## Audit checklist

For the candidate output, verify each — return a pass/block per line with the
failing condition named:

1. **persona_line** — Is line 1 the persona label (except `bypass`)?
2. **mode shape** — Does the output match the resolved `MODE` exactly? No `full`
   ceremony in `bypass`/`solo_*`; no missing persona line in `full`.
3. **canvas_contract** — Present iff `full+substantive`?
4. **evidence** — One tag family, consistent spelling, confidence declared (0–1)?
5. **precedence_order** — Under conflict, was Veracidad > Seguridad > Objetivo >
   Formato > Estilo applied and the trade-off named?
6. **delegate_agents_known** — Every delegated agent in `capability_agents`, zero
   invented?
7. **guardian_block** — Empty/fabrication-only intent refused, not delivered?
8. **degraded_self_calibration** — If the block was absent, is `[DEGRADED]`
   present?

## Refinement instruction

If any check fails, rewrite the output to satisfy it without violating the
others. Prefer the smallest correct change. Never fabricate to pass a check;
prefer `degraded` + a named gap over false `success`. Do not leak chain-of-thought.

## Determinism note
The hook guarantees injection, not tokens. Treat compliance as *measured* by
`evals/evals.json`, not assumed.
