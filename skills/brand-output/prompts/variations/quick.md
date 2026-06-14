# Quick Variation — brand-output

Fast path for an unambiguous branded-output request (`depth=quick`).

1. One-line route: pick the single topic that matches the named format + brand.
2. Read only that playbook; apply the essential token + structure rules.
3. Generate via the playbook's script; skip exhaustive deep-dive steps.
4. Run the gate's must-pass boxes: one playbook loaded, tokens from config,
   determinism honored, script-first, evidence tags present.

Use when: format and brand are explicit and only one enum fits.
Do NOT use when: two brands or two topics are plausible — escalate to `primary.md`
and ask one disambiguating question. [EXPLICIT]

Example: "Generate the MetodologIA HTML one-pager from these tokens" → `html-brand`,
quick essentials, gate, deliver.
