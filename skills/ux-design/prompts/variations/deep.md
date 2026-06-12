# Deep Variation — ux-design

`depth=deep`. Apply the routed playbook exhaustively and verify each step.

1. Resolve `topic`; confirm against the disambiguation rules before committing.
2. Read the single routed playbook in full.
3. Run the spine exhaustively:
   - **Discover** — user goal, primary task, audience, device/context, success
     metric, and which decisions are open vs. locked.
   - **Analyze** — walk every applicable heuristic / token / state, recording
     location, rule violated, and user consequence for each.
   - **Execute** — produce the complete deliverable: all severities for a
     critique; full token tables + component quick ref + a11y for a design system;
     atomic level + props contract + all states for a component.
   - **Validate** — re-check each item against the user goal; calibrate severities
     against each other; run deterministic checks (hex-literal grep, success-yellow,
     contrast) and log results.
4. Tag every non-obvious claim; mark heuristic Blockers `[SUPUESTO]` until
   confirmed by testing/analytics.
5. Full gate: single-playbook discipline, shape match, tags, color/contrast rule,
   no `{VACIO_CRITICO}`, critique integrity.

Example: "Deep design-system pass on this dashboard kit." → load
`references/design-system.md`, emit the full token set with `:root` injection,
verify zero hex literals outside `:root`, confirm success = `#FFD700` with black
text, and list every WCAG AA contrast pair checked.
